# -*- mode: python -*-

block_cipher = None

static = Tree('pimpmybot\\wsgi\\static', prefix='wsgi\\static')
templates = Tree('pimpmybot\\wsgi\\templates', prefix='wsgi\\templates')
core_modules = Tree('pimpmybot\\core_modules', prefix='core_modules')
i18n = Tree('pimpmybot\\locales', prefix='locales', excludes='*.po')

a = Analysis(['pimpmybot\\main.py'],
             pathex=['D:\\Libraries\\Documents\\git\\PimpMyBot'],
             binaries=None,
             datas=None,
             hiddenimports=['utils.api'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pimpmybot',
          debug=True,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               static, templates, i18n, core_modules,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='pimpmybot')
