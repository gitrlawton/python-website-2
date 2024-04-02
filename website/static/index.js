// Function to delete a note, given the note's id.
// This function sends a request to the backend using JavaScript.
function deleteNote(noteId) {
    // Send a POST request to the /delete-note endpoint.
    fetch('/delete-note', {
        method: 'POST',
        // { noteID: noteID } is a JavaScript object.  stringify takes a 
        // JS object and returns the JSON representation of it as a JSON string.
        body: JSON.stringify({ noteId: noteId }),
    // Once it gets a response...
    }).then((_res) => {
        // reload the window and redirect us to the homepage.
        window.location.href = "/";
    });
}