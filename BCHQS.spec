# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all

datas = [
    ('D:\\BCHQSTB\\assets', 'assets'),
    ('D:\\BCHQSTB\\.venv\\Lib\\site-packages\\mysql\\connector\\locales', 'mysql\\connector\\locales'),
    ('D:\\BCHQSTB\\.venv\\Lib\\site-packages\\mysql\\connector\\plugins', 'mysql\\connector\\plugins'),
    ('D:\\BCHQSTB\\.venv\\Lib\\site-packages\\mysql\\vendor', 'mysql\\vendor'),
]
binaries = []
hiddenimports = ['passlib.handlers.pbkdf2']
hiddenimports += collect_submodules('mysql.connector')
hiddenimports += collect_submodules('mysql.connector.plugins')
tmp_ret = collect_all('qtawesome')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['D:\\BCHQSTB\\main.py'],
    pathex=['D:\\BCHQSTB\\.venv\\Lib\\site-packages'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BCHQS',
    icon='D:\\BCHQSTB\\assets\\images\\logo.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BCHQS',
)
