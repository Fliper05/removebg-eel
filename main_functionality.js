eel.expose(updateProgress);
function updateProgress(progress) {
    var progressBar = document.getElementById("myProgressBar");
    progressBar.value = progress;
    console.log(`Progress updated: ${progress}`);  // Log a message when the progress is updated
    return progress;  // return the progress value
}

eel.expose(updateStatusMessage);
function updateStatusMessage(status, message) {
    var statusHighlight = document.getElementById("status-highlight");
    var statusMessage = document.getElementById("status-message");
    statusHighlight.innerText = status;
    statusMessage.innerText = message;
    console.log(`Status message updated: ${status}, ${message}`);  // Log a message when the status message is updated
    return {status, message};  // return the status and message
}


eel.expose(updateSelectedFolder);
function updateSelectedFolder(folder) {
    var selectedFolder = document.getElementById("selected-folder");
    selectedFolder.innerText = folder;
}
