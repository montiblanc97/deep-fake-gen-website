document.addEventListener("DOMContentLoaded", function(event) {
    setupWebcam();

    showView("webcam");

    // let args = {
    //     session_id: "1606783991269",
    //     avail_inputs: ["Deeper and Faker", "Seashells", "Mitochondria", "Don't do drugs"],
    //     avail_models: ["Wav2Lip", "First Order Model"],
    //     src_vid_url: "test.mp4"
    // };
    // toSessionView(args);
    // showView("session");
});

document.addEventListener("sessionStarted", function (event) {
    let args = event.detail;
    toSessionView(args);
    showView("session");
});

document.addEventListener("retakeVideo", function (event) {
    startingView();
    showView("webcam");
});

function showView(view) {
    let input = document.getElementById("input");
    let session = document.getElementById("session");
    if (view === "webcam") {
        input.style.display = "flex";
        session.style.display = "none";
    } else if (view === "session") {
        input.style.display = "none";
        session.style.display = "flex";
    } else {
        throw Error(`unknown view ${view}`);
    }
}