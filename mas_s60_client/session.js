let sessionId, availModels, availInputs;
let srcVidUrl, srcVidDisp, outVid;
let sampleSelect, modelSelect, voiceCloneBox;
let runButton, backButton;

function toSessionView(args) {
    // sessionId = args["session_id"];
    sessionId = "1606783991269";
    availInputs = args["avail_inputs"];
    availModels = args["avail_models"];
    srcVidUrl = "test.webm";
    // srcVidUrl = args["src_vid_url"];

    srcVidDisp = document.getElementById("src_video");
    sampleSelect = document.getElementById("sample_select");
    modelSelect = document.getElementById("model_select");
    voiceCloneBox = document.getElementById("voice_clone");
    outVid = document.getElementById("out_video");
    runButton = document.getElementById("run_button");
    backButton = document.getElementById("back_button");

    srcVidDisp.src = srcVidUrl;

    addOptions(sampleSelect, availInputs);
    addOptions(modelSelect, availModels);

    backButton.addEventListener("click", function(event) {
        let e = new CustomEvent('retakeVideo');
        document.dispatchEvent(e);
    });

    runButton.addEventListener("click", function (event) {
        run();
    })
}

function run() {
    const data = new FormData();
    data.append("session_id", sessionId);
    data.append("driving_audio", sampleSelect.value);
    data.append("voice_clone", voiceCloneBox.checked);
    data.append("model", modelSelect.value);

    const url = `http://${get_server_url()}/run`;

    return fetch(url, {
        method: 'post',
        body: data,
    }).then(
        async (resp) => {
            let data = await resp.blob();
            outVid.src = URL.createObjectURL(data);
        }
    ).catch(
        except => console.log(except)
    );
}

function addOptions(select, options) {
    for (let o_name of options) {
        let opt = document.createElement("option");
        opt.text = o_name;
        select.add(opt);
    }
}