from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

import model_wrapper
import util
from util import *
from const import *

app = Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def post_video():
    session_id = create_session()

    save_request_file_stream(session_id, request.files["user_video"])
    resp_data = {
        "session_id": session_id,
        "avail_models": avail_models,
        "avail_inputs": avail_inputs
    }

    return jsonify(resp_data)

@app.route('/run', methods=["POST"])
def handle_message():
    parsed = request.form
    session_id = int(parsed["session_id"])
    driving_audio = parsed["driving_audio"]
    do_voice_clone = parsed["voice_clone"] == "true"
    model = parsed["model"]

    return run_deepfake(session_id, driving_audio, do_voice_clone, model)

def run_deepfake(session_id, driving_audio, do_voice_clone, model):
    prefix = input_to_text[driving_audio]["file_prefix"]
    session_folder = util.get_session_folder(session_id)

    voice_clone_text = "_cloned" if do_voice_clone and model == "Wav2Lip" else ""
    out_prefix = f"{model.lower().replace(' ', '')}_{prefix}{voice_clone_text}"
    out_vid_fname = out_prefix + ".mp4"

    out_vid_path = session_folder / out_vid_fname
    if not os.path.exists(out_vid_path):
        # only uses mp3 input
        if model == "Wav2Lip":
            if do_voice_clone:
                cloned_audio_fname = out_prefix + ".wav"
                cloned_audio_path = str(session_folder / cloned_audio_fname)
                if not os.path.exists(cloned_audio_path):
                    tts = input_to_text[driving_audio]["text"]
                    driving_audio_path = model_wrapper.run_rtvc(session_id, tts, cloned_audio_fname)
                else:
                    driving_audio_path = cloned_audio_path
            else:
                driving_audio_path = f"resources/{prefix}.mp3"
            out_vid_path = model_wrapper.run_wav2lip(session_id, driving_audio_path, out_vid_fname)

        elif model == "First Order Model":
            driving_video_path = f"resources/{prefix}_square.mp4"
            out_vid_path = model_wrapper.run_fom(session_id, driving_video_path, out_vid_fname)
        else:
            raise ValueError(f"Unknown model: {model}")

    data = open(out_vid_path, "rb").read()
    return data

if __name__ == '__main__':
    app.run()