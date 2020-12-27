import subprocess
import platform
import util
from wav2lip import inference
from rtvc import demo_cli
from rtvc_wrapper import generate_audio
from fom_wrapper import fom_animate


def run_wav2lip(session_id, driving_audio, out_fname):
    session_folder = util.get_session_folder(session_id)
    in_path = str(session_folder / "src_vid.mp4")
    # inter_path = str(session_folder / ("unedited_" + out_fname))
    out_path = str(session_folder / out_fname)

    inference.main(source_vid=in_path,
                   driving_audio=driving_audio,
                   out_path=out_path,
                   checkpoint_path="wav2lip/checkpoints/wav2lip.pth")

    return out_path

    # cut last second, wav2lip jacks it up
    # vid_dur = util.get_length(inter_path)
    # command = f'ffmpeg -i {inter_path} -t {str(vid_dur-1)} {out_path}'
    # subprocess.call(command, shell=platform.system() != 'Windows', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def run_fom(session_id, driving_video, out_fname):
    session_folder = util.get_session_folder(session_id)
    src_img = str(session_folder / "src_img.jpg")
    out_path = session_folder / out_fname

    buffer_dir = session_folder / "buffer"
    buffer_dir.mkdir(exist_ok=True)

    fom_animate(src_img, driving_video, out_path, str(buffer_dir))

    return str(out_path)

def run_rtvc(session_id, tts, out_fname):
    session_folder = util.get_session_folder(session_id)
    audio_path = str(session_folder / "src_audio.wav")
    out_path = session_folder / out_fname

    generate_audio(audio_path, tts, out_path)

    return str(out_path)


if __name__ == '__main__':
    demo_cli.main()