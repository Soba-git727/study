import tkinter as tk
from tkinter import ttk, messagebox

def tinh_tien():
    try:
        # Lấy dữ liệu
        nhom = combo_nhom.get()
        gio = var_gio.get()
        kw = float(entry_kw.get())
        
        if kw < 0:
            messagebox.showerror("Lỗi", "Số kWh không được âm!")
            return

        # Bảng giá tương ứng với lựa chọn
        # 1.1, 1.2, 1.3, 1.4 theo đề bài
        gia_map = {
            "Cấp 110 kV trở lên": {'binh_thuong': 1649, 'thap_diem': 1044, 'cao_diem': 2973},
            "Cấp 22kV - 110kV": {'binh_thuong': 1669, 'thap_diem': 1084, 'cao_diem': 3093},
            "Cấp 6kV - 22kV": {'binh_thuong': 1729, 'thap_diem': 1124, 'cao_diem': 3194},
            "Cấp dưới 6kV": {'binh_thuong': 1809, 'thap_diem': 1184, 'cao_diem': 3314}
        }
        
        don_gia = gia_map[nhom][gio]
        thanh_tien = kw * don_gia
        vat = thanh_tien * 0.1
        tong = thanh_tien + vat

        # Hiển thị kết quả
        lbl_don_gia.config(text=f"Đơn giá: {don_gia:,} VND/kWh")
        lbl_thanh_tien.config(text=f"Thành tiền: {thanh_tien:,.1f} VND")
        lbl_vat.config(text=f"Thuế VAT (10%): {vat:,.1f} VND")
        lbl_tong.config(text=f"TỔNG CỘNG: {tong:,.1f} VND")

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số kWh hợp lệ!")

# Cấu hình giao diện
root = tk.Tk()
root.title("App Tính Tiền Điện - Hải Đăng")
root.geometry("400x550")

# Tiêu đề
tk.Label(root, text="HỆ THỐNG TÍNH TIỀN ĐIỆN", font=("Arial", 16, "bold")).pack(pady=10)

# Khung đối tượng
frame_nhom = tk.LabelFrame(root, text="1. Đối tượng khách hàng")
frame_nhom.pack(fill="x", padx=10, pady=5)
combo_nhom = ttk.Combobox(frame_nhom, values=["Cấp 110 kV trở lên", "Cấp 22kV - 110kV", "Cấp 6kV - 22kV", "Cấp dưới 6kV"])
combo_nhom.current(0)
combo_nhom.pack(fill="x", padx=5, pady=5)

# Khung giờ
frame_gio = tk.LabelFrame(root, text="2. Khung giờ sử dụng")
frame_gio.pack(fill="x", padx=10, pady=5)
var_gio = tk.StringVar(value="binh_thuong")
ttk.Radiobutton(frame_gio, text="Bình thường", variable=var_gio, value="binh_thuong").pack(side="left", padx=10)
ttk.Radiobutton(frame_gio, text="Cao điểm", variable=var_gio, value="cao_diem").pack(side="left", padx=10)
ttk.Radiobutton(frame_gio, text="Thấp điểm", variable=var_gio, value="thap_diem").pack(side="left", padx=10)

# Nhập số điện
tk.Label(root, text="Nhập số điện tiêu thụ (kWh):").pack(pady=5)
entry_kw = tk.Entry(root)
entry_kw.pack(pady=5)

# Nút tính
tk.Button(root, text="TÍNH TIỀN ĐIỆN", bg="green", fg="white", font=("Arial", 10, "bold"), command=tinh_tien).pack(fill="x", padx=10, pady=15)

# Kết quả
frame_kq = tk.LabelFrame(root, text="Kết quả thanh toán")
frame_kq.pack(fill="both", padx=10, pady=5, expand=True)

lbl_don_gia = tk.Label(frame_kq, text="Đơn giá: 0 VND/kWh")
lbl_don_gia.pack(anchor="w", padx=5)
lbl_thanh_tien = tk.Label(frame_kq, text="Thành tiền: 0 VND")
lbl_thanh_tien.pack(anchor="w", padx=5)
lbl_vat = tk.Label(frame_kq, text="Thuế VAT (10%): 0 VND")
lbl_vat.pack(anchor="w", padx=5)
lbl_tong = tk.Label(frame_kq, text="TỔNG CỘNG: 0 VND", fg="red", font=("Arial", 10, "bold"))
lbl_tong.pack(anchor="w", padx=5)

# Footer
tk.Label(root, text="Sản phẩm được tạo bởi Hải Đăng", font=("Arial", 8, "italic")).pack(side="bottom", pady=10)

root.mainloop()