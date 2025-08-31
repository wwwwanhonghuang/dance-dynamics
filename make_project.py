import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--input_video_files", type=str, required=True)
parser.add_argument("--out_dir", type=str, default=".")

args = parser.parse_args()
input_video_files = args.input_video_files
out_dir = args.out_dir

print(f'Use video file(s): {input_video_files}')
print(f'Out Dir = {out_dir}')


os.makedirs(out_dir, exist_ok=True)
