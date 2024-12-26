



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




// Wait for the page to load completely
window.addEventListener("load", () => {
    const loader = document.getElementById("loader");
    const mainContent = document.getElementById("mainContent");
    const loaderAudio = document.getElementById("loaderAudio");

    // Attempt to play the audio when the loader is visible
    loaderAudio.play().then(() => {
        console.log("Audio is playing.");
    }).catch(error => {
        console.warn("Autoplay restriction: Audio playback failed. User interaction is required.");
    });

    // Set a timeout to show the main content after 8 seconds
    setTimeout(() => {
        // Hide the loader
        loader.style.display = "none";

        // Stop the audio when the loader is hidden
        loaderAudio.pause();
        loaderAudio.currentTime = 0;

        // Show the main content
        mainContent.classList.remove("hidden");
    }, 8000); // Adjust the time as needed (8000 ms = 8 seconds)
});


