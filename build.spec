# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

pf_foldr='platforms\\'
a = Analysis(['main.py'],
             pathex=['C:\\project\\happynet'],
    binaries=[(pf_foldr+'qwindows.dll', 'platforms'),
    (pf_foldr+'qoffscreen.dll', 'platforms'),
    (pf_foldr+'qminimal.dll', 'platforms')
    ],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
    name='happynmonitor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=['qwindows.dll'],
          runtime_tmpdir=None,
          console=False , icon='happynet.ico')
