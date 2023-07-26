#!/usr/bin/env python

import argparse
import math
import os
from pathlib import Path
import subprocess
import sys

def parse_args():
    description = """
Runs editor on images in a directory.
Set `CLASS_LABELS` environment variable to avoid passing `--labels` as option.
Use C-b in editor to break out of the loop, use C-r to get back to previous image.
"""
    p = argparse.ArgumentParser(description)
    p.add_argument('input_path', type=Path, help='Image directory')
    p.add_argument('output_path', type=Path, help='Annotation directory')
    p.add_argument('--labels', '-l', help='Class labels, comma separated')
    p.add_argument('--skip', '-s', type=int, default=0, help='Number of images to skip')
    p.add_argument('--skip-annotated', '-a', action='store_true', help='Skip already annotated images')
    return p.parse_args()


def main():
    args = parse_args()

    labels = args.labels
    if labels is None:
        labels = os.environ.get('CLASS_LABELS')

    def get_data_path(path):
        return args.output_path / path.name

    paths = [
        p for p in args.input_path.iterdir()
        if not args.skip_annotated or not get_data_path(p).exists()]

    if args.skip:
        paths = paths[args.skip:]

    editor_path = Path(sys.argv[0]).parent / 'editor.py'
    idx_len = int(math.log(len(paths), 10))
    idx = 0
    while idx < len(paths):
        path = paths[idx]
        print(str(idx).rjust(idx_len), path)

        command = ['python', editor_path, '--data', get_data_path(path), path]
        if labels:
            command += ['--labels', labels]
        result = subprocess.run(command)
        if result.returncode == 0:
            idx += 1
        elif result.returncode == 2:
            if idx > 0:
                idx -= 1
        else:
            break


if __name__ == '__main__':
    main()
