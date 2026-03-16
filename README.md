# BCHQSTB

Ung dung desktop PySide6 de quan ly cong dan va theo doi quy trinh nhap ngu.

## Tong quan

Ung dung hien tai gom cac nhom chuc nang chinh:

- Dang nhap va tao tai khoan nguoi dung
- Quan ly danh sach cong dan
- Quan ly ho so suc khoe va ly lich cong dan
- Theo doi trang thai nghia vu quan su
- Dashboard thong ke tong hop

Entry point cua ung dung la [main.py](/E:/CodeX/BCHQSTB/main.py).

## Cau truc thu muc

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

## Yeu cau

- Windows
- Python 3.10+
- MySQL Server 8+

## Cai dat moi truong

1. Cai Python 3.10 tro len.
2. Mo terminal tai thu muc project.
3. Cai dependencies:

```powershell
python -m pip install -r requirements.txt
```

Neu may co nhieu ban Python, co the dung:

```powershell
py -3.10 -m pip install -r requirements.txt
```

Neu can build `.exe`, cai them PyInstaller:

```powershell
python -m pip install pyinstaller
```

## Cau hinh database

Thong tin ket noi mac dinh nam trong [config/settings.py](/E:/CodeX/BCHQSTB/config/settings.py):

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `DB_AUTH_PLUGIN`

Mac dinh project dang dung:

- database: `military_citizen_db`
- user: `bch`
- password: `BCHQSPTB`

Ung dung ho tro ghi de `host`, `port`, `database` vao file runtime:

- [config/db_connection.json](/E:/CodeX/BCHQSTB/config/db_connection.json)

Ban co 3 cach cau hinh:

1. Sua truc tiep trong [config/settings.py](/E:/CodeX/BCHQSTB/config/settings.py)
2. Tao file [config/db_connection.json](/E:/CodeX/BCHQSTB/config/db_connection.json)
3. Mo app va bam `Thiet lap` trong man hinh dang nhap, hoac dung phim tat `Ctrl+Shift+D`

Vi du `config/db_connection.json`:

```json
{
  "host": "10.164.88.37",
  "port": 3306,
  "database": "military_citizen_db"
}
```

## Khoi tao database moi

Project da co san schema va script bootstrap:

- [config/schema.sql](/E:/CodeX/BCHQSTB/config/schema.sql)
- [scripts/init_database.py](/E:/CodeX/BCHQSTB/scripts/init_database.py)

### Cach 1: Tao user va grant bang root

Chay tren MySQL voi tai khoan admin:

```sql
CREATE DATABASE IF NOT EXISTS military_citizen_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'bch'@'%' IDENTIFIED WITH mysql_native_password BY 'BCHQSPTB';
GRANT ALL PRIVILEGES ON military_citizen_db.* TO 'bch'@'%';
FLUSH PRIVILEGES;
```

### Cach 2: Apply schema tu source

Sau khi user `bch` da co quyen tren database, chay:

```powershell
$env:PYTHONPATH="E:\CodeX\BCHQSTB"
python scripts\init_database.py --host 10.164.88.37 --port 3306
```

Script nay se:

- ket noi MySQL bang credential trong project
- tao database neu chua co
- tao cac bang can thiet
- ghi file [config/db_connection.json](/E:/CodeX/BCHQSTB/config/db_connection.json)

## Schema toi thieu

Code hien tai su dung cac bang sau:

- `users`
- `citizens`
- `citizen_backgrounds`
- `citizen_health`
- `military_service`

Luu y:

- App khong tu tao toan bo schema khi chay thuong.
- Mot so cot thieu trong `citizen_backgrounds` co the duoc bo sung boi service runtime.
- Neu dung DB moi, nen apply [config/schema.sql](/E:/CodeX/BCHQSTB/config/schema.sql) truoc.

## Chay ung dung

```powershell
python main.py
```

Neu `python` chua co trong `PATH`, co the dung duong dan day du den `python.exe`.

## Tai khoan dang nhap

Bang `users` la bat buoc cho luong dang nhap.

Ban co 2 cach tao user:

1. Mo app va bam `Tao tai khoan moi`
2. Tao bang chuc nang trong app/service sau khi database da san sang

Neu moi bootstrap mot DB trong qua trinh test, co the seed thu cong mot user `admin` de dang nhap.

## Luong su dung co ban

1. Mo app tu [main.py](/E:/CodeX/BCHQSTB/main.py)
2. Cau hinh ket noi MySQL neu can
3. Dang ky tai khoan moi hoac dang nhap
4. Quan ly cong dan trong module citizen
5. Cap nhat thong tin nghia vu trong module military
6. Xem tong hop trong module statistics

## Quy tac nghia vu quan su

Trang thai duoc code san trong [services/military_service.py](/E:/CodeX/BCHQSTB/services/military_service.py), gom:

- `CHUA_GOI`
- `KHAM_SO_TUYEN`
- `KHAM_SUC_KHOE`
- `DU_DIEU_KIEN`
- `CHO_NHAP_NGU`
- `DA_NHAP_NGU`
- `DA_XUAT_NGU`
- `TAM_HOAN`
- `MIEN_NVQS`

He thong chi cho chuyen sang buoc ke tiep trong quy trinh, hoac sang `TAM_HOAN` / `MIEN_NVQS`.

## Build file exe

File build nam tai [BCHQS.spec](/E:/CodeX/BCHQSTB/BCHQS.spec).

Ban spec hien tai da duoc sua de:

- khong con hardcode duong dan may cu hay may moi
- build duoc o `D:\BCHQSTB`, `E:\CodeX\BCHQSTB` hoac bat ky thu muc nao
- lay asset theo duong dan tu repo hien tai

Lenh build:

```powershell
python -m PyInstaller -y BCHQS.spec
```

File output:

- [dist/BCHQS/BCHQS.exe](/E:/CodeX/BCHQSTB/dist/BCHQS/BCHQS.exe)

## Luu y khi chuyen giua cac may

- Khong commit [config/db_connection.json](/E:/CodeX/BCHQSTB/config/db_connection.json) neu day la cau hinh runtime rieng cho tung moi truong.
- Source da portable cho build exe, nhung may build van can cai Python, dependencies va PyInstaller.
- Neu ve may cu, chi can `git pull`, cai package, cau hinh DB va build lai bang [BCHQS.spec](/E:/CodeX/BCHQSTB/BCHQS.spec).

## Luu y phat trien

- Giao dien duoc xay dung bang `PySide6`
- Stylesheet nam tai [assets/style.qss](/E:/CodeX/BCHQSTB/assets/style.qss)
- Da co mot so chuoi UI duoc don lai de tranh loi hien thi tieng Viet
- Build Windows dung `PyInstaller`

## Xu ly loi nhanh

`python` khong chay:

- Kiem tra lai `PATH`
- Thu dung `py`
- Hoac chay truc tiep file `python.exe`

Loi `No module named PySide6`:

```powershell
python -m pip install -r requirements.txt
```

Loi `No module named PyInstaller`:

```powershell
python -m pip install pyinstaller
```

Loi ket noi MySQL:

- Kiem tra MySQL da chay chua
- Kiem tra lai `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- Thu mo hop thoai `Thiet lap database` tu man hinh dang nhap
- Kiem tra user `bch` da duoc grant quyen tren `military_citizen_db` chua

Loi build vi thu muc `dist` khong rong:

```powershell
python -m PyInstaller -y BCHQS.spec
```
