const myTextArea = document.getElementById('title');
const remainingCharsText = document.getElementById('remaining-text');
const MAX_CHARS = 300;

myTextArea.addEventListener('input', () => {
    var charCount = myTextArea.value.length;

    if (charCount > MAX_CHARS) {
        myTextArea.value = myTextArea.value.substring(0, MAX_CHARS)
    }
    else {
        remainingCharsText.textContent = `${charCount}/${MAX_CHARS}`;
    }

});