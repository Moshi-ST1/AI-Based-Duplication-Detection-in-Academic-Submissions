# Implementation Code
import streamlit as st 
import pytesseract 
from pdf2image import convert_from_path 
from PIL import Image 
import tempfile 
import io 
from difflib import SequenceMatcher 
import plotly.express as px 
 
# Setup Tesseract path 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 
st.set_page_config(page_title="Duplication Checker", layout="centered") 
st.title("Academic Duplication Checker") 
 
# Extract text from PDF 
def extract_text_from_pdf(pdf_file): 
    images = convert_from_path(pdf_file) 
    full_text = '' 
    for image in images: 
        text = pytesseract.image_to_string(image.convert('L')) # Grayscale 
        full_text += text + '\n' 
    return full_text 
 
# Calculate similarity percentage 
def simple_similarity(text1, text2): 
    return SequenceMatcher(None, text1, text2).ratio() * 100 
 
# Get common words 
def get_common_words(text1, text2): 
    words1 = set(text1.lower().split()) 
    words2 = set(text2.lower().split()) 
    common = words1.intersection(words2) 
    return sorted(list(common)) 
 
# File uploader 
uploaded_files = st.file_uploader("Upload Documents (PDF/Image/Text)", type=["pdf", "png", 
"jpg", "jpeg", "txt"], accept_multiple_files=True) 
 
if st.button("Check for Duplicates"): 
    if len(uploaded_files) >= 2: 
        text_files = [] 
        file_names = [] 
        report = io.StringIO() 
        threshold = 10.0 # Minimum threshold for duplication alert 
 
        with st.spinner("Extracting text..."): 
            for uploaded_file in uploaded_files: 
                text = "" 
                file_names.append(uploaded_file.name) 
                if uploaded_file.type == "application/pdf": 
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp: 
                        tmp.write(uploaded_file.read()) 
                        text = extract_text_from_pdf(tmp.name) 
                elif uploaded_file.type.startswith("image/"): 
                    image = Image.open(io.BytesIO(uploaded_file.read())) 
                    text = pytesseract.image_to_string(image.convert('L')) 
                elif uploaded_file.type == "text/plain": 
                    text = uploaded_file.read().decode("utf-8") 
                text_files.append(text) 
 
        st.header("Extracted Text") 
        for i, text in enumerate(text_files): 
            st.subheader(file_names[i]) 
            st.text_area("Text", text, height=200) 
 
        duplicates_found = False 
        for i in range(len(text_files)): 
            for j in range(i + 1, len(text_files)): 
                sim = simple_similarity(text_files[i], text_files[j]) 
                common_words = get_common_words(text_files[i], text_files[j]) 
 
                st.subheader(f"{file_names[i]} vs {file_names[j]}") 
                st.write(f"**Duplicate Percentage:** {sim:.2f}%") 
                report.write(f"{file_names[i]} vs {file_names[j]}\nDuplicate Percentage: {sim:.2f}%\n") 
 
                # PIE CHART 
                pie_labels = ["Duplicate", "Non-Duplicate"] 
                pie_values = [sim, 100 - sim] 
                pie_colors = ["red", "green"] 
 
                pie_fig = px.pie( 
                    names=pie_labels, 
                    values=pie_values, 
                    color=pie_labels, 
                    color_discrete_map={"Duplicate": "red", "Non-Duplicate": "green"}, 
                    title=f"Similarity Distribution: {file_names[i]} vs {file_names[j]}" 
                ) 
                pie_fig.update_traces(textinfo='label+percent', hole=0.3) 
                st.plotly_chart(pie_fig) 
 
                if sim >= threshold: 
                    duplicates_found = True 
                    st.warning("Possible duplication detected!") 
                else: 
                    st.success("No significant duplication.") 
 
                if common_words: 
                    st.markdown("**Common Words:**") 
                    st.write(", ".join(common_words)) 
                    report.write("Common Words:\n" + ", ".join(common_words) + "\n\n") 
                else: 
                    st.write("No common words found.") 
                    report.write("No common words found.\n\n") 
 
        st.download_button("Download Report", report.getvalue(), 
file_name="duplication_report.txt") 
    else: 
        st.error("Please upload at least two files.")
