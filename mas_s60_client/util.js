

function get_server_url() {
    let raw = document.getElementById("ip_addr").value.trim();
    let split_i = raw.indexOf("//");
    let url;
    if (split_i !== -1) {
        url = raw.slice(split_i+2);
    } else {
        url = raw;
    }
    return url;
}