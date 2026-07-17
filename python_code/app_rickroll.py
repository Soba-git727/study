import cv2
import numpy as np
import os
import webbrowser
import urllib.request
import tkinter as tk
from tkinter import messagebox, simpledialog

# =====================================================================
# CẤU HÌNH FILE MẪU NHẬN DIỆN
# =====================================================================
CASCADE_FILE = "haarcascade_frontalface_default.xml"

if not os.path.exists(CASCADE_FILE):
    try:
        url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        urllib.request.urlretrieve(url, CASCADE_FILE)
    except Exception as e:
        pass

face_cascade = cv2.CascadeClassifier(CASCADE_FILE)
DATA_DIR = "face_data_opencv"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# =====================================================================
# LOGIC XỬ LÝ HÀM CHỨC NĂNG
# =====================================================================
def xu_ly_dang_ky():
    # Hiển thị pop-up nhập tên tài khoản
    name = simpledialog.askstring("Đăng ký", "Nhập tên tài khoản của bạn:", parent=root)
    if not name:
        return
    name = name.strip()
    if name == "":
        messagebox.showerror("Lỗi", "Tên không được để trống!")
        return

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Hướng dẫn", "Camera sẽ mở lên.\nHãy nhìn thẳng và nhấn phím 'S' trên bàn phím để chụp mặt.")

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Lỗi", "Không thể kết nối với Camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(frame, "Nhan 'S' de chup | Nhan 'Q' de thoat", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Dang ky tai khoan", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') or key == ord('S'):
            if len(faces) == 1:
                (x, y, w, h) = faces[0]
                face_crop = gray[y:y+h, x:x+w]
                face_resize = cv2.resize(face_crop, (200, 200))
                
                img_path = os.path.join(DATA_DIR, f"{name}.jpg")
                cv2.imwrite(img_path, face_resize)
                messagebox.showinfo("Thành công", f"🎉 Đăng ký thành công tài khoản: [{name}]")
                break
            elif len(faces) == 0:
                print("Không tìm thấy khuôn mặt.")
            else:
                print("Phát hiện quá nhiều khuôn mặt.")
        elif key == ord('q') or key == ord('Q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def xu_ly_dang_nhap():
    image_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.jpg')]
    if not image_files:
        messagebox.showwarning("Cảnh báo", "Cơ sở dữ liệu trống! Vui lòng Đăng ký trước.")
        return

    db_faces = {}
    for file_name in image_files:
        name = os.path.splitext(file_name)[0]
        img_path = os.path.join(DATA_DIR, file_name)
        db_faces[name] = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    cap = cv2.VideoCapture(0)
    rickroll_triggered = False

    while True:
        ret, frame = cap.read()
        if not ret: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        current_name = "Unknown"
        color = (0, 0, 255)

        for (x, y, w, h) in faces:
            face_crop = gray[y:y+h, x:x+w]
            face_resize = cv2.resize(face_crop, (200, 200))
            
            best_score = 0
            best_match = None

            for name, saved_face in db_faces.items():
                res = cv2.matchTemplate(face_resize, saved_face, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                
                if max_val > best_score and max_val > 0.45:
                    best_score = max_val
                    best_match = name

            if best_match:
                current_name = best_match
                color = (0, 255, 0)
                
                if not rickroll_triggered:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, f"Kich hoat: {current_name}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    cv2.imshow("Dang nhap he thong", frame)
                    cv2.waitKey(500)
                    
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    rickroll_triggered = True
                    break

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, current_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("Dang nhap he thong", frame)
        if rickroll_triggered or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()

# =====================================================================
# THIẾT KẾ GIAO DIỆN CỬA SỔ (GUI ĐỒ HỌA)
# =====================================================================
root = tk.Tk()
root.title("Hệ Thống Bảo Mật Biometric")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="#2c3e50")

# Tiêu đề app
label_title = tk.Label(root, text="HỆ THỐNG XÁC THỰC KHUÔN MẶT", 
                       font=("Helvetica", 14, "bold"), fg="#ecf0f1", bg="#2c3e50")
label_title.pack(pady=20)

# Nút Đăng ký
btn_register = tk.Button(root, text="1. Đăng ký tài khoản mới", width=25, height=2,
                         font=("Helvetica", 11), bg="#27ae60", fg="white", 
                         activebackground="#2ecc71", command=xu_ly_dang_ky)
btn_register.pack(pady=10)

# Nút Đăng nhập
btn_login = tk.Button(root, text="2. Đăng nhập (Mở Rickroll)", width=25, height=2,
                      font=("Helvetica", 11), bg="#2980b9", fg="white", 
                      activebackground="#3498db", command=xu_ly_dang_nhap)
btn_login.pack(pady=10)

root.mainloop()