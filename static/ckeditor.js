
document.addEventListener('DOMContentLoaded', () => {
    CKEDITOR.replace('editor');

    function updateText() {
        if (recognitionRunning) {
            fetchRecognizedContent();
        }
    }

    // Start the initial updateText call with a delay of 1000 milliseconds
    setTimeout(() => {
        updateText();

        // Set an interval for subsequent calls with a 1000 milliseconds delay
        setInterval(updateText, 1000);
    }, 1000);
});

function fetchRecognizedContent() {
    fetch('/audio_send_text', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Set the fetched content as the initial value of CKEditor
            CKEDITOR.instances['editor'].setData(data.processed_text);
        })
        .catch(error => console.error('Error fetching file:', error));
}




function fetchRecognizedContent() {
    fetch('/audio_send_text', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Set the fetched content as the initial value of CKEditor
            CKEDITOR.instances['editor'].setData(data.processed_text);
        })
        .catch(error => console.error('Error fetching file:', error));
}
