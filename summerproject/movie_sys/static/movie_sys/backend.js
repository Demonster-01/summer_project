

// Wait for 10 seconds and then remove the messages
setTimeout(function() {
    var messages = document.querySelectorAll('.messages');
    messages.forEach(function(message) {
        message.remove();
    });
}, 6000); // 10000 milliseconds = 10 seconds


function updateCurrentTime() {
    var currentTimeElement = document.getElementById('current-time');
    var currentTime = new Date().toLocaleTimeString();
    currentTimeElement.innerHTML = currentTime;
}

// Update the current time initially
updateCurrentTime();

// Update the current time every second (adjust the interval as needed)
setInterval(updateCurrentTime, 1000);