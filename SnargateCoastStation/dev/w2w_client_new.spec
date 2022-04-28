# -*- mode: python -*-
a = Analysis(['w2w_client_new.py'],
             pathex=['C:\\Users\\gm4slv\\Python_Projects\\SnargateCoastStation\\dev'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='w2w_client_new.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
