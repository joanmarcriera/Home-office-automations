import streamlit as st
import requests
import os
from datetime import datetime

# Configuration - should match video_search_api.py default
BACKEND_URL = os.environ.get("VIDEO_SEARCH_API_URL", "http://localhost:8000")

st.set_page_config(page_title="Family Video Archive Search", layout="wide")

st.title("🎥 Family Video Archive Search")
st.write("Search through decades of family memories using natural language.")

# Search interface
query = st.text_input("What are you looking for?", placeholder="e.g., 'birthday party in the garden' or 'kids playing with snow'")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Search Settings")
    limit = st.slider("Max results", 1, 20, 5)

    st.divider()
    st.info("💡 Tip: Try searching for specific events, people, or emotions.")

if query:
    with st.spinner(f"Searching for '{query}'..."):
        try:
            response = requests.get(f"{BACKEND_URL}/search", params={"query": query, "limit": limit})
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                if not results:
                    st.warning("No matching videos found. Try a different query.")
                else:
                    st.success(f"Found {data['total_found']} results in {data['processing_time_ms']:.2f}ms")

                    for doc in results:
                        with st.container():
                            st.divider()
                            c1, c2 = st.columns([1, 2])

                            with c1:
                                # Mock video preview
                                st.image("https://placehold.co/400x225?text=Video+Preview+Placeholder", width="stretch")
                                if doc.get("url"):
                                    st.link_button("Play Video", doc["url"])

                            with c2:
                                st.subheader(doc['filename'])
                                st.write(f"**Relevance Score:** {doc['relevance_score']:.2f}")
                                st.write(f"**Transcript Snippet:**")
                                st.write(f"_{doc['transcript_snippet']}_")

                                # Display tags
                                if doc.get("tags"):
                                    st.write("**Tags:**")
                                    tags_html = " ".join([f'<span style="background-color: #f0f2f6; padding: 2px 8px; border-radius: 10px; margin-right: 5px;">{tag}</span>' for tag in doc["tags"]])
                                    st.markdown(tags_html, unsafe_allow_html=True)

                                st.caption(f"Processed on: {doc['processed_at']}")
            else:
                st.error(f"Error from search API: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to video search API at {BACKEND_URL}: {e}")
            st.info("Ensure the backend API is running: `python scripts/video_search_api.py`")

else:
    st.info("Enter a query above to start searching.")

st.divider()
st.caption("Home-Office Automation - Video Archive Module v1.0")
