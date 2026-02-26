import os
import sys
import yaml
import json
import time
import feedparser
import hashlib
from datetime import datetime, timedelta, timezone
from openai import OpenAI

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
DATA_DIR = "data"
DAILY_DIR = "daily"
SOURCES_FILE = "sources.yaml"
PROCESSED_FILE = os.path.join(DATA_DIR, "processed.json")
README_FILE = "README.md"

# Model selection with comma separated fallbacks (e.g., model1,model2,model3)
MODEL_STRING = os.environ.get(
    "OPENROUTER_MODEL", 
    "meta-llama/llama-3.3-70b-instruct:free,google/gemini-2.0-pro-exp-02-05:free,mistralai/mistral-nemo:free,nvidia/llama-nemotron-embed-vl-1b-v2:free"
)
MODELS = [m.strip() for m in MODEL_STRING.split(",")]

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY environment variable not set.")
    sys.exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def ensure_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DAILY_DIR, exist_ok=True)

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_processed(processed_set):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(processed_set), f)

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def fetch_source(source, processed_set, cutoff_date):
    """
    Fetches a single source and returns a list of new items.
    """
    url = source.get("url")
    src_type = source.get("type", "rss").lower()
    name = source.get("name", "Unknown Source")
    
    new_items = []
    
    if src_type in ["rss", "reddit"]:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Fallback chains for finding link & title
            link = getattr(entry, "link", getattr(entry, "id", None))
            title = getattr(entry, "title", "No Title")
            
            if not link:
                link = get_hash(title)
                
            if link in processed_set:
                continue
                
            # Date filtering
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                entry_date = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc)
                if entry_date < cutoff_date:
                    continue
                    
            summary = getattr(entry, "summary", "")[:800] # Truncate to save context
            
            new_items.append({
                "source": name,
                "title": title,
                "link": link,
                "summary": summary
            })
            processed_set.add(link)
    else:
        print(f"Skipping {name} - unsupported type '{src_type}'")
        
    return new_items

def summarize_with_openrouter(items):
    """
    Sends the items to OpenRouter for summarisation and categorisation.
    """
    system_prompt = """
You are an expert AI curator, editor, and analyst. You are given a raw list of news items, blog posts, and forum discussions from the past 24 hours regarding AI, LLMs, and technology.

Your task is to create a beautifully formatted Markdown digest.

Rules & Guidelines:
1. **Executive Summary**: Start with a 3-5 bullet point summary of the most important news.
2. **Deduplicate**: If multiple items cover the exact same story (e.g., a new model release reported by 3 different sources), merge them into a single coherent update.
3. **Categorise**: Organise the items into logical sections. Use headings like:
   - 🚀 Models & Releases
   - 🛠️ Tools & Agents (e.g., Open Source, MCP, new libraries)
   - 🔬 Research & Papers
   - 🏢 Industry News
   (You don't have to use all of them, only what fits best).
4. **Formatting**: Use Markdown extensively. Provide links back to the original source (`[Source Name](link)`). Keep summaries concise but informative.
5. **Curation**: Ignore highly irrelevant, extremely localized, or spammy items. Flag "highly important" updates with a pushpin 📌 or fire 🔥 emoji.
6. **No Markdown Wrapper**: Return ONLY the raw Markdown text. Do NOT wrap the entire response in ` ```markdown ` or any other code block wrappers.
"""

    user_content = json.dumps(items, indent=2)
    prompt = f"Here are the new items to process:\n\n{user_content}"
    
    for model in MODELS:
        try:
            print(f"Attempting to generate digest with model: {model}...")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3, # Low temperature for more factual summaries
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate limit" in err_str or "temporarily rate-limited" in err_str or hasattr(e, 'status_code') and e.status_code == 429:
                print(f"Model {model} is rate limited. Trying next fallback...")
                continue
            else:
                print(f"Failed to generate digest via OpenRouter with {model}: {e}")
                # Don't fallback for non-rate-limit errors like 401 unauthorized
                return None
                
    print("All fallback models were rate limited or failed.")
    return None

def update_readme(digest_md, date_str):
    """
    Optionally prepends the latest digest to the README.md or a central file.
    """
    header = f"## 📅 Digest for {date_str}\n\n"
    
    if not os.path.exists(README_FILE):
        content = f"# AI Daily Digest\n\n{header}{digest_md}\n"
    else:
        with open(README_FILE, "r") as f:
            content = f.read()
            
        # Find the marker or simply prepend below the main header
        marker = "# AI Daily Digest\n"
        if marker in content:
            content = content.replace(marker, f"{marker}\n{header}{digest_md}\n\n---\n\n")
        else:
            content = f"{marker}\n{header}{digest_md}\n\n---\n\n" + content
            
    with open(README_FILE, "w") as f:
        f.write(content)

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
def main():
    ensure_directories()
    
    if not os.path.exists(SOURCES_FILE):
        print(f"Error: {SOURCES_FILE} not found. Please create one.")
        sys.exit(1)
        
    with open(SOURCES_FILE, "r") as f:
        try:
            sources = yaml.safe_load(f)
        except Exception as e:
            print(f"Error parsing {SOURCES_FILE}: {e}")
            sys.exit(1)
            
    processed_set = load_processed()
    all_new_items = []
    
    # We look back up to 48 hours to account for timezone differences and scraping delays
    cutoff_date = datetime.now(timezone.utc) - timedelta(hours=48)
    
    print("Fetching sources...")
    for source in sources:
        items = fetch_source(source, processed_set, cutoff_date)
        all_new_items.extend(items)
        
    if not all_new_items:
        print("No new items found. Exiting cleanly.")
        sys.exit(0)
        
    print(f"Found {len(all_new_items)} new items. Processing with OpenRouter (Models: {', '.join(MODELS)})...")
    
    digest_md = summarize_with_openrouter(all_new_items)
    
    if not digest_md:
        sys.exit(1)
        
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_file = os.path.join(DAILY_DIR, f"{date_str}.md")
    
    with open(out_file, "w") as f:
        f.write(f"# Daily Digest - {date_str}\n\n")
        f.write(digest_md)
        f.write("\n")
        
    print(f"Successfully generated digest: {out_file}")
    
    # Update main README
    update_readme(digest_md, date_str)
    
    save_processed(processed_set)
    print("State saved. Done.")

if __name__ == "__main__":
    main()
