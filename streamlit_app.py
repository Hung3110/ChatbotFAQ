import streamlit as st
import requests
import os

st.title("Chatbot FAQ Nội bộ Doanh nghiệp")

# Nhập API key (trong thực tế, lưu trong .env)
openai_api_key = st.text_input("Nhập OpenAI API Key", type="password")

# Tải file
uploaded_file = st.file_uploader("Tải lên tài liệu (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file and openai_api_key:
    # Lưu file tạm thời
    os.makedirs("app/static/uploads", exist_ok=True)
    file_path = f"app/static/uploads/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Gửi file tới API
    with open(file_path, "rb") as f:
        files = {"file": (uploaded_file.name, f)}
        response = requests.post(
            "http://localhost:8000/api/v1/chatbot/upload", files=files
        )
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(response.json().get("detail", "Lỗi khi tải file"))

# Đặt câu hỏi
question = st.text_input("Đặt câu hỏi:")
if question and openai_api_key:
    response = requests.post(
        "http://localhost:8000/api/v1/chatbot/ask", json={"question": question}
    )
    if response.status_code == 200:
        result = response.json()
        st.write("**Trả lời**: ", result["answer"])
        st.write("**Nguồn**: ", result["sources"])
    else:
        st.error("Lỗi khi đặt câu hỏi")
