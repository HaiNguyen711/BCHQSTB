# BCHQSTB

Ứng dụng desktop PySide6 để quản lý công dân và theo dõi quy trình nhập ngũ.

## Tổng quan

Ứng dụng hiện tại gồm các nhóm chức năng chính:

- Đăng nhập và tạo tài khoản người dùng
- Quản lý danh sách công dân
- Quản lý hồ sơ sức khỏe và lý lịch công dân
- Theo dõi trạng thái nghĩa vụ quân sự
- Dashboard thống kê tổng hợp

Entry point của ứng dụng là [main.py](main.py).

## Cấu trúc thư mục

```text
BCHQSTB/
|-- main.py
|-- requirements.txt
|-- BCHQS.spec
|-- config/
|   |-- settings.py
|   |-- database.py
|   `-- schema.sql
|-- scripts/
|   `-- init_database.py
|-- services/
|-- ui/
`-- assets/
```

## Yêu cầu

- Windows
- Python 3.10+
- MySQL Server 8+

## Cài đặt môi trường

1. Cài Python 3.10 trở lên.
2. Mở terminal tại thư mục project.
3. Cài dependencies:

```powershell
python -m pip install -r requirements.txt
```

Nếu máy có nhiều bản Python, có thể dùng:

```powershell
py -3.10 -m pip install -r requirements.txt
```

Nếu cần build `.exe`, cài thêm PyInstaller:

```powershell
python -m pip install pyinstaller
```

## Cấu hình database

Thông tin kết nối mặc định nằm trong [config/settings.py](config/settings.py):

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `DB_AUTH_PLUGIN`

Mặc định project đang dùng:

- database: `military_citizen_db`
- user: `bch`
- password: `BCHQSPTB`

Ứng dụng hỗ trợ ghi đè `host`, `port`, `database` vào file runtime:

- `config/db_connection.json`

Bạn có 3 cách cấu hình:

1. Sửa trực tiếp trong [config/settings.py](config/settings.py)
2. Tạo file `config/db_connection.json`
3. Mở app và bấm `Thiết lập` trong màn hình đăng nhập, hoặc dùng phím tắt `Ctrl+Shift+D`

Ví dụ `config/db_connection.json`:

```json
{
  "host": "10.164.88.37",
  "port": 3306,
  "database": "military_citizen_db"
}
```

## Khởi tạo database mới

Project đã có sẵn schema và script bootstrap:

- [config/schema.sql](config/schema.sql)
- [scripts/init_database.py](scripts/init_database.py)

### Cách 1: Tạo user và grant bằng root

Chạy trên MySQL với tài khoản admin:

```sql
CREATE DATABASE IF NOT EXISTS military_citizen_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'bch'@'%' IDENTIFIED WITH mysql_native_password BY 'BCHQSPTB';
GRANT ALL PRIVILEGES ON military_citizen_db.* TO 'bch'@'%';
FLUSH PRIVILEGES;
```

### Cách 2: Apply schema từ source

Sau khi user `bch` đã có quyền trên database, chạy ngay trong thư mục project:

```powershell
python scripts\init_database.py --host 10.164.88.37 --port 3306
```

Script này sẽ:

- kết nối MySQL bằng credential trong project
- tạo database nếu chưa có
- tạo các bảng cần thiết
- ghi file `config/db_connection.json`

## Schema tối thiểu

Code hiện tại sử dụng các bảng sau:

- `users`
- `citizens`
- `citizen_backgrounds`
- `citizen_health`
- `military_service`

Lưu ý:

- App không tự tạo toàn bộ schema khi chạy thường.
- Một số cột thiếu trong `citizen_backgrounds` có thể được bổ sung bởi service runtime.
- Nếu dùng DB mới, nên apply [config/schema.sql](config/schema.sql) trước.

## Chạy ứng dụng

```powershell
python main.py
```

Nếu `python` chưa có trong `PATH`, có thể dùng đường dẫn đầy đủ đến `python.exe`.

## Tài khoản đăng nhập

Bảng `users` là bắt buộc cho luồng đăng nhập.

Bạn có 2 cách tạo user:

1. Mở app và bấm `Tạo tài khoản mới`
2. Tạo bằng chức năng trong app/service sau khi database đã sẵn sàng

Nếu mới bootstrap một DB trong quá trình test, có thể seed thủ công một user `admin` để đăng nhập.

## Luồng sử dụng cơ bản

1. Mở app từ [main.py](main.py)
2. Cấu hình kết nối MySQL nếu cần
3. Đăng ký tài khoản mới hoặc đăng nhập
4. Quản lý công dân trong module citizen
5. Cập nhật thông tin nghĩa vụ trong module military
6. Xem tổng hợp trong module statistics

## Quy tắc nghĩa vụ quân sự

Trạng thái được code sẵn trong [services/military_service.py](services/military_service.py), gồm:

- `CHUA_GOI`
- `KHAM_SO_TUYEN`
- `KHAM_SUC_KHOE`
- `DU_DIEU_KIEN`
- `CHO_NHAP_NGU`
- `DA_NHAP_NGU`
- `DA_XUAT_NGU`
- `TAM_HOAN`
- `MIEN_NVQS`

Hệ thống chỉ cho chuyển sang bước kế tiếp trong quy trình, hoặc sang `TAM_HOAN` / `MIEN_NVQS`.

## Build file exe

File build nằm tại [BCHQS.spec](BCHQS.spec).

Bản spec hiện tại đã được sửa để:

- không còn hardcode đường dẫn máy cũ hay máy mới
- build được ở `D:\BCHQSTB`, `E:\CodeX\BCHQSTB` hoặc bất kỳ thư mục nào
- lấy asset theo đường dẫn từ repo hiện tại

Lệnh build:

```powershell
python -m PyInstaller -y BCHQS.spec
```

File output:

- `dist/BCHQS/BCHQS.exe`

## Lưu ý khi chuyển giữa các máy

- Không commit `config/db_connection.json` nếu đây là cấu hình runtime riêng cho từng môi trường.
- Source đã portable cho build exe, nhưng máy build vẫn cần cài Python, dependencies và PyInstaller.
- Nếu về máy cũ, chỉ cần `git pull`, cài package, cấu hình DB và build lại bằng [BCHQS.spec](BCHQS.spec).

## Lưu ý phát triển

- Giao diện được xây dựng bằng `PySide6`
- Stylesheet nằm tại [assets/style.qss](assets/style.qss)
- Đã có một số chuỗi UI được dọn lại để tránh lỗi hiển thị tiếng Việt
- Build Windows dùng `PyInstaller`

## Xử lý lỗi nhanh

`python` không chạy:

- Kiểm tra lại `PATH`
- Thử dùng `py`
- Hoặc chạy trực tiếp file `python.exe`

Lỗi `No module named PySide6`:

```powershell
python -m pip install -r requirements.txt
```

Lỗi `No module named PyInstaller`:

```powershell
python -m pip install pyinstaller
```

Lỗi kết nối MySQL:

- Kiểm tra MySQL đã chạy chưa
- Kiểm tra lại `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- Thử mở hộp thoại `Thiết lập database` từ màn hình đăng nhập
- Kiểm tra user `bch` đã được grant quyền trên `military_citizen_db` chưa

Lỗi build vì thư mục `dist` không rỗng:

```powershell
python -m PyInstaller -y BCHQS.spec
```