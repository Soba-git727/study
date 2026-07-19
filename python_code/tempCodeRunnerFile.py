import cv2
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox, simpledialog
from deepface import DeepFace

# =====================================================================
# CẤU HÌNH ĐƯỜNG DẪN CƠ SỞ DỮ LIỆU
# =====================================================================
DATA_DIR = "face_database_facenet"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Tắt bớt log không cần thiết của TensorFlow để Terminal sạch sẽ
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# =====================================================================
# LOGIC XỬ LÝ AI VỚI FACENET (ĐÃ FIX LỖI ĐĂNG KÝ)
# =====================================================================
def xu_ly_dang_ky():
    name = simpledialog.askstring("Đăng ký tài khoản", "Nhập tên của bạn:", parent=root)
    if not name or not name.strip():
        messagebox.showerror("Lỗi", "Tên không hợp lệ!")
        return
    name = name.strip()

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Hướng dẫn", "Hãy nhìn thẳng vào camera và nhấn 'S' để hệ thống quét và lưu khuôn mặt.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Vẽ một khung vuông gợi ý ở giữa màn hình để người dùng căn mặt vào cho chuẩn
        h, w, _ = frame.shape
        cv2.rectangle(frame, (int(w/2)-120, int(h/2)-120), (int(w/2)+120, int(h/2)+120), (255, 255, 0), 1)

        cv2.putText(frame, "Nhan 'S' de quet mat | Nhan 'Q' de thoat", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Chup anh dang ky - FaceNet", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') or key == ord('S'):
            try:
                # Trích xuất thử khuôn mặt từ frame xem có mặt người không
                # Sử dụng detector mặc định 'opencv' cực nhẹ để kiểm tra nhanh
                faces = DeepFace.extract_faces(img_path=frame, detector_backend='opencv', enforce_detection=True)
                
                if len(faces) == 1:
                    img_path = os.path.join(DATA_DIR, f"{name}.jpg")
                    # Lưu nguyên frame (hoặc ảnh đã xác thực có mặt) vào DB
                    cv2.imwrite(img_path, frame)
                    messagebox.showinfo("Thành công", f"🎉 AI đã nhận diện và lưu khuôn mặt mẫu thành công cho [{name}]!")
                    break
                else:
                    messagebox.showwarning("Cảnh báo", "Phát hiện quá nhiều khuôn mặt trong khung hình. Vui lòng chỉ quét 1 người!")
            except Exception:
                # Nếu không tìm thấy mặt, DeepFace sẽ throw exception vì enforce_detection=True
                messagebox.showerror("Lỗi nhận diện", "❌ AI không tìm thấy khuôn mặt nào! Hãy nhìn thẳng vào camera, giữ mặt rõ nét và bấm 'S' lại.")
                
        elif key == ord('q') or key == ord('Q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def xu_ly_dang_nhap():
    if not os.listdir(DATA_DIR):
        messagebox.showwarning("Cảnh báo", "Cơ sở dữ liệu trống! Vui lòng đăng ký trước.")
        return

    cap = cv2.VideoCapture(0)
    rickroll_triggered = False

    while True:
        ret, frame = cap.read()
        if not ret: break

        current_name = "Unknown"
        color = (0, 0, 255)

        if not rickroll_triggered:
            try:
                # Quét và so khớp bằng model Facenet chuyên dụng
                dfs = DeepFace.find(img_path=frame, db_path=DATA_DIR, model_name="Facenet", enforce_detection=False)
                
                if len(dfs) > 0 and not dfs[0].empty:
                    identity = dfs[0]['identity'].iloc[0]
                    file_name = os.path.basename(identity)
                    current_name = os.path.splitext(file_name)[0]
                    color = (0, 255, 0)
                    
                    x = int(dfs[0]['source_x'].iloc[0])
                    y = int(dfs[0]['source_y'].iloc[0])
                    w = int(dfs[0]['source_w'].iloc[0])
                    h = int(dfs[0]['source_h'].iloc[0])
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    
                    cv2.putText(frame, f"Kich hoat: {current_name}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    cv2.imshow("Xac thuc FaceNet AI", frame)
                    cv2.waitKey(1000)
                    
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    rickroll_triggered = True
                    break
            except Exception:
                pass

        cv2.putText(frame, f"User: {current_name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.imshow("Xac thuc FaceNet AI", frame)

        if rickroll_triggered or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()

# =====================================================================
# GIAO DIỆN CỬA SỔ ĐỒ HỌA (GUI)
# =====================================================================
root = tk.Tk()
root.title("Hệ Thống Bảo Mật FaceNet Pro")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="#111d27")

label_title = tk.Label(root, text="XÁC THỰC AI KHUÔN MẶT FACENET", 
                       font=("Helvetica", 13, "bold"), fg="#e1e7ed", bg="#111d27")
label_title.pack(pady=25)

btn_register = tk.Button(root, text="1. Đăng ký tài khoản (FaceNet)", width=28, height=2,
                         font=("Helvetica", 10, "bold"), bg="#1b4965", fg="white", 
                         activebackground="#13354c", command=xu_ly_dang_ky)
btn_register.pack(pady=10)

btn_login = tk.Button(root, text="2. Đăng nhập (Mở Rickroll)", width=28, height=2,
                      font=("Helvetica", 10, "bold"), bg="#bc3908", fg="white", 
                      activebackground="#942d06", command=xu_ly_dang_nhap)
btn_login.pack(pady=10)

root.mainloop()
