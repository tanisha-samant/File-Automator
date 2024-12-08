import streamlit as st
from azure_services.azure_setup import (
    summarize_and_extract_details,
    classify_document,
    translate_text,
    enhance_ocr_with_context,
)
from utilss.ocr import extract_text_from_pdf, extract_text_from_docx
from database.database import (
    create_table,
    insert_document,
    get_all_documents,
    get_document_summary,
    get_document_type,
    get_ocr_enhanced,
    delete_document,
)

def main():
    create_table()
    
    st.set_page_config(
        page_title="Document Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        .document-card {
            background-color: #0000;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            position: relative;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar for file upload and processing
    with st.sidebar:
        st.title("Document Upload")
        uploaded_file = st.file_uploader(
            "Upload a PDF or DOCX file",
            type=["pdf", "docx"],
            help="Supported formats: PDF and DOCX"
        )
        
        if uploaded_file:
            # Check file size (limit set to 5 MB)
            if uploaded_file.size > 5 * 1024 * 1024:  # 5 MB in bytes
                st.error("File size exceeds 5 MB. Please upload a smaller file.")
            else:
                st.success(f"File uploaded: {uploaded_file.name}")

    # Main content area
    st.title("📄 Document Assistant")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Process Document", "View All Documents", "Translate Document"])

    with tab1:
        
        if uploaded_file is not None:
            with st.spinner("Processing document..."):
                # Extract text based on the file type
                if uploaded_file.type == "application/pdf":
                    extracted_text = extract_text_from_pdf(uploaded_file)
                else:
                    extracted_text = extract_text_from_docx(uploaded_file)

                if extracted_text:
                    document_name = uploaded_file.name
                    document_type = classify_document(extracted_text)
                    
                    # Process document
                    st.write("🔄 Analyzing document...")
                    summary = summarize_and_extract_details(extracted_text)
                    ocr_enhanced = enhance_ocr_with_context(extracted_text)
                    
                    # Store in database
                    insert_document(document_name, document_type, summary, ocr_enhanced)
                    st.success("✅ Document processed successfully!")

                    if st.button("Summarize Document"):
                        document_summary = get_document_summary(document_name)
                        st.write(f"Summary: {document_summary}")
                        st.success("✅ Document summarized successfully!")
                        
                    if st.button("Classify Document"):
                        document_type_info = get_document_type(document_name)
                        st.write(f"Document Type: {document_type_info}")
                        st.success("✅ Document classified successfully!")
                        
                    if st.button("Enhance OCR Text"):
                        ocr_text = get_ocr_enhanced(document_name)
                        st.write(f"**Enhanced OCR Text:** {ocr_text}")
                        st.success("✅ OCR text enhanced successfully!")

                    
                    
                else:
                    st.error("⚠️ Could not extract text from the document. Please try a different file.")

    with tab2:
        st.markdown("### 📚 Document Library")
        documents = get_all_documents()
        
        if not documents:
            st.info("No documents found in the database.")
        else:
            for doc in documents:
                with st.container():
                    st.markdown(f"""
                        <div class="document-card">
                            <h4>📄 {doc[1]}</h4>
                            <p><strong>Type:</strong> {doc[2]}</p>
                            <p><strong>Summary:</strong> {doc[3][:100] if doc[3] else "No summary available"}...</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Adding Delete button for each document
                    if st.button(f"Delete {doc[1]}", key=f"delete_{doc[0]}"):
                        delete_document(doc[1])
                        st.success(f"Document '{doc[1]}' deleted successfully!")
                        st.experimental_rerun()  

    with tab3:
        st.markdown("### 🌐 Translate Document")
        if uploaded_file is not None:
            try:
                # Check file size before processing
                file_size = uploaded_file.size
                if file_size > 10 * 1024 * 1024:  # 10 MB limit
                    st.error(f"File size is {file_size/1024/1024:.2f} MB. Please upload a file smaller than 10 MB.")
                else:
                    with st.spinner("Processing document..."):
                        # Extract text based on the file type
                        if uploaded_file.type == "application/pdf":
                            extracted_text = extract_text_from_pdf(uploaded_file)
                        else:
                            extracted_text = extract_text_from_docx(uploaded_file)
                        # Check if text extraction was successful
                        if not extracted_text:
                            st.error("Could not extract text from the document. The file might be corrupted or unsupported.")
                        else:
                            # Log extracted text details
                            st.write(f"📄 Extracted Text Length: {len(extracted_text)} characters")
                            # Select target language
                            language = st.selectbox(
                                "Select target language",
                                 options=[
                                     "French", "Spanish", "German", 
                                     "Italian", "Portuguese", 
                                     "Telugu", "Hindi", "Marathi", "Odia"
                                 ]
                            )
                            if st.button("Translate Document"):
                                with st.spinner(f"Translating to {language}..."):
                                    translated_text = translate_text(extracted_text, language)
                                    if translated_text:
                                        st.success("Translation Complete!")
                                        st.text_area("Translated Text", value=translated_text, height=300)
                                    else:
                                        st.error("Translation failed. Please check the logs.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()