function updateTime() {
    // Get the current date and time
    var currentDate = new Date();

    // Extract hours, minutes, and seconds
    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();
    var seconds = currentDate.getSeconds();

    // Format the time as a string
    var formattedTime = padZero(hours) + ":" + padZero(minutes) + ":" + padZero(seconds);

    // Update the content of the element with id "current-date-time"
    document.getElementById("current-date-time").innerText = formattedTime;
}

function padZero(number) {
    // Add leading zero if the number is less than 10
    return (number < 10 ? "0" : "") + number;
}

// Update the time every second (1000 milliseconds)
setInterval(updateTime, 1000);

// Run updateTime once on page load
window.onload = updateTime;
