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

<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/>

# Assignment1_MMT
  
## Commands
- Run code `py server.py`: cần thực hiện trước để ứng dụng khởi động server.
- Run code `py client.py`: để chạy ứng dụng client và kết nối client với server.  

## Cài đặt thư viện cần thiết
Trước khi chạy ứng dụng, bạn cần cài đặt các thư viện cần thiết. Bạn có thể sử dụng pip để cài đặt:

```bash
pip install opencv-python Pillow numpy
```

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
- **Phương thức**: Server sử dụng TCP để gửi/nhận gói tin.
- **Quản lý người dùng trực tuyến**: Theo dõi và gửi danh sách người dùng đang trực tuyến.
- **Gửi và nhận tin nhắn**: Server có thể gửi tin nhắn đến tất cả client và lưu trữ lịch sử tin nhắn.
- **Quản lý phát trực tiếp**: Cho phép người dùng bắt đầu phát trực tiếp video (đang chỉnh sửa).

### 2. Client (`client.py`)
- **Kết nối tới Server**: Client có thể kết nối tới server bằng cách sử dụng username để đăng nhập.
- **Gửi và nhận tin nhắn**: Người dùng có thể gửi nhận tin nhắn từ các người dùng khác thông qua phương thức Client-Server.
- **Nhận tin nhắn**: Client lắng nghe và hiển thị tin nhắn từ server.
- **Phát trực tiếp video**: Client có khả năng phát video từ webcam và truyền tải đến người dùng khác bằng P2P.

## Hình ảnh minh họa
- Đầu tiên ta phải kết nối vào server tước:
![Image](https://github.com/user-attachments/assets/7fd1eb74-4aa6-4e61-9114-ad503d7a0500)
- Sau đó ta đăng nhập vào thiết bị bằng username:
<img src="https://github.com/user-attachments/assets/29253e0f-f859-450c-a002-9a10c35ae6cc" alt="Sign in" width="300" height="300"/> <img src="https://github.com/user-attachments/assets/29253e0f-f859-450c-a002-9a10c35ae6cc" alt="Sign in" width="300" height="300"/>
- Có thể đăng nhập bằng nhiều client:
![Image](https://github.com/user-attachments/assets/49cf64b7-fbba-4534-911c-b06e8b799884)
- Hay đăng nhập bằng chế độ không xác minh, không có thông báo online hay offline nhưng vẫn nhận tin nhắn từ server:
<img src="https://github.com/user-attachments/assets/8b4e3f2c-fece-496f-8cc3-acc1babc68e8" alt="as_guest" width="300" height="300"/> <img src="https://github.com/user-attachments/assets/4aaa1b20-4b03-4579-bdd9-d73324d20823" alt="as_guest" width="300" height="300"/>
- Sau khi tài khoản đóng kết nối sẽ hiện thông báo:
![Image](https://github.com/user-attachments/assets/66d3fee5-69c5-46f7-b55e-364586550cc8)
- Khi kết thúc nếu muốn đóng server ta sẽ nhập lệnh 'exit'.


