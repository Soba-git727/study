import sys
import os
import cv2
import webbrowser
import tkinter as tk
from tkinter import messagebox, simpledialog
from deepface import DeepFace
import time
import numpy as np

# =====================================================================
# PHƯƠNG ÁN CHỐNG XUNG ĐỘT KHI CHẠY ẨN CONSOLE TRÊN WINDOWS
# =====================================================================
if sys.platform == "win32" and getattr(sys, 'frozen', False):
    # Ép hệ thống chuyển hướng toàn bộ luồng log hệ thống vào hố đen (devnull)
    # Tránh việc TensorFlow/OpenCV ghi đè gây crash ứng dụng khi ẩn console.
    f = open(os.devnull, 'w')
    sys.stdout = f
    sys.stderr = f
    
    import ctypes
    ctypes.windll.kernel32.SetStdHandle(-11, None) # Ép luồng STDOUT ngầm
    ctypes.windll.kernel32.SetStdHandle(-12, None) # Ép luồng STDERR ngầm



# =====================================================================
# CẤU HÌNH ĐƯỜNG DẪN TUYỆT ĐỐI (ĐỒNG BỘ CHO CẢ FILE .PY VÀ .EXE)
# =====================================================================
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "face_database_VGGFace")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Ngưỡng nhận diện chuẩn cho VGG-Face
FACE_THRESHOLD = 0.28

# =====================================================================
# KHÂU 1: ĐĂNG KÝ TÀI KHOẢN (LỌC DIỆN TÍCH MẶT CHUẨN - CHỐNG RÁC DATABASE)
# =====================================================================
def xu_ly_dang_ky():
    name = simpledialog.askstring("Đăng ký tài khoản", "Nhập tên của bạn:", parent=root)
    if not name or not name.strip():
        messagebox.showerror("Lỗi", "Tên không hợp lệ!")
        return
    name = name.strip()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    messagebox.showinfo("Hướng dẫn", "Nhìn thẳng camera. Khi khung HIỆN MÀU XANH LÁ, nhấn 'S' để lưu.")
    
    prev_frame_time = 0

    while True:
        ret, frame = cap.read()
        if not ret: break

        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if (new_frame_time - prev_frame_time) > 0 else 0
        prev_frame_time = new_frame_time

        box_color = (0, 0, 255) # Mặc định màu đỏ (Chưa đạt yêu cầu)
        ready_to_save = False
        status_text = "Scanning... (Keep Face Clear)"

        try:
            # Dùng YuNet trích xuất nhanh vị trí mặt để vẽ khung mượt mà khi đăng ký
            faces = DeepFace.extract_faces(img_path=frame, detector_backend='yunet', enforce_detection=True)
            if len(faces) == 1:
                # Lấy độ tin cậy nhận diện toàn diện khuôn mặt (từ 0.0 đến 1.0)
                confidence = faces[0].get('confidence', 0.0)
                box = faces[0]['facial_area']
                x, y, w, h = box['x'], box['y'], box['w'], box['h']
                
                # Điều kiện lọc nghiêm ngặt: Phải nhìn rõ trọn vẹn khuôn mặt (> 90%)
                if confidence > 0.90:
                    box_color = (0, 255, 0) # Xanh lá cây thông báo hợp lệ
                    ready_to_save = True
                    status_text = "FACE DETECTED - Press 'S' to Save"
                else:
                    # Nếu quét lệch hoặc chỉ thấy nửa mặt
                    status_text = "Partial Face - Center your face fully"
                
                # Vẽ khung bám theo mặt trực tiếp
                cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
                # Hiển thị chữ trạng thái bám sát ngay trên thanh khung vuông
                cv2.putText(frame, status_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
        except Exception:
            pass
        
        # Nếu camera trống hoàn toàn, in chữ cảnh báo ở góc trái màn hình
        if not ready_to_save and 'x' not in locals():
            cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        cv2.putText(frame, f"FPS: {int(fps)}", (frame.shape[1] - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.imshow("Dang ky", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') or key == ord('S'):
            if ready_to_save:
                img_path = os.path.join(DATA_DIR, f"{name}.jpg")
                cv2.imwrite(img_path, frame)
                
                pkl_path = os.path.join(DATA_DIR, "representations_vgg_face.pkl")
                if os.path.exists(pkl_path):
                    try: os.remove(pkl_path)
                    except: pass
                    
                cv2.destroyWindow("Dang ky")
                messagebox.showinfo("Thành công", f"Đã lưu tài khoản: {name}")
                break
        elif key == ord('q') or key == ord('Q'):
            cv2.destroyWindow("Dang ky")
            break

    cap.release()

# =====================================================================
# KHÂU 2: ĐĂNG NHẬP XÁC THỰC (TÁCH BIỆT LUỒNG KHUNG & ĐỊNH DANH)
# =====================================================================
def xu_ly_dang_nhap():
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        messagebox.showwarning("Cảnh báo", "Cơ sở dữ liệu trống!")
        return

    pkl_path = os.path.join(DATA_DIR, "representations_vgg_face.pkl")
    if os.path.exists(pkl_path):
        try: os.remove(pkl_path)
        except: pass

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) 
    
    login_success = False
    prev_frame_time = 0
    
    last_recognition_time = 0
    recognition_interval = 0.4  # Chu kỳ chạy ngầm tác vụ quét dữ liệu VGG-Face
    
    # Bộ biến lưu trạng thái nhận diện xử lý ngầm
    ai_similarity = 0.0
    ai_name = "Unknown"
    ai_distance = 99.0
    is_matched = False

    while True:
        ret, frame = cap.read()
        if not ret: break

        current_time = time.time()
        fps = 1 / (current_time - prev_frame_time) if (current_time - prev_frame_time) > 0 else 0
        prev_frame_time = current_time

        # LUỒNG 1: TRÍCH XUẤT TỌA ĐỘ REAL-TIME (Chạy liên tục 30 FPS để chống giật khung)
        live_box = None
        face_valid_for_login = False
        try:
            faces = DeepFace.extract_faces(img_path=frame, detector_backend='yunet', enforce_detection=True)
            if len(faces) == 1:
                live_box = faces[0]['facial_area']
                # Lọc góc cạnh tối thiểu khi đăng nhập phải đạt hơn 75% diện tích mặt
                if faces[0].get('confidence', 0.0) > 0.75:
                    face_valid_for_login = True
        except:
            pass

        # LUỒNG 2: BẮN TIẾN TRÌNH NHẬN DIỆN CHẠY NGẦM THEO CHU KỲ (Chỉ trích xuất khi thấy rõ mặt)
        if face_valid_for_login and (current_time - last_recognition_time > recognition_interval):
            last_recognition_time = current_time
            try:
                dfs = DeepFace.find(
                    img_path=frame, 
                    db_path=str(DATA_DIR), 
                    model_name="VGG-Face", 
                    detector_backend='yunet', 
                    enforce_detection=True
                )
                
                if len(dfs) > 0 and not dfs[0].empty:
                    ai_distance = dfs[0]['distance'].iloc[0]
                    identity = dfs[0]['identity'].iloc[0]
                    ai_name = os.path.splitext(os.path.basename(identity))[0]
                    
                    if ai_distance < FACE_THRESHOLD:
                        ai_similarity = 85.0 + ((FACE_THRESHOLD - ai_distance) / FACE_THRESHOLD) * 15.0
                        is_matched = True
                    else:
                        ai_similarity = max(0.0, min(100.0, (1.0 - (ai_distance / 0.65)) * 85.0))
                        is_matched = False
                else:
                    ai_distance = 99.0
                    ai_similarity = 0.0
                    ai_name = "Unknown"
                    is_matched = False
            except Exception:
                pass
        elif not face_valid_for_login:
            # Nếu người dùng né mặt ra xa hoặc che mặt, reset trạng thái phân tích ngay lập tức
            is_matched = False
            ai_similarity = 0.0

        # LUỒNG 3: ÁP THÔNG TIN VÀ VẼ LÊN GIAO DIỆN HIỂN THỊ
        if live_box is not None:
            x, y, w, h = live_box['x'], live_box['y'], live_box['w'], live_box['h']
            
            if is_matched:
                # ĐĂNG NHẬP KHỚP: Khung xanh lá real-time bám sát khuôn mặt
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                text_success = f"FACE MATCHED: {ai_similarity:.1f}% | User: {ai_name}"
                cv2.putText(frame, text_success, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Hiện thông số FPS chốt và đóng băng màn hình 1.5 giây
                cv2.putText(frame, f"FPS: {int(fps)}", (frame.shape[1] - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.imshow("Dang nhap", frame)
                cv2.waitKey(1500)
                
                cap.release()
                cv2.destroyWindow("Dang nhap")
                
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                login_success = True
                break
            else:
                # ĐANG QUÉT HOẶC KHÔNG KHỚP: Khung đỏ bám mịn theo mặt di chuyển
                display_text = f"Analyzing: {ai_similarity:.1f}%" if face_valid_for_login else "Keep face fully inside frame"
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, display_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Luôn duy trì bộ đếm FPS thực tế góc phải màn hình
        cv2.putText(frame, f"FPS: {int(fps)}", (frame.shape[1] - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow("Dang nhap", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow("Dang nhap")
            break

    if not login_success:
        cap.release()

# =====================================================================
# GIAO DIỆN CHÍNH (GUI)
# =====================================================================
root = tk.Tk()
root.title("Hệ Thống Bảo Mật")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="#111d27")

label_title = tk.Label(root, text="XÁC THỰC KHUÔN MẶT", font=("Helvetica", 13, "bold"), fg="#e1e7ed", bg="#111d27")
label_title.pack(pady=25)

btn_register = tk.Button(root, text="1. Đăng ký tài khoản", width=28, height=2, font=("Helvetica", 10, "bold"), bg="#1b4965", fg="white", command=xu_ly_dang_ky)
btn_register.pack(pady=10)

btn_login = tk.Button(root, text="2. Đăng nhập hệ thống", width=28, height=2, font=("Helvetica", 10, "bold"), bg="#bc3908", fg="white", command=xu_ly_dang_nhap)
btn_login.pack(pady=10)

# ---------------------------------------------------------------------
# CƠ CHẾ MỒI NGẦM THÔNG MINH
# ---------------------------------------------------------------------
def warm_up_models():
    # Tạo cấu trúc ảnh nhiễu ngẫu nhiên giả lập camera thực để kích hoạt driver chuẩn chỉ trên EXE
    fake_img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    try:
        DeepFace.extract_faces(img_path=fake_img, detector_backend='yunet', enforce_detection=False)
        if os.path.exists(DATA_DIR) and os.listdir(DATA_DIR):
            DeepFace.find(img_path=fake_img, db_path=str(DATA_DIR), model_name="VGG-Face", detector_backend='yunet', enforce_detection=False)
    except:
        pass

# Gọi hàm mồi ngầm chạy sau khi GUI hiển thị được 100ms
root.after(100, warm_up_models)

root.mainloop()