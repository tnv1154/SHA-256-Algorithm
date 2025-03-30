# Chương Trình Mã Hóa SHA-256

Đây là một triển khai hoàn toàn từ đầu của thuật toán mã hóa SHA-256 mà không sử dụng bất kỳ thư viện mã hóa nào.

## Tính năng
- Mã hóa chuỗi văn bản thành chuỗi SHA-256
- Mã hóa nội dung file thành chuỗi SHA-256

## Cách sử dụng

### Yêu cầu
- Python 3.x

### Chạy chương trình
1. Chạy file `main.py`:
   ```
   python main.py
   ```
2. Chọn một trong các tùy chọn:
   - Tùy chọn 1: Mã hóa chuỗi
   - Tùy chọn 2: Mã hóa nội dung file
   - Tùy chọn 3: Thoát

## Cấu trúc Dự Án
- `main.py`: Điểm vào chính của chương trình, cung cấp giao diện dòng lệnh
- `sha256.py`: Triển khai thuật toán SHA-256
  
## Giải thích Chi Tiết về Thuật Toán SHA-256

SHA-256 là một thuật toán hàm băm mật mã được thiết kế bởi Cơ quan An ninh Quốc gia Hoa Kỳ (NSA) và được công bố năm 2001 bởi Viện Tiêu chuẩn và Công nghệ Quốc gia (NIST) như một Tiêu chuẩn Xử lý Thông tin Liên bang (FIPS).

Quá trình băm SHA-256 bao gồm các bước chính:

1. **Tiền xử lý**: Bổ sung bit và độ dài thông điệp để chuẩn bị cho quá trình băm
2. **Khởi tạo**: Thiết lập các giá trị băm ban đầu
3. **Xử lý khối**: Xử lý từng khối 512-bit của thông điệp qua vòng lặp nén
4. **Kết quả cuối cùng**: Kết hợp 8 giá trị 32-bit để tạo thành giá trị băm 256-bit

Các hàm toán học chính trong SHA-256:
- Hàm xoay: Rotate Right
- Hàm chọn (Ch): Chọn bit từ y hoặc z dựa trên giá trị của bit x
- Hàm đa số (Maj): Bit kết quả dựa trên đa số giữa x, y, z
- Sigma: Hàm tóm tắt hoạt động như bộ trộn bit

### Ưu điểm của Triển khai Này
- Không phụ thuộc vào thư viện ngoài
- Dễ hiểu và có thể học hỏi về thuật toán băm
- Có thể sử dụng trong các môi trường hạn chế không cho phép thư viện ngoài

## Lưu ý
Triển khai này nhằm mục đích học tập. Trong môi trường sản xuất, bạn nên sử dụng các thư viện mã hóa đã được kiểm chứng về tính bảo mật như `hashlib` của Python. 