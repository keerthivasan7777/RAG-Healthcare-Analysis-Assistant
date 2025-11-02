import streamlit as st
from rag import process_urls, generate_answer
import os
from pathlib import Path

st.set_page_config(page_title="Healthcare Analysis Assistant", page_icon="🏥")
st.title("🏥 Healthcare Analysis Assistant")
st.markdown("*Your intelligent medical research companion* 🩺")

# Medical disclaimer at the top
st.warning("⚕️ **Medical Disclaimer**: This tool is for educational and research purposes only. Always consult qualified healthcare professionals for medical advice, diagnosis, or treatment.")

# Initialize session state for tracking processed URLs
if 'urls_processed' not in st.session_state:
    # Check if vector store already exists
    vectorstore_path = Path(__file__).parent / "resources/vectorstore"
    st.session_state.urls_processed = vectorstore_path.exists() and any(vectorstore_path.iterdir()) if vectorstore_path.exists() else False

# Sidebar URL inputs
st.sidebar.header("📋 Setup Healthcare Resources")
st.sidebar.markdown("*Add URLs from trusted medical sources*")
st.sidebar.markdown("**Recommended sources:** PubMed, WHO, CDC, NIH, medical journals")

url1 = st.sidebar.text_input("URL 1", placeholder="https://pubmed.ncbi.nlm.nih.gov/...")
url2 = st.sidebar.text_input("URL 2", placeholder="https://www.who.int/...")
url3 = st.sidebar.text_input("URL 3", placeholder="https://www.cdc.gov/...")

# Process URLs button
if st.sidebar.button("Process URLs"):
    urls = [url for url in (url1, url2, url3) if url.strip() != ""]
    if not urls:
        st.sidebar.warning("❌ You must provide at least one valid URL")
    else:
        status_container = st.container()
        with status_container:
            with st.spinner("Processing medical resources..."):
                try:
                    for status in process_urls(urls):
                        st.write(status)
                    st.session_state.urls_processed = True
                    st.success("✅ Medical resources processed successfully!")
                except Exception as e:
                    st.error(f"❌ Error processing URLs: {e}")
                    st.session_state.urls_processed = False

# Display status indicator
if st.session_state.urls_processed:
    st.sidebar.success("✅ Ready to analyze healthcare data!")
else:
    st.sidebar.info("💡 Load medical resources first")

# Query input section
st.markdown("---")
st.subheader("💬 Ask your medical research question")
query = st.text_input("Type your question here...", placeholder="e.g., What are the treatment guidelines for hypertension?")

if query:
    if not st.session_state.urls_processed:
        st.warning("⚠️ Please load medical resources first from the sidebar 👈")
    else:
        with st.spinner("Analyzing medical literature... 💭"):
            try:
                answer, sources = generate_answer(query)
                
                # Display answer in a medical-themed format
                st.markdown("### 📋 Analysis:")
                st.markdown(f"""
                <div style='
                    background-color: {"#1a1a2e" if st.get_option("theme.base") == "dark" else "#f0f8ff"};
                    color: {"#ffffff" if st.get_option("theme.base") == "dark" else "#000000"};
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid #2196F3;
                    line-height: 1.8;
                '>
                    {answer}
                </div>
                """, unsafe_allow_html=True)
                
                # Show sources in an expander
                with st.expander("📚 Sources (click to view)"):
                    st.markdown("**Retrieved from:**")
                    for source in sources.split("\n"):
                        if source.strip():
                            st.markdown(f"- `{source}`")
                
                # Additional disclaimer after answer
                st.info("💡 **Remember**: This analysis is based on the provided sources. Medical knowledge evolves constantly. Always verify with current medical professionals and guidelines.")
                
            except Exception as e:
                st.error(f"😅 Oops! Something went wrong: {e}")
                st.info("💡 Try rephrasing your question or check your internet connection!")

# Display instructions if no URLs processed yet
if not st.session_state.urls_processed:
    st.info("👋 **Welcome!** To get started:\n\n1. Add trusted medical resource URLs in the sidebar 👈\n2. Click 'Process URLs' \n3. Ask healthcare analysis questions!")
    
    st.markdown("---")
    st.markdown("### 💡 Example Questions:")
    st.markdown("""
    - What are the latest treatment guidelines for Type 2 diabetes?
    - Summarize recent research on cardiovascular disease prevention
    - What are the diagnostic criteria for chronic kidney disease?
    - Explain evidence-based practices for wound care
    - What are the risk factors for stroke?
    - What are common side effects of statins?
    - How is asthma diagnosed in children?
    """)
    
    st.markdown("---")
    st.markdown("### 📌 Trusted Medical Sources:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - **PubMed**: pubmed.ncbi.nlm.nih.gov
        - **WHO**: www.who.int
        - **CDC**: www.cdc.gov
        - **NIH**: www.nih.gov
        """)
    with col2:
        st.markdown("""
        - **Mayo Clinic**: www.mayoclinic.org
        - **Cleveland Clinic**: my.clevelandclinic.org
        - **UpToDate**: www.uptodate.com
        - **Cochrane**: www.cochrane.org
        """)

# Footer
st.markdown("---")
st.markdown("*Built for healthcare research and education | Not a substitute for professional medical advice*")