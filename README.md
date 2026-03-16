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
|-- config/
|   |-- settings.py
|   `-- database.py
|-- services/
|-- ui/
`-- assets/
```

## Yeu cau

- Windows
- Python 3.10+
- MySQL Server

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

## Cau hinh database

Thong tin ket noi mac dinh dang nam trong [config/settings.py](/E:/CodeX/BCHQSTB/config/settings.py):

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `DB_AUTH_PLUGIN`

Ung dung con ho tro ghi de `host`, `port`, `database` vao file runtime:

- [config/db_connection.json](/E:/CodeX/BCHQSTB/config/db_connection.json)

Ban co 2 cach cau hinh:

1. Sua truc tiep gia tri trong [config/settings.py](/E:/CodeX/BCHQSTB/config/settings.py)
2. Mo app va bam `Thiet lap` trong man hinh dang nhap, hoac dung phim tat `Ctrl+Shift+D`

## Yeu cau schema toi thieu

Code hien tai su dung cac bang sau trong MySQL:

- `users`
- `citizens`
- `citizen_backgrounds`
- `citizen_health`
- `military_service`

Luu y:

- App khong tu tao toan bo database schema tu dau.
- Service `citizen_service` co tu bo sung mot so cot thieu trong bang `citizen_backgrounds`.
- Chuc nang dang nhap phu thuoc vao bang `users`.

## Chay ung dung

Chay app bang lenh:

```powershell
python main.py
```

Neu `python` chua co trong `PATH`, co the dung duong dan day du den `python.exe`.

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

## Luu y phat trien

- Giao dien duoc xay dung bang `PySide6`
- Stylesheet nam tai [assets/style.qss](/E:/CodeX/BCHQSTB/assets/style.qss)
- Mot so chuoi tieng Viet trong source hien dang bi loi encoding khi hien thi
- File build PyInstaller nam tai [BCHQS.spec](/E:/CodeX/BCHQSTB/BCHQS.spec)

## Xu ly loi nhanh

`python` khong chay:

- Kiem tra lai `PATH`
- Thu dung `py`
- Hoac chay truc tiep file `python.exe`

Loi `No module named PySide6`:

```powershell
python -m pip install -r requirements.txt
```

Loi ket noi MySQL:

- Kiem tra MySQL da chay chua
- Kiem tra lai `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- Thu mo hop thoai `Thiet lap database` tu man hinh dang nhap
