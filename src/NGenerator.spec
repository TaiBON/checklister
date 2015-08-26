# -*- mode: python -*-

def Datafiles(*filenames, **kw):
    import os

    def datafile(path, strip_path=True):
        parts = path.split('/')
        path = name = os.path.join(*parts)
        if strip_path:
            name = os.path.basename(path)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    return TOC(
        datafile(filename, strip_path=strip_path)
        for filename in filenames
        if os.path.isfile(filename))

block_cipher = None
dbfile = Datafiles('db/twnamelist.db', strip_path=False) # keep the path of this file

a = Analysis(['NGenerator.py'],
             #pathex=['/Users/psilotum/Documents/Dropbox/projects/2014_TWplantlist/namelist-generator/src/qt-gui'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)

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
               a.binaries + [('pandoc', '/usr/local/bin/pandoc', 'BINARY')],
               dbfile,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'NGenerator'))
app = BUNDLE(coll,
             name='NGenerator.app',
             icon='icons/ngenerator.icns',
             bundle_identifier=None)
