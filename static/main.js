var recognitionRunning = false;

function toggleRecognition() {
    if (recognitionRunning) {
        console.log("Recognition Button Opened");
        stopRecognition();
    } else {
        console.log("Recognition Button Closed");
        startRecognition();
    }
}

function startRecognition() {
    console.log("Start Recognition Clicked");
    // Get the content from the CKEditor
    var editorContent = CKEDITOR.instances.editor.getData();
    
    // Send the content in the POST request
    $.post("/start_recognition", { editor_content: editorContent }, function(data) {
        recognitionRunning = true;
        $("#start_recognition_btn").text("Stop Recognition");
        updateText();
    });
}


function stopRecognition() {
    console.log("Stop Recognition Clicked");
    $.get("/stop_recognition", function(data) {
        recognitionRunning = false;
        $("#start_recognition_btn").text("Start Recognition");
        $("#recognized_text").val(data.text);  // Update the recognized text in the input
    });
}

function updateText() {
    $.get("/get_text", function(data) {
        $("#recognized_text").val(data.text);  // Update the recognized text in the input
        if (recognitionRunning) {
            setTimeout(updateText, 5000);  // Add a 1-second delay before calling updateText again
        }
    });
}

// Load CKEditor initialization and file content loading script
$.getScript("/static/ckeditor.js");