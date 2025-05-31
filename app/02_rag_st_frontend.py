import base64

import pymupdf
from PIL import Image
from datetime import datetime

import streamlit as st


# ------------ Config ------------
MAX_FILES = 3
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# ------------ Helper ------------
def extract_text(pdf_bytes: bytes) -> str:
    """
    Extract all text from a PDF using pymupdf
    """
    doc = pymupdf.open(stream=pdf_bytes, filetype='pdf')
    return "\n\n".join(page.get_text("text") for page in doc)

@st.cache_data(show_spinner=False)
def render_page_image(pdf_bytes: bytes, page_number: int = 0, zoom: float = 2.0) -> Image.Image:
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pix = doc.load_page(page_number).get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    mode = "RGBA" if pix.alpha else "RGB"
    return Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    

# ------------ St UI ------------
st.set_page_config(page_title='Project Chitti', layout='centered')
st.title("Project Chitti")

with st.sidebar:
    # File uploader
    uploaded_files = st.file_uploader(
        f'Upload up to a {MAX_FILES} files. (< {MAX_FILE_SIZE // 1024 // 1024} MB each)',
        type='pdf',
        accept_multiple_files=True
    )

    if uploaded_files:
        # Enforce file count limit
        if len(uploaded_files) > MAX_FILES:
            st.error(f'Please upload at max {MAX_FILES} files.')
        else:
            progress = st.progress(0)
            total = len(uploaded_files)
            for idx, uploaded_file in enumerate(uploaded_files, start=1):
                st.header(uploaded_file.name)

                # Check if it meets the allowed size threshold
                if uploaded_file.size > MAX_FILE_SIZE:
                    st.warning(f'{uploaded_file.name} is > than {MAX_FILE_SIZE // 1024 // 1024}')
                else:
                    pdf_bytes = uploaded_file.read()


                    # 1 - preview PDF: using image
                    # Let the user pick a page
                    page_idx = st.slider("Choose page", min_value=1, max_value=10, value=1)
                    try:
                        img = render_page_image(pdf_bytes, page_number=page_idx-1, zoom=1.0)
                        st.image(img, caption=f"Page {page_idx-1}", use_container_width=True)
                    except Exception as e:
                        st.error(f'Could not render page image. Error: {e}')

                    # 2 - Extract & Display the PDF text
                    with st.expander("Show pymupdf text"):
                        text = extract_text(pdf_bytes)
                        if text.strip():
                            st.text_area("Full text", text, height=600)
                        else:
                            st.write("_ NO TEXT FOUND _")

                    progress.progress(int(idx / total *100))

                progress.empty()

# Chatbot Portion


# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title
st.header("Ask Chitti")

# Create main chat container
chat_container = st.container(height=500)

# Display all chat messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            st.caption(f"*{message['timestamp']}*")

# Chat input (always at bottom)
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    timestamp = datetime.now().strftime("%H:%M:%S")
    user_message = {
        "role": "user", 
        "content": prompt,
        "timestamp": timestamp
    }
    st.session_state.messages.append(user_message)
    
    # Display the new user message
    with chat_container:
        with st.chat_message("user"):
            st.write(prompt)
            st.caption(f"*{timestamp}*")
    
    # Rerun to refresh the display
    st.rerun()

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Footer info
if not st.session_state.messages:
    st.info("👋 Start chatting by typing a message below!")