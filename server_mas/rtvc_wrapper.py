from rtvc.encoder import inference as encoder
from rtvc.vocoder import inference as vocoder
from rtvc.synthesizer.inference import Synthesizer
import numpy as np
import soundfile as sf
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

encoder_path = Path("rtvc/encoder/saved_models/pretrained.pt")
vocoder_path = Path("rtvc/vocoder/saved_models/pretrained/pretrained.pt")
synthesizer_path = Path("rtvc/synthesizer/saved_models/logs-pretrained/taco_pretrained")

encoder.load_model(encoder_path)
synthesizer = Synthesizer(synthesizer_path)
vocoder.load_model(vocoder_path)

def generate_audio(audio_path, tts, out_path):
    preprocessed_wav = encoder.preprocess_wav(audio_path)

    embed = encoder.embed_utterance(preprocessed_wav)

    ## Generating the spectrogram
    texts = [tts]
    embeds = [embed]
    # If you know what the attention layer alignments are, you can retrieve them here by
    # passing return_alignments=True
    specs = synthesizer.synthesize_spectrograms(texts, embeds)
    spec = specs[0]

    generated_wav = vocoder.infer_waveform(spec)
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate*3), mode="constant")
    generated_wav = encoder.preprocess_wav(generated_wav)

    sf.write(out_path, generated_wav.astype(np.float32), synthesizer.sample_rate)

    silence = AudioSegment.silent(duration=1000)  # duration in milliseconds
    song = AudioSegment.from_wav(out_path)
    final_song = silence + song + silence + silence
    final_song.export(out_path, format="wav")