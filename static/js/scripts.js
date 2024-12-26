document.getElementById('translateButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent form submission and page reload

    const word = document.getElementById('word').value;
    const language = document.getElementById('language').value;
    const outputArea = document.getElementById('outputArea');
    
    // Show "loading..." message while waiting for response
    outputArea.innerHTML = '<p id="loadingText">Loading...Please Wait</p>';

    // Perform the AJAX request to your server (Flask, for example)
    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word: word, language: language }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.result) {
            const result = data.result;

            // Prepare the output structure
            let outputText = `
                <p><strong>Translated Word:</strong> ${result.translated_word}</p>
                <p><strong>Synonyms:</strong></p>
                <ul>
                    ${result.synonyms.map(synonym => `<li>${synonym}</li>`).join('')}
                </ul>
                <p><strong>Antonyms:</strong></p>
                <ul>
                    ${result.antonyms.map(antonym => `<li>${antonym}</li>`).join('')}
                </ul>
                <p><strong>Example Sentences:</strong></p>
                <ul>
                    ${result.examples.map(example => `<li>${example}</li>`).join('')}
                </ul>
                <p><strong>Definitions:</strong></p>
                <ul>
                    ${result.definitions.map(definition => `<li>${definition}</li>`).join('')}
                </ul>
            `;

            

            outputArea.innerHTML = outputText; // Display all content at once
        } else {
            outputArea.innerHTML = '<p>No translation result available.</p>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        outputArea.innerHTML = '<p>Error occurred. Please try again.</p>';
    });
});




const cursor = document.querySelector('.cursor');

document.addEventListener('mousemove', e => {
    cursor.setAttribute("style", "top: " + (e.pageY - 10) + "px; left: " + (e.pageX - 10) + "px;")
});

document.addEventListener('click', e => {
    cursor.classList.add("expand");
    setTimeout(() => {
        cursor.classList.remove("expand");
    }, 500);
});









let menu = document.querySelector('.menu');

profile.onclick = function () {
    menu.classList.toggle('active');
}