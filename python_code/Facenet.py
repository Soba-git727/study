import cv2
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox, simpledialog
from deepface import DeepFace
import time

# =====================================================================
# CẤU HÌNH ĐƯỜNG DẪN CƠ SỞ DỮ LIỆU
# =====================================================================
DATA_DIR = "face_database_facenet"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Ẩn hoàn toàn các dòng cảnh báo log thừa của TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# =====================================================================
# KHÂU 1: ĐĂNG KÝ TÀI KHOẢN (DEEPFACE REAL-TIME TRACKING)
# =====================================================================
def xu_ly_dang_ky():
    name = simpledialog.askstring("Đăng ký tài khoản", "Nhập tên của bạn:", parent=root)
    if not name or not name.strip():
        messagebox.showerror("Lỗi", "Tên không hợp lệ!")
        return
    name = name.strip()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    messagebox.showinfo("Hướng dẫn đăng ký", "Hãy nhìn thẳng camera laptop.\nKhi khung vuông HIỆN MÀU XANH LÁ, nhấn 'S' để lưu.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        box_color = (0, 0, 255) 
        ready_to_save = False
        text_status = "Kiem tra: Chua tim thay mat..."

        try:
            faces = DeepFace.extract_faces(img_path=frame, detector_backend='yunet', enforce_detection=True)
            if len(faces) == 1:
                box_color = (0, 255, 0) 
                ready_to_save = True
                text_status = "San sang! Nhan 'S' de luu"
                
                box = faces[0]['facial_area']
                x, y, w, h = box['x'], box['y'], box['w'], box['h']
                cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
        except Exception:
            pass

        cv2.putText(frame, text_status, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)
        cv2.putText(frame, "Nhan 'Q' de thoat", (15, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow("Dang ky - DeepFace Realtime", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') or key == ord('S'):
            if ready_to_save:
                img_path = os.path.join(DATA_DIR, f"{name}.jpg")
                cv2.imwrite(img_path, frame)
                cv2.destroyWindow("Dang ky - DeepFace Realtime")
                messagebox.showinfo("Thành công", f"🎉 Đã lưu tài khoản khuôn mặt cho [{name}]!")
                break
        elif key == ord('q') or key == ord('Q'):
            cv2.destroyWindow("Dang ky - DeepFace Realtime")
            break

    cap.release()

# =====================================================================
# KHÂU 2: ĐĂNG NHẬP XÁC THỰC (BẤT NGỜ CÚ RICKROLL)
# =====================================================================
def xu_ly_dang_nhap():
    if not os.listdir(DATA_DIR):
        messagebox.showwarning("Cảnh báo", "Cơ sở dữ liệu trống! Vui lòng đăng ký trước.")
        return

    # Dọn dẹp cache cũ
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pkl"):
            try: os.remove(os.path.join(DATA_DIR, file))
            except: pass

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    login_success = False

    while True:
        ret, frame = cap.read()
        if not ret: break

        current_name = "Nguoi dung an danh"
        box_color = (0, 0, 255) 

        try:
            dfs = DeepFace.find(img_path=frame, db_path=DATA_DIR, model_name="Facenet", detector_backend='yunet', enforce_detection=True)
            
            if len(dfs) > 0 and not dfs[0].empty:
                distance = dfs[0]['distance'].iloc[0]
                
                # Khớp khuôn mặt thành công
                if distance < 0.20:
                    identity = dfs[0]['identity'].iloc[0]
                    file_name = os.path.basename(identity)
                    current_name = os.path.splitext(file_name)[0]
                    box_color = (0, 255, 0) 
                    
                    x = int(dfs[0]['source_x'].iloc[0])
                    y = int(dfs[0]['source_y'].iloc[0])
                    w = int(dfs[0]['source_w'].iloc[0])
                    h = int(dfs[0]['source_h'].iloc[0])
                    
                    # Hiện thông tin ngụy trang để tạo bất ngờ
                    cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
                    cv2.putText(frame, f"User: {current_name}", (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)
                    cv2.putText(frame, "Dang dong bo du lieu...", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                    
                    cv2.imshow("He thong xac thuc", frame)
                    cv2.waitKey(800) # Giữ khung hình ngụy trang 0.8 giây để tạo đà
                    
                    # Giải phóng camera ngay lập tức
                    cv2.destroyWindow("He thong xac thuc")
                    cap.release()
                    
                    # BẬT NỀN BẤT NGỜ: Mở thẳng trình duyệt web bài Rickroll
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    login_success = True
                    break
        except Exception:
            pass

        # Giao diện quét thời gian thực khi chưa khớp danh tính
        if not login_success:
            try:
                faces = DeepFace.extract_faces(img_path=frame, detector_backend='yunet', enforce_detection=True)
                if len(faces) == 1:
                    box = faces[0]['facial_area']
                    cv2.rectangle(frame, (box['x'], box['y']), (box['x']+box['w'], box['y']+box['h']), (0, 0, 255), 2)
            except:
                pass
                
            cv2.putText(frame, "He thong: Dang quet khuon mat...", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.imshow("He thong xac thuc", frame)

        if login_success or (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyWindow("He thong xac thuc")
            break

    if not login_success:
        cap.release()

# =====================================================================
# CỬA SỔ GIAO DIỆN CHÍNH (GUI)
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

btn_login = tk.Button(root, text="2. Đăng nhập hệ thống", width=28, height=2,
                      font=("Helvetica", 10, "bold"), bg="#bc3908", fg="white", 
                      activebackground="#942d06", command=xu_ly_dang_nhap)
btn_login.pack(pady=10)

root.mainloop()