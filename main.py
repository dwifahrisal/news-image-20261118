#!/usr/bin/env python3
"""entry point: copy the pre-rendered front page into /output/entry.png"""
import shutil, os, sys
os.makedirs('/output', exist_ok=True)
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'entry.png')
dst = '/output/entry.png'
shutil.copyfile(src, dst)
print(f'wrote {dst} ({os.path.getsize(dst)} bytes)')
