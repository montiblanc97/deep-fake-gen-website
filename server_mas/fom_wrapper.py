import platform
import subprocess

import cv2
import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
import warnings
warnings.filterwarnings("ignore")

from first_order_model.demo import make_animation, load_checkpoints


def fom_animate(src_img_path, driving_vid_path, out_path, buffer_dir):
    source_image = imageio.imread(src_img_path)
    reader = imageio.get_reader(driving_vid_path)

    #Resize image and video to 256x256
    source_image = resize(source_image, (256, 256))[..., :3]

    driving_video = []
    try:
        for im in reader:
            driving_video.append(im)
    except RuntimeError:
        pass
    reader.close()

    driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]

    generator, kp_detector = load_checkpoints(config_path='first_order_model/config/vox-256.yaml', checkpoint_path='first_order_model/example/vox-cpk.pth.tar', cpu=True)

    predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True, adapt_movement_scale=True, cpu=True)

    display(predictions, driving_vid_path, out_path, buffer_dir)


def display(generated, driving_vid_path, out_path, buffer_dir):

    for i in range(len(generated)):
        fname = buffer_dir + f"/{str(i)}.jpg"
        scaled = 255 * generated[i]  # float to rgb
        imageio.imwrite(fname, scaled.astype(np.uint8))

    command = f"ffmpeg -y -f image2 -r 15 -i {buffer_dir}/%d.jpg {buffer_dir}/inter.mp4"
    subprocess.call(command, shell=platform.system() != 'Windows', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    mp3_name = driving_vid_path.replace("_square.mp4", ".mp3")
    command = f"ffmpeg -y -i {buffer_dir}/inter.mp4 -i {mp3_name} -c:v copy -c:a aac {out_path}"
    subprocess.call(command, shell=platform.system() != 'Windows', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
