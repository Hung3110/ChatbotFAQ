import google.generativeai as genai
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("LỖI: Không tìm thấy GOOGLE_API_KEY trong file .env của bạn.")
else:
    # Chỉ in ra 4 ký tự cuối của key để bảo mật
    print(f"Đang thử kết nối với API Key kết thúc bằng: ...{api_key[-4:]}")
    try:
        # Cấu hình API key
        genai.configure(api_key=api_key)
        print("Cấu hình API Key thành công!")

        # Thử lấy danh sách các model có sẵn
        print("Đang thử lấy danh sách models...")
        model_count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # print(m.name) # Bỏ comment dòng này nếu muốn xem tên các model
                model_count += 1

        print(f"Tìm thấy {model_count} models có thể sử dụng.")
        print("\n✅ KIỂM TRA THÀNH CÔNG! API Key và dự án của bạn hoạt động bình thường.")

    except Exception as e:
        print("\n❌ KIỂM TRA THẤT BẠI!")
        print("Lỗi chi tiết:", e)