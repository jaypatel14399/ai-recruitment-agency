from utils.text_extractor import extract_text_from_pdf, extract_text_from_docx

print("=== PDF Extraction ===")
pdf_text = extract_text_from_pdf("C:/Users/jaypa/ai-recruitment-agency/backend/uploads/JayResumeDraft.pdf")
print(pdf_text[:500])  # Print first 500 chars

print("\n=== DOCX Extraction ===")
docx_text = extract_text_from_docx("C:/Users/jaypa/ai-recruitment-agency/backend/uploads/JayResumeDraft.docx")
print(docx_text[:500])
