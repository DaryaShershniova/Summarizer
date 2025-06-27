from transformers import pipeline
import gradio as gr
from docx import Document
from PyPDF2 import PdfReader
import os

# Model initialization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def extract_text_from_file(file):
    """Extracts text from a file (txt, docx, pdf)"""
    try:
        if file.name.endswith('.txt'):
            with open(file.name, 'r', encoding='utf-8') as f:
                return f.read()

        elif file.name.endswith('.docx'):
            doc = Document(file.name)
            return "\n".join([para.text for para in doc.paragraphs if para.text])

        elif file.name.endswith('.pdf'):
            reader = PdfReader(file.name)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text

        return "Unsupported file format. Only TXT, DOCX, PDF are supported."
    except Exception as e:
        return f"File reading error: {str(e)}"


def split_text(text, chunk_size=500):
    """Splits text into parts for processing"""
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def summarize_long_text(text):
    """Processes long texts"""
    chunks = split_text(text)
    summaries = []
    for chunk in chunks:
        if len(chunk) > 10:
            try:
                summary = summarizer(chunk, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
                summaries.append(summary)
            except Exception as e:
                summaries.append(f"[Error summarizing text part: {str(e)}]")
    return " ".join(summaries)


def summarize(text):
    """The main function of summation"""
    if not text.strip():
        return "Please enter text to summarize"

    try:
        if len(text) > 1000:
            return summarize_long_text(text)
        return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    except Exception as e:
        return f"Summarization error: {str(e)}"


def process_input(text, file):
    """Processes input - text/file"""
    if file is not None:
        file_text = extract_text_from_file(file)
        if "Unsupported" in file_text or "Error" in file_text:
            return file_text
        return summarize(file_text)
    return summarize(text)


# Сreating an interface
with gr.Blocks(title="Text Summarization Tool") as app:
    gr.Markdown("## Text Summarization Tool")
    gr.Markdown("Upload a file or enter text for summarization")

    with gr.Row():
        with gr.Column():
            text_input = gr.TextArea(label="Enter text", lines=10,
                                     placeholder="Type or paste your text here...")
            file_input = gr.File(label="Upload file (TXT, DOCX, PDF)",
                                 file_types=[".txt", ".pdf", ".docx"])
            summarize_btn = gr.Button("Text Summarization", variant="primary")

        with gr.Column():
            output = gr.TextArea(label="Summary Result", lines=10, interactive=False)

    # Handler for button
    summarize_btn.click(
        fn=process_input,
        inputs=[text_input, file_input],
        outputs=output,
        api_name="summarize"
    )

# Launch the application
if __name__ == "__main__":
    app.launch(share=True)
