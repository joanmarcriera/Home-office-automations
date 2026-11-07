import streamlit as st
import requests

# This would ideally come from environment variables
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="HITL Document Review", layout="wide")

st.title("🛡️ Human-in-the-Loop Document Review")
st.write("Review and approve AI-extracted metadata before it's committed to the system of record.")

def get_staged_docs():
    try:
        response = requests.get(f"{BACKEND_URL}/staged-docs")
        return response.json()
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
        return []

staged_docs = get_staged_docs()

if not staged_docs:
    st.info("No documents currently awaiting review.")
else:
    # Sidebar for selection
    st.sidebar.header("Pending Documents")
    doc_options = {str(doc['id']): f"{doc['original_metadata'].get('title', 'Untitled')} ({doc['staged_at'][:10]})" for doc in staged_docs}
    selected_id = st.sidebar.selectbox("Select a document to review", options=list(doc_options.keys()), format_func=lambda x: doc_options[x])

    # Find the selected doc
    selected_doc = next(doc for doc in staged_docs if str(doc['id']) == selected_id)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Visual Reference")
        st.info(f"Source URL: {selected_doc['source_document_url']}")
        # In a real app, you'd use st.iframe or st.image to show the actual PDF/Image
        st.image("https://via.placeholder.com/600x800.png?text=Document+Preview+Placeholder", caption="Document Preview")

    with col2:
        st.subheader("Metadata Verification")

        # Form for editing
        with st.form("review_form"):
            metadata = selected_doc['corrected_metadata'] or selected_doc['original_metadata']

            edited_metadata = {}
            for key, value in metadata.items():
                edited_metadata[key] = st.text_input(key.replace("_", " ").title(), value=str(value))

            c1, c2 = st.columns(2)
            with c1:
                submitted = st.form_submit_button("Approve & Sync", type="primary", use_container_width=True)
            with c2:
                rejected = st.form_submit_button("Reject", type="secondary", use_container_width=True)

            if submitted:
                try:
                    res = requests.post(f"{BACKEND_URL}/approve/{selected_id}", json=edited_metadata)
                    if res.status_code == 200:
                        st.success("Document approved and synced!")
                        st.rerun()
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Failed to approve: {e}")

            if rejected:
                try:
                    res = requests.post(f"{BACKEND_URL}/reject/{selected_id}")
                    if res.status_code == 200:
                        st.warning("Document rejected and removed.")
                        st.rerun()
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Failed to reject: {e}")

st.divider()
st.caption("Home-Office Automation - HITL Module v1.0")
