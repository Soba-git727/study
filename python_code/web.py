import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

# 1. Cấu hình giao diện Web Bán Hàng Dangfood
st.set_page_config(page_title="Dangfood Order System - Nhóm 11", page_icon="🍔", layout="wide")

st.title("🍔 Dangfood - Hệ Thống Đặt Món Trực Tuyến")
st.markdown("### Sản phẩm được thực hiện bởi: **Hồ Hải Đăng - Nhóm 11**")
st.write("Chào mừng bạn đến với hệ thống menu thử nghiệm của Dangfood. Vui lòng chọn món ăn yêu thích bên dưới.")

# 2. Khởi tạo dữ liệu món ăn của Dangfood
if "menu_mon_an" not in st.session_state:
    st.session_state.menu_mon_an = [
        {
            "id": 1,
            "ten": "Bento Gà Chiên Karaage tổng hợp",
            "gia": 85000,
            "anh": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500",
            "mota": "Gà chiên giòn kiểu Nhật, kèm cơm trắng và salad."
        },
        {
            "id": 2,
            "ten": "Mỳ Ramen Xá Xíu Sốt Tương",
            "gia": 120000,
            "anh": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500",
            "mota": "Sợi mỳ tươi, thịt xá xíu đậm vị, nước dùng hầm xương 12 tiếng."
        },
        {
            "id": 3,
            "ten": "Combo Sushi Truyền Thống (12 cái)",
            "gia": 250000,
            "anh": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500",
            "mota": "Gồm sushi cá hồi, cá ngừ, tôm và bơ tươi."
        },
        {
            "id": 4,
            "ten": "Trà Sữa Matcha Trân Châu Đường Đen",
            "gia": 45000,
            "anh": "https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=500",
            "mota": "Matcha Uji nguyên chất kết hợp sữa tươi và trân châu dai giòn."
        }
    ]

# Khởi tạo giỏ hàng trống nếu chưa có
if "gio_hang" not in st.session_state:
    st.session_state.gio_hang = {}

# 3. Giao diện hiển thị Menu món ăn và Chọn số lượng
st.subheader("📋 Menu Món Ăn - Dangfood")

# Chia thành 2 cột: Cột trái hiển thị Menu, Cột phải hiển thị Giỏ hàng & Thanh toán
col_menu, col_gio_hang = st.columns([2, 1])

with col_menu:
    # Hiển thị danh sách món ăn dưới dạng lưới (Grid) 2 cột
    grid_cols = st.columns(2)
    for index, mon in enumerate(st.session_state.menu_mon_an):
        with grid_cols[index % 2]:
            st.image(mon["anh"], use_container_width=True)
            st.markdown(f"#### **{mon['ten']}**")
            st.caption(mon["mota"])
            st.markdown(f"💰 Giá bán: **{mon['gia']:,} VNĐ**")
            
            # Ô chọn số lượng và nút thêm vào giỏ
            so_luong = st.number_input(f"Số lượng ({mon['ten']})", min_value=1, max_value=20, value=1, key=f"sl_{mon['id']}")
            if st.button(f"🛒 Thêm vào giỏ", key=f"btn_{mon['id']}"):
                if mon['id'] in st.session_state.gio_hang:
                    st.session_state.gio_hang[mon['id']] += so_luong
                else:
                    st.session_state.gio_hang[mon['id']] = so_luong
                st.toast(f"Đã thêm {so_luong} x {mon['ten']} vào giỏ hàng Dangfood!")

with col_gio_hang:
    st.subheader("🛒 Giỏ Hàng Của Bạn")
    
    tong_tien = 0
    thong_tin_hoa_don = "HOA DON DANGFOOD SYSTEM\n"
    
    if not st.session_state.gio_hang:
        st.info("Giỏ hàng đang trống. Vui lòng chọn món!")
    else:
        # Hiển thị các món đã chọn trong giỏ hàng
        for mon_id, qty in list(st.session_state.gio_hang.items()):
            mon = next(m for m in st.session_state.menu_mon_an if m["id"] == mon_id)
            thanh_tien_mon = mon["gia"] * qty
            tong_tien += thanh_tien_mon
            
            st.markdown(f"**{mon['ten']}**")
            st.write(f"{qty} x {mon['gia']:,} = **{thanh_tien_mon:,} VNĐ**")
            
            # Nút xóa món khỏi giỏ hàng
            if st.button("❌ Xóa", key=f"del_{mon_id}"):
                del st.session_state.gio_hang[mon_id]
                st.rerun()
            st.write("---")
            
            # Ghi nhận thông tin vào chuỗi dữ liệu mã QR Dangfood
            thong_tin_hoa_don += f"- {mon['ten']} x{qty}\n"
            
        st.markdown(f"### 💵 Tổng tiền: `{tong_tien:,} VNĐ`")
        thong_tin_hoa_don += f"TONG TIEN: {tong_tien} VND\nThuc hien boi: Ho Hai Dang Nhom 11"
        
        # 4. Chức năng Ấn Thanh toán -> Xuất mã QR mẫu
        if st.button("💳 TIẾN HÀNH THANH TOÁN", type="primary", use_container_width=True):
            st.success("Đang khởi tạo mã QR thanh toán từ Dangfood...")
            
            # Tạo mã QR chứa thông tin hóa đơn mẫu bằng thư viện qrcode
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(thong_tin_hoa_don)
            qr.make(fit=True)
            
            # Chuyển đổi mã QR thành hình ảnh để Streamlit hiển thị
            img_qr = qr.make_image(fill_color="black", back_color="white")
            
            # Lưu ảnh vào bộ nhớ tạm thời buffer để hiển thị trên web
            buf = BytesIO()
            img_qr.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            # Hiển thị mã QR lên màn hình
            st.markdown("### 📲 Quét mã QR mẫu để xác nhận đơn hàng")
            st.image(byte_im, width=300, caption="Mã QR xác nhận hóa đơn Dangfood - Nhóm 11")
            
            # Nút reset giỏ hàng sau khi thanh toán xong
            if st.button("🔄 Tạo đơn hàng mới"):
                st.session_state.gio_hang = {}
                st.rerun()