import platform
import sys
import time
from pathlib import Path
import os
import subprocess

def create_session():
    session_id = int(round(time.time() * 1000))
    workspace = Path("tmp/{id}".format(id=session_id))
    workspace.mkdir(exist_ok=True)

    return session_id

def get_session_folder(session_id):
    return Path("tmp/{id}".format(id=session_id))

def save_request_file_stream(session_id, video_file):
    session_folder = get_session_folder(session_id)

    # save to workspace
    webm_path = session_folder / "src_vid.webm"
    video_file.save(str(webm_path))

    # convert to mp4
    mp4_path = session_folder / "src_vid.mp4"
    subprocess.call(['ffmpeg', "-y", '-i', str(webm_path),
                     # "-filter:v", "fps=7,scale=640:480,crop=in_w/3:2*in_h/3:in_w/3:in_h/10", mp4_path],
                     "-filter:v", "fps=7,scale=640:480,crop=in_w/2:2*in_h/3:in_w/4:in_h/12", mp4_path],
                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # extract audio for voice cloning
    wav_path = session_folder / "src_audio.wav"
    subprocess.call(["ffmpeg", "-y", "-i", webm_path, wav_path])

    # extract first image as square
    img_path = session_folder / "src_img.jpg"
    command = f"ffmpeg -i {webm_path} -vf \"scale=640:480,crop=3*in_h/4:3*in_h/4:in_w/2-3*in_h/8:in_h/12,select=eq(n\,0)\" -q:v 3 {img_path}"
    subprocess.call(command, shell=platform.system() != 'Windows', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return float(result.stdout)


if __name__ == '__main__':
    mp4_path = "tmp/1606508717789/src_vid.mp4"
    # convert to mp4
    subprocess.call(['ffmpeg', "-y", '-i', "tmp/1606508717789/src_vid.webm",
                     # "-filter:v", "fps=7,scale=640:480,crop=in_w/3:2*in_h/3:in_w/3:in_h/10", mp4_path],
                     "-filter:v", "fps=7,scale=640:480,crop=in_w/2:3*in_h/4:in_w/4:0", mp4_path],
                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # extract audio for voice cloning
    wav_path = "tmp/1606508717789/src_audio.wav"
    subprocess.call(["ffmpeg", "-y", "-i", "tmp/1606508717789/src_vid.webm", wav_path])