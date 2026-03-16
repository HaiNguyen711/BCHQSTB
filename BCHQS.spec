# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import collect_submodules

PROJECT_DIR = Path(SPECPATH)
ASSETS_DIR = PROJECT_DIR / 'assets'

datas = [
    (str(ASSETS_DIR), 'assets'),
]
binaries = []
hiddenimports = ['passlib.handlers.pbkdf2']
hiddenimports += collect_submodules('mysql.connector')
hiddenimports += collect_submodules('mysql.connector.plugins')

tmp_ret = collect_all('qtawesome')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[str(PROJECT_DIR)],
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
    icon=str(ASSETS_DIR / 'images' / 'logo.ico'),
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
