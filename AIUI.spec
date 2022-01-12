# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

b = Analysis(['sysTrayApp.py'],
			 pathex=['D:\\myWork\\AIone'],
			 binaries=[],
			 datas=[],
			 hiddenimports=[],
			 hookspath=[],
			 hooksconfig={},
			 runtime_hooks=[],
			 excludes=[],
			 win_no_prefer_redirects=False,
			 win_private_assemblies=False,
			 cipher=block_cipher,
			 noarchive=False)
bpyz = PYZ(b.pure, b.zipped_data,
			 cipher=block_cipher)

bexe = EXE(bpyz,
		  b.scripts, 
		  [],
		  exclude_binaries=True,
		  name='AI6',
		  debug=False,
		  bootloader_ignore_signals=False,
		  strip=False,
		  upx=True,
		  console=False,
		  disable_windowed_traceback=False,
		  target_arch=None,
		  codesign_identity=None,
		  entitlements_file=None , icon='zImg\\promodders.ico')


coll = COLLECT(bexe,
			   b.binaries,
			   b.zipfiles,
			   b.datas,
			   strip=False,
			   upx=True,
			   upx_exclude=[],
			   name='AI')