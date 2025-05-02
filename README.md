<div align="center">
VIETNAM NATIONAL UNIVERSITY, HO CHI MINH CITY
<br />
UNIVERSITY OF TECHNOLOGY
<br />
FACULTY OF COMPUTER SCIENCE AND ENGINEERING
<br />
<br />

[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/HCMUT_official_logo.png/238px-HCMUT_official_logo.png)](https://www.hcmut.edu.vn/vi)
<br />
<br />
<img src="https://img.shields.io/github/stars/minhlight1306/Assignment1_MMT?color=white&logo=github">&emsp;<img src="https://img.shields.io/github/last-commit/minhlight1306/Assignment1_MMT?color=blue">
<br />
<img src="https://img.shields.io/github/languages/top/minhlight1306/Assignment1_MMT?color=yellow&logo=c&logoColor=yellow">&emsp;<img src="https://img.shields.io/github/repo-size/minhlight1306/Assignment1_MMT?color=orange&label=size&logo=git&logoColor=orange">
<br />

**Chat Application / Semester 242**
<br/>

</div>

# Languages & Tools

<img src="https://img.icons8.com/color/96/000000/c-programming.png" align="center" style="margin-left:10px;margin-bottom:5px;" width=70px/><img src="https://img.icons8.com/color/96/000000/linux--v1.png" align="center" style="margin-left:10px;margin-bottom:5px;" width=70px/>

# Assignment1_MMT
  
## Commands
- Run code `py server.py`: cần thực hiện trước để ứng dụng khởi động server.
- Run code `py client.py`: để chạy ứng dụng client và kết nối client với server.  

## Cài đặt thư viện cần thiết
Trước khi chạy ứng dụng, bạn cần cài đặt các thư viện cần thiết. Bạn có thể sử dụng pip để cài đặt:

```bash
pip install opencv-python Pillow numpy

## Cấu trúc của BTL:
```
 ┣ 📂Images         # Chứa hình ảnh.
 ┣ 📂.vscode        # Chứa file .json của VSCode, không ảnh hưởng tới bài tập lớn này.
 ┣ 📜server.py      # Code để khởi tạo server cho ứng dụng.
 ┣ 📜client.py      # Code để khởi tạo client cho ứng dụng.
 ┣ 📜README.md      # Mô tả chức năng và cách sử dụng.
```

## Chức năng

### 1. Server (`server.py`)
- **Kết nối với Client**: Server lắng nghe các kết nối từ nhiều client và xử lý các yêu cầu.
- **Phương thức**: Server sử dụng UDP để gửi/nhận gói tin.
- **Quản lý người dùng trực tuyến**: Theo dõi và gửi danh sách người dùng đang trực tuyến.
- **Gửi và nhận tin nhắn**: Server có thể gửi tin nhắn đến tất cả client và lưu trữ lịch sử tin nhắn.
- **Quản lý phát trực tiếp**: Cho phép người dùng bắt đầu phát trực tiếp video (đang chỉnh sửa).

### 2. Client (`client.py`)
- **Kết nối tới Server**: Client có thể kết nối tới server bằng cách sử dụng username để đăng nhập.
- **Gửi và nhận tin nhắn**: Người dùng có thể gửi nhận tin nhắn từ các người dùng khác thông qua phương thức Client-Server.
- **Nhận tin nhắn**: Client lắng nghe và hiển thị tin nhắn từ server.
- **Phát trực tiếp video**: Client có khả năng phát video từ webcam và truyền tải đến người dùng khác bằng P2P.

## Hình ảnh minh họa

![Đăng nhập ứng dụng](https://github.com/minhlight1306/Assignment1_MMT/tree/a3d162c2fd1fa8c7d69b2d0202020b6546d7daec/Images/images.png)  <!-- Thay đổi đường dẫn nếu cần -->
