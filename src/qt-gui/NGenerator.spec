# -*- mode: python -*-

block_cipher = None


a = Analysis(['NGenerator.py'],
             pathex=['/Users/psilotum/Documents/Dropbox/projects/2014_TWplantlist/namelist-generator/src/qt-gui'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)

a.datas += [('twnamelist.db', '/tmp/twnamelist.db', 'DATA')]
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='NGenerator',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='NGenerator')
app = BUNDLE(coll,
             name='NGenerator.app',
             icon=None,
             bundle_identifier=None)
