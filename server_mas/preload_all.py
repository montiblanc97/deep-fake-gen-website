from index import run_deepfake


session_id = 1606783991269
driving_audio = ["Deeper and Faker", "Seashells", "Mitochondria", "Don't do drugs"]
models = ["Wav2Lip", "First Order Model"]
do_voice_clone = [False, True]

for d_a in driving_audio:
    for m in models:
        for d_v_c in do_voice_clone:
            run_deepfake(session_id, d_a, d_v_c, m)

