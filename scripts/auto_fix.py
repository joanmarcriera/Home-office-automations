import os
import sys
import subprocess
import json

def get_issue(issue_number):
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_number), "--json", "title,body"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch issue {issue_number}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_fix.py <issue_number>")
        sys.exit(1)
        
    issue_number = sys.argv[1]
    issue = get_issue(issue_number)
    
    title = issue.get('title', 'Unknown Issue')
    body = issue.get('body', '')
    
    prompt = f"""Please fix the following GitHub issue. Search the repository for relevant files and update them to resolve the problem. 

# Issue {issue_number}: {title}

{body}
"""
    with open("issue_prompt.txt", "w") as f:
        f.write(prompt)
        
    model = os.environ.get("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
    
    print(f"Running Aider on issue #{issue_number} using OpenRouter model {model}...")
    
    # Run aider with OpenRouter free model to do the automated fixing and committing
    cmd = [
        "aider",
        f"--model=openrouter/{model}",
        "--message-file=issue_prompt.txt",
        "--yes",
        "--auto-commits",
        "--no-suggest-shell-commands"
    ]
    
    # We use subprocess.call to stream stdout/stderr interactively or to the CI logs
    ret = subprocess.call(cmd)
    
    if os.path.exists("issue_prompt.txt"):
        os.remove("issue_prompt.txt")
        
    if ret != 0:
        print("Aider exited with a non-zero status code.")
        sys.exit(ret)

if __name__ == "__main__":
    main()
