let introSection, recordSection;
let webcamView, preview, turnOnButton, startButton, stopButton;
let playbackView, playback, redoButton, uploadButton;

function setupWebcam() {
    introSection = document.getElementById("intro_section");
    recordSection = document.getElementById("record_section");

    webcamView = document.getElementById("webcam_view");
    preview = document.getElementById("webcam_preview");
    turnOnButton = document.getElementById("turn_on_button");
    startButton = document.getElementById("start_button");
    stopButton = document.getElementById("stop_button");

    playbackView = document.getElementById("playback_view");
    playback = document.getElementById("playback");
    redoButton = document.getElementById("redo_button");
    uploadButton = document.getElementById("upload_button");


    turnOnButton.addEventListener("click", turnOnHandle);

    startButton.addEventListener("click", startRecordingHandle);

    stopButton.addEventListener("click", function() {
        toggleInputView(false);
        stop(preview.srcObject);
    });

    redoButton.addEventListener("click", function() {
        toggleInputView(true);
        turnOnHandle()
    });

    uploadButton.addEventListener("click", async function() {
        playback.pause();

        let result = await upload();
        let json = JSON.parse(await result.text());
        json["src_vid_url"] = playback.src;

        let event = new CustomEvent('sessionStarted', {detail: json});
        document.dispatchEvent(event);
    });

    startingView(true);
}

function startingView(first_start) {
    toggleInputView(true);
    toggleWebcamVideoElement(false);
    toggleWebcamSection(turnOnButton);

    if (!first_start) {
        turnOnHandle();
    }
}

function turnOnHandle() {
    toggleInputView(true);
    toggleWebcamVideoElement(true);
    navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
    }).then(stream => {
        preview.srcObject = stream;
        preview.captureStream = preview.captureStream || preview.mozCaptureStream;
        toggleWebcamSection(startButton);
    })
}

function startRecordingHandle() {
    toggleWebcamSection(stopButton);
    startRecording(preview.captureStream())
        .then (recordedChunks => {
            let recordedBlob = new Blob(recordedChunks, { type: "video/webm" });
            playback.blob = recordedBlob;
            playback.src = URL.createObjectURL(recordedBlob);

            console.log("Successfully recorded " + recordedBlob.size + " bytes of " +
                recordedBlob.type + " media.");
        })
        .catch(console.log);
}

function startRecording(stream) {
    let recorder = new MediaRecorder(stream);
    let data = [];

    recorder.ondataavailable = event => data.push(event.data);
    recorder.start();

    let stopped = new Promise((resolve, reject) => {
        recorder.onstop = resolve;
        recorder.onerror = event => reject(event.name);
    });

    return stopped.then(() => data);
}
function stop(stream) {
    stream.getTracks().forEach(track => track.stop());
}

function toggleInputView(showWebcam) {
    if (showWebcam === true) {
        webcamView.style.display = "block";
        playbackView.style.display = "none";
    } else {
        webcamView.style.display = "none";
        playbackView.style.display = "block";
    }
}

function toggleWebcamVideoElement(showElement) {
    if (showElement === true) {
        preview.style.display = "block"
    } else {
        preview.style.display = "none"
    }
}

function toggleWebcamSection(buttonToShow) {
    for (let but of [turnOnButton, startButton, stopButton]) {
        if (but === buttonToShow) {
            but.style.display = "block";
        } else {
            but.style.display = "none";
        }
    }
    if ([startButton, stopButton].includes(buttonToShow)) {
        introSection.style.display = "none";
        recordSection.style.display = "block";
    } else {
        introSection.style.display = "block";
        recordSection.style.display = "none";
    }

}

function upload() {
    const url = `http://${get_server_url()}/upload`;
    let file = new File([playback.blob], 'playback');

    const data = new FormData();
    data.append('user_video', file);

    return fetch(url, {
        method: 'post',
        body: data,
    }).then(
        data => data
    ).catch(
        except => console.log(except)
    )
}