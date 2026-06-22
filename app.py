
# Frontend interface setup snippet
import streamlit as st 
st.set_page_config(page_title="Duplication Checker", layout="centered") 
st.title("Academic Duplication Checker") 
# File uploader 
uploaded_files = st.file_uploader("Upload Documents (PDF/Image/Text)", 
                                  type=["pdf", "png", "jpg", "jpeg", "txt"], 
                                  accept_multiple_files=True 
                                 )


# Frontend output display snippet 
if st.button("Check for Duplicates"): 
    st.spinner("Extracting text...") 
    st.header("Extracted Text") 
    st.subheader("Similarity Results") 
    st.plotly_chart(pie_fig) 
    st.download_button("Download Report", report.getvalue(), 
file_name="duplication_report.txt")
