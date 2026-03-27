# -*- mode: python ; coding: utf-8 -*-
import os
from kivy_deps import sdl2, glew

block_cipher = None

# Rutas de assets y configuración
added_files = [
    ('assets', 'assets'),
    ('version.json', '.'),
    ('modules', 'modules'),
    ('config', 'config'),
]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'kivymd.stiffscroll',
        'kivymd.uix.segmentedcontrol',
        'kivymd.uix.behaviors',
        'kivymd.effects.stiffscroll',
        'requests',
        'supabase',
        'pydantic',
        'pydantic_core._pydantic_core'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ReparacionesWasion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Ponemos False para que no abra ventana de comandos
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/wasion-ltd--600.png'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ReparacionesWasion',
)
