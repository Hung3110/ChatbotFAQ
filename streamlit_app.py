# streamlit_app.py
import streamlit as st
import requests  # Thư viện để gửi HTTP request đến backend FastAPI
import os
from datetime import datetime

# Cấu hình cơ bản cho trang Streamlit
st.set_page_config(page_title="Chatbot FAQ", page_icon="🤖", layout="wide")

# Nhúng CSS tùy chỉnh để giao diện đẹp hơn
st.markdown("""
<style>
/* ... (giữ nguyên CSS) ... */
</style>
""", unsafe_allow_html=True)


# --- Khởi tạo Session State ---
# Session State dùng để lưu trữ trạng thái của ứng dụng giữa các lần re-run (tương tác của người dùng)
if "google_api_key" not in st.session_state:
    st.session_state.google_api_key = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Lưu lịch sử chat của session hiện tại
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = [] # Lưu danh sách tên các file đã upload
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None # File đang được chọn để chat

# --- Bố cục 3 cột ---
col1, col2, col3 = st.columns([3, 7, 3]) # Tỷ lệ chiều rộng các cột

# --- Cột trái: Quản lý tài liệu ---
with col1:
    st.header("Cấu hình", divider='rainbow')

    # Dùng expander để ẩn/hiện ô nhập API key
    with st.expander("Nhập Google API Key (nếu cần)"):
        google_api_key = st.text_input("Google API Key", value=st.session_state.google_api_key, type="password", label_visibility="collapsed")
        if google_api_key:
            st.session_state.google_api_key = google_api_key

    # Dùng st.form để nhóm các input và một nút bấm, tránh re-run không cần thiết
    with st.form("upload_form", clear_on_submit=True):
        st.subheader("1. Tải tài liệu")
        uploaded_file = st.file_uploader("Tải lên file PDF hoặc DOCX", type=["pdf", "docx"], label_visibility="collapsed")
        submitted = st.form_submit_button("Tải lên và xử lý")

    # Xử lý logic sau khi form được submit và có file
    if submitted and uploaded_file:
        with st.spinner("Đang xử lý tài liệu..."): # Hiển thị con quay chờ
            # Chuẩn bị để gọi API backend
            headers = {"google_api_key": st.session_state.google_api_key} if st.session_state.google_api_key else {}
            # Mở file và gửi request POST đến endpoint /upload
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post("http://localhost:8000/api/v1/chatbot/upload", files=files, headers=headers)

            if response.status_code == 200:
                st.success(f"Tải lên thành công: {uploaded_file.name}")
                # Cập nhật danh sách file đã upload
                if uploaded_file.name not in st.session_state.uploaded_files:
                    st.session_state.uploaded_files.append(uploaded_file.name)
                # Tự động chọn file vừa upload nếu chưa có file nào được chọn
                if not st.session_state.selected_file:
                     st.session_state.selected_file = uploaded_file.name
            else:
                st.error(f"Lỗi server: {response.text}")
        st.rerun() # Chạy lại script để cập nhật giao diện

    st.markdown("---")
    st.subheader("2. Chọn tài liệu để chat")
    if st.session_state.uploaded_files:
        # Hiển thị danh sách các file đã upload dưới dạng radio button
        selected_file = st.radio(
            "Danh sách tài liệu:",
            options=st.session_state.uploaded_files,
            index=st.session_state.uploaded_files.index(st.session_state.selected_file) if st.session_state.selected_file in st.session_state.uploaded_files else 0,
            key="file_selector",
            label_visibility="collapsed"
        )
        # Nếu người dùng chọn file khác, cập nhật state và xóa lịch sử chat cũ
        if st.session_state.selected_file != selected_file:
             st.session_state.selected_file = selected_file
             st.session_state.chat_history = []
             st.rerun()
    else:
        st.info("Chưa có tài liệu nào.")

# --- Cột giữa: Khung chat chính ---
with col2:
    st.title("🤖 Chatbot FAQ")
    if st.session_state.selected_file:
        st.caption(f"Đang chat với tài liệu: **{st.session_state.selected_file}**")

    # Vùng chứa để hiển thị các tin nhắn
    chat_container = st.container(height=600, border=False)
    with chat_container:
        for msg in st.session_state.chat_history:
            # Hiển thị tin nhắn của user hoặc bot với style khác nhau
            align = "user-msg" if msg["role"] == "user" else "bot-msg"
            st.markdown(f'<div class="{align}">{msg["content"]}<div class="time">{msg["time"]}</div></div>', unsafe_allow_html=True)

    # Ô nhập câu hỏi của người dùng
    question = st.chat_input("Hỏi về nội dung trong tài liệu...")
    if question:
        if not st.session_state.selected_file:
            st.error("Vui lòng tải lên và chọn một tài liệu để bắt đầu!")
        else:
            current_time = datetime.now().strftime("%H:%M:%S")
            # Thêm câu hỏi của user vào lịch sử chat để hiển thị ngay lập tức
            st.session_state.chat_history.append({"role": "user", "content": question, "time": current_time})

            # Gửi câu hỏi đến backend API /ask
            headers = {"google_api_key": st.session_state.google_api_key} if st.session_state.google_api_key else {}
            response = requests.post(
                "http://localhost:8000/api/v1/chatbot/ask",
                json={"question": question, "document_name": st.session_state.selected_file},
                headers=headers
            )
            if response.status_code == 200:
                answer = response.json()["answer"]
            else:
                answer = f"Lỗi: {response.json().get('detail', 'Không thể nhận câu trả lời từ server.')}"

            # Thêm câu trả lời của bot vào lịch sử chat
            st.session_state.chat_history.append({"role": "bot", "content": answer, "time": datetime.now().strftime("%H:%M:%S")})
            st.rerun() # Chạy lại script để hiển thị tin nhắn mới

# --- Cột phải: Lịch sử chat (hiển thị lại) ---
with col3:
    st.header("📜 Lịch sử", divider='rainbow')
    if st.button("Xóa lịch sử chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")

    if st.session_state.chat_history:
        # Hiển thị lịch sử chat theo thứ tự ngược (mới nhất ở trên)
        for msg in reversed(st.session_state.chat_history):
            align = "user-msg" if msg["role"] == "user" else "bot-msg"
            st.markdown(f'<div class="{align}">{msg["content"]}<div class="time">{msg["time"]}</div></div>', unsafe_allow_html=True)
    else:
        st.info("Chưa có nội dung trò chuyện.")