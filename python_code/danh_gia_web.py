import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import os
from PIL import Image, ImageTk
import google.generativeai as genai

# =====================================================================
# CẤU HÌNH TIÊU CHÍ ĐÁNH GIÁ (AI sẽ dựa vào đây để chấm điểm)
# =====================================================================
PROMPT_DANH_GIA = """
Bạn là một chuyên gia UI/UX Senior xuất sắc. Hãy phân tích hình ảnh hoặc video về giao diện trang web được cung cấp dưới đây.
Hãy chấm điểm theo thang điểm 10 và đánh giá chi tiết theo đúng 7 tiêu chí sau:

1. Bố cục & Sự căn chỉnh (Layout & Alignment)
2. Phối màu & Độ tương phản (Color Palette & Contrast)
3. Hệ thống phân cấp trực quan (Visual Hierarchy)
4. Kiểu chữ & Khả năng đọc (Typography & Readability)
5. Khả năng điều hướng & Usability (Navigation & Usability)
6. Tính thẩm mỹ & Xu hướng hiện đại (Aesthetics & Modern Trend)
7. Mật độ thông tin & Độ gọn gàng (Information Density & Cleanliness)

YÊU CẦU ĐẦU RA:
- Nhận xét ưu điểm và nhược điểm cho từng tiêu chí.
- Cho điểm từ 1 đến 10 cho từng tiêu chí.
- Cuối cùng, đưa ra ĐIỂM TRUNG BÌNH CHUNG (thang điểm 10) và lời khuyên quan trọng nhất để cải thiện giao diện này.
- Trả lời hoàn toàn bằng tiếng Việt, trình bày chuyên nghiệp, rõ ràng, dễ đọc.
"""

class WebEvaluatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Đánh Giá Giao Diện Web AI - Hải Đăng Nhóm 11")
        self.root.geometry("680x600")
        self.root.configure(bg="#f4f6f9")
        
        self.selected_file_path = ""
        self.is_analyzing = False
        
        self.setup_ui()

    def setup_ui(self):
        # Tiêu đề chính
        tk.Label(
            self.root, 
            text="ĐÁNH GIÁ GIAO DIỆN WEBSITE BẰNG AI", 
            font=("Arial", 15, "bold"), 
            fg="#1e3a8a", 
            bg="#f4f6f9"
        ).pack(pady=15)

        # Khung cấu hình API Key
        frame_api = tk.LabelFrame(self.root, text=" Cấu hình Gemini API Key ", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#333")
        frame_api.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame_api, text="Nhập API Key:", font=("Arial", 9), bg="#f4f6f9").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_api = tk.Entry(frame_api, font=("Arial", 10), width=50, show="*")
        self.entry_api.grid(row=0, column=1, padx=10, pady=10)
        
        # Mẹo lấy key
        lbl_hint = tk.Label(frame_api, text="* Lấy key miễn phí tại: aistudio.google.com", font=("Arial", 8, "italic"), fg="#2563eb", bg="#f4f6f9", cursor="hand2")
        lbl_hint.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 5))

        # Khung chọn tệp
        frame_file = tk.LabelFrame(self.root, text=" Tải lên Ảnh hoặc Video giao diện ", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#333")
        frame_file.pack(fill="x", padx=20, pady=10)

        self.btn_select = tk.Button(
            frame_file, text="Chọn tệp (Ảnh/Video)", bg="#2563eb", fg="white", 
            font=("Arial", 10, "bold"), command=self.chon_tep, cursor="hand2"
        )
        self.btn_select.pack(side="left", padx=15, pady=15)

        self.lbl_file_status = tk.Label(
            frame_file, text="Chưa chọn tệp nào (Hỗ trợ: png, jpg, mp4, avi, mov...)", 
            font=("Arial", 9, "italic"), fg="#555", bg="#f4f6f9", wraplength=400, justify="left"
        )
        self.lbl_file_status.pack(side="left", padx=10, fill="x", expand=True)

        # Nút bấm Phân tích
        self.btn_analyze = tk.Button(
            self.root, text="BẮT ĐẦU PHÂN TÍCH & CHẤM ĐIỂM", bg="#10b981", fg="white",
            font=("Arial", 11, "bold"), height=2, command=self.start_analysis_thread, cursor="hand2"
        )
        self.btn_analyze.pack(fill="x", padx=20, pady=10)

        # Khung kết quả đánh giá
        frame_result = tk.LabelFrame(self.root, text=" Kết quả đánh giá từ Chuyên gia AI ", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#333")
        frame_result.pack(fill="both", expand=True, padx=20, pady=10)

        self.txt_result = scrolledtext.ScrolledText(frame_result, font=("Segoe UI", 10), state="disabled", bg="#ffffff")
        self.txt_result.pack(fill="both", expand=True, padx=5, pady=5)

    def chon_tep(self):
        file_types = [
            ("Tệp đa phương tiện", "*.png *.jpg *.jpeg *.mp4 *.avi *.mov *.mkv"),
            ("Hình ảnh", "*.png *.jpg *.jpeg"),
            ("Video", "*.mp4 *.avi *.mov *.mkv")
        ]
        path = filedialog.askopenfilename(title="Chọn ảnh hoặc video giao diện web", filetypes=file_types)
        if path:
            self.selected_file_path = path
            filename = os.path.basename(path)
            self.lbl_file_status.config(text=f"Đã chọn: {filename}", fg="#059669")

    def log_result(self, text):
        self.txt_result.config(state="normal")
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, text)
        self.txt_result.config(state="disabled")

    def start_analysis_thread(self):
        api_key = self.entry_api.get().strip()
        if not api_key:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Gemini API Key của bạn!")
            return
        if not self.selected_file_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải lên hình ảnh hoặc video giao diện web trước!")
            return
        
        if self.is_analyzing:
            return

        self.is_analyzing = True
        self.btn_analyze.config(state="disabled", text="HỆ THỐNG ĐANG PHÂN TÍCH (Vui lòng đợi)...", bg="#9ca3af")
        self.log_result("Đang kết nối tới AI và tải tệp lên để xử lý...\n(Nếu là video, quá trình này có thể mất từ 1 - 2 phút tùy dung lượng tệp)")
        
        # Chạy ngầm tránh đơ UI
        t = threading.Thread(target=self.process_evaluation, args=(api_key,), daemon=True)
        t.start()

    def process_evaluation(self, api_key):
        try:
            # Cấu hình AI
            genai.configure(api_key=api_key)
            
            file_extension = os.path.splitext(self.selected_file_path)[1].lower()
            
            # Khởi tạo model thích hợp cho tác vụ multimodal
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            if file_extension in ['.mp4', '.avi', '.mov', '.mkv']:
                # Nếu là video, sử dụng File API của Google để tải lên trước
                self.log_result("Đang tải video lên bộ nhớ tạm của Google Cloud...")
                uploaded_file = genai.upload_file(path=self.selected_file_path)
                
                self.log_result("Tải lên thành công! Đang chờ AI xử lý và phân tích video giao diện...")
                
                # Đợi cho file video được xử lý xong trên Cloud
                import time
                while uploaded_file.state.name == "PROCESSING":
                    time.sleep(5)
                    uploaded_file = genai.get_file(uploaded_file.name)
                
                if uploaded_file.state.name == "FAILED":
                    raise Exception("Quá trình xử lý video trên máy chủ AI thất bại.")

                response = model.generate_content([uploaded_file, PROMPT_DANH_GIA])
                
                # Dọn dẹp tệp tạm trên cloud sau khi dùng xong
                genai.delete_file(uploaded_file.name)
            else:
                # Nếu là ảnh, mở trực tiếp bằng PIL và gửi đi luôn
                img = Image.open(self.selected_file_path)
                response = model.generate_content([img, PROMPT_DANH_GIA])

            self.log_result(response.text)

        except Exception as e:
            self.log_result(f"Đã xảy ra lỗi trong quá trình phân tích:\n{str(e)}")
            messagebox.showerror("Lỗi hệ thống", f"Không thể hoàn thành đánh giá. Chi tiết: {e}")
        finally:
            self.is_analyzing = False
            self.btn_analyze.config(state="normal", text="BẮT ĐẦU PHÂN TÍCH & CHẤM ĐIỂM", bg="#10b981")

# --- Khởi chạy ứng dụng ---
if __name__ == "__main__":
    root = tk.Tk()
    app = WebEvaluatorApp(root)
    root.mainloop()