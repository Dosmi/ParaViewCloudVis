# NOTE: run this script from command line ...
# ... where your images are to be made into a video
import os
from os import listdir
import subprocess
ffmpeg_cmd1 = [
    "ffmpeg",
    "-f",
    "image2",
    "-framerate",
    "24",
    "-i",
    # instead of getting all png files, ...
    # ... get files by pattern:
    #     frame_sanim.####.png ...
    #     ... where # is a digit
    os.path.join("frame_sanim.%04d.png"),
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
