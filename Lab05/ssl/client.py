import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))
    except:
        pass
    finally:
        ssl_socket.close()
        print("Kết nối đã đóng.")

def main():
    # Tạo socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Tạo SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # Không xác minh chứng chỉ (dùng cho thử nghiệm)

    # Thiết lập kết nối SSL
    ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')
    ssl_socket.connect(server_address)

    # Bắt đầu một luồng để nhận dữ liệu từ server
    receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
    receive_thread.start()

    # Gửi dữ liệu lên server
    try:
        while True:
            message = input("Nhập tin nhắn: ")
            ssl_socket.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("\nĐã thoát khỏi chương trình.")
    finally:
        ssl_socket.close()

if __name__ == "__main__":
    main()
