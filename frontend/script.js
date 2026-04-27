// file name: frontend/script.js

const alarm = document.getElementById("alarmSound");

let audioUnlocked = false;
let alarmPlaying = false;

// -----------------------------------
// Unlock audio on first click anywhere
// -----------------------------------
document.body.addEventListener("click", async () => {
    if (audioUnlocked) return;

    try {
        await alarm.play();
        alarm.pause();
        alarm.currentTime = 0;

        audioUnlocked = true;
        console.log("Audio unlocked");
    } catch (e) {
        console.log("Audio blocked by browser");
    }
});

// -----------------------------------
// Start alarm
// -----------------------------------
function startBeep() {

    if (!audioUnlocked) return;
    if (alarmPlaying) return;

    alarm.play()
        .then(() => {
            alarmPlaying = true;
        })
        .catch(err => console.log(err));
}

// -----------------------------------
// Stop alarm
// -----------------------------------
function stopBeep() {

    if (!alarmPlaying) return;

    alarm.pause();
    alarm.currentTime = 0;
    alarmPlaying = false;
}

// -----------------------------------
// Fetch backend status
// -----------------------------------
async function updateDashboard() {

    try {
        const res = await fetch("/status");
        const data = await res.json();

        // Navbar
        document.getElementById("meta").innerText =
            `${data.jetson_id} | ${data.location}`;

        // Drone Count
        document.getElementById("count").innerText =
            data.drone_count;

        // Status Box
        const statusBox = document.getElementById("status");

        if (data.status === "ALERT") {

            statusBox.innerText = "DRONE DETECTED";
            statusBox.className = "alert";

            startBeep();

        } else {

            statusBox.innerText = "NORMAL";
            statusBox.className = "normal";

            stopBeep();
        }

    } catch (err) {
        console.log("Status fetch error:", err);
    }
}

// -----------------------------------
// Live Clock
// -----------------------------------
setInterval(() => {

    document.getElementById("clock").innerText =
        new Date().toLocaleString();

}, 1000);

// -----------------------------------
// Refresh dashboard every second
// -----------------------------------
setInterval(updateDashboard, 1000);

// Initial load
updateDashboard();