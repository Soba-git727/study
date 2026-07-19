import streamlit as st
import ollama

# 1. Cấu hình giao diện Web Chatbot
st.set_page_config(page_title="DangBot AI - Nhóm 11", page_icon="🤖", layout="centered")

st.title("🤖 DangBot AI - Offline Assistant")
st.markdown("### Hệ thống trợ lý trí tuệ nhân tạo của **Hồ Hải Đăng - Nhóm 11**")
st.caption("Ứng dụng chạy offline 100% sử dụng mô hình Qwen 2.5 trên card đồ họa RTX 3050.")

# 2. Khởi tạo bộ nhớ Lịch sử trò chuyện (Memory) nếu chưa có
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Hiển thị lại toàn bộ các tin nhắn cũ khi giao diện load lại
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Ô nhập câu hỏi từ người dùng (Chat Input)
if prompt := st.chat_input("Nhập câu hỏi của bạn vào đây..."):
    # Hiển thị tin nhắn của người dùng lên màn hình ngay lập tức
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Lưu câu hỏi của user vào lịch sử
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 5. Xử lý gọi AI xử lý và hiển thị hiệu ứng gõ chữ (Streaming)
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Tạo một ô trống để điền chữ từ từ vào
        full_response = ""
        
        try:
            # Gọi mô hình từ Ollama chạy trên card đồ họa của bạn
            # Cấu hình stream=True để nhận kết quả dạng từng từ một
            response_stream = ollama.chat(
                model='qwen2.5:7b',
                messages=st.session_state.messages,
                stream=True
            )
            
            # Vòng lặp lấy từng từ AI trả về và đập lên màn hình tạo hiệu ứng gõ chữ
            for chunk in response_stream:
                full_response += chunk['message']['content']
                message_placeholder.markdown(full_response + "▌") # Thêm con trỏ nhấp nháy
            
            # Khi kết thúc, hiển thị văn bản hoàn chỉnh và bỏ dấu con trỏ
            message_placeholder.markdown(full_response)
            
            # Lưu câu trả lời của AI vào lịch sử phiên chat
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Lỗi kết nối với Ollama: {e}")
            st.info("Hãy chắc chắn rằng ứng dụng Ollama vẫn đang chạy dưới nền hệ thống của bạn.")