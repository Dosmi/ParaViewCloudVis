# NOTE: run this script from command line ...
# ... where your images are to be made into a video
import os
from os import listdir
import glob, os
os.chdir("/currentdir/")
import subprocess
ffmpeg_cmd1 = [
    "ffmpeg",
    "-f",
    "image2",
    "-framerate",
    "24",
    "-pattern_type",
    "glob",
    "-i",
    "*.png",
    "-c:",
    "libx264",
    "-pix_fmt",
    "yuv444p",
    "-vf",
    "fps=24",
    "-crf",
    "20",
    "videofilename.mp4",
]
subprocess.call(ffmpeg_cmd1, shell=False)
# shutil.rmtree("temp-movie")

# save("curve_corected_test.mp4")
