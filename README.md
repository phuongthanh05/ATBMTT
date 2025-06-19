# ATBMTT 
 -Mục tiêu
Cho phép người gửi ký số một file bằng khóa riêng.
Gửi file đã ký, chữ ký (.sig) và khóa công khai cho người nhận.
Người nhận có thể xác minh chữ ký để kiểm tra tính toàn vẹn và xác thực của file.

- rsa_utils.py
Thư viện hỗ trợ:
Tạo cặp khóa RSA (2048 bit).
Ký dữ liệu bằng khóa riêng.
Xác minh chữ ký bằng khóa công khai.

-Giao diện Web
sender.html: Giao diện người gửi (upload và ký file).
receiver.html: Giao diện người nhận (upload file, chữ ký và public key để xác minh).
result_links.html: Trang kết quả hiển thị đường dẫn tải chữ ký và khóa công khai.

