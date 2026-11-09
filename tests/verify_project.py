#!/usr/bin/env python3
"""Safe static checks: does not pretend to replace Android compilation or device QA."""
from pathlib import Path
import hashlib
import re
import json

root=Path(__file__).resolve().parents[1]
required=[
 'build.gradle.kts','settings.gradle.kts','app/build.gradle.kts',
 'app/src/main/AndroidManifest.xml',
 'app/src/main/java/uz/melova/app/MainActivity.kt',
 'app/src/main/java/uz/melova/app/playback/MelovaPlaybackService.kt',
 'app/src/main/java/uz/melova/app/data/MelovaApi.kt',
 'app/src/main/java/uz/melova/app/ui/MelovaApp.kt',
 '.github/workflows/android-apk.yml',
]
for n in required:
    p=root/n
    assert p.exists() and p.stat().st_size>50,n
for i in range(1,4):
    p=root/f'app/src/main/res/raw/demo_{i}.mp3'
    assert p.is_file() and p.stat().st_size>100000,p
    assert p.read_bytes()[:3]==b'ID3',p
manifest=(root/'app/src/main/AndroidManifest.xml').read_text()
assert 'FOREGROUND_SERVICE_MEDIA_PLAYBACK' in manifest
assert 'uzmelova' in manifest
assert 'MediaSessionService' in manifest
build=(root/'app/build.gradle.kts').read_text()
assert 'compileSdk = 36' in build
assert 'compose-bom:2025.08.00' in build
assert 'media3-session:1.11.1' in build
api=(root/'app/src/main/java/uz/melova/app/data/MelovaApi.kt').read_text()
for v in ['melova-audio','profiles','tracks','playlists','playlist_tracks','listening_history','reports','favorites','auth/v1','storage/v1']:
    assert v in api, v
assert 'sb_secret_' in api and 'service_role' in api
assert 'setFixedLengthStreamingMode' in api
assert '20*1024*1024' in api
print('MELOVA static smoke checks: PASSED')
