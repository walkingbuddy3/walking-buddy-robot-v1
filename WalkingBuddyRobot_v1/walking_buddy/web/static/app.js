async function moveRobot(command) {
    const status = document.getElementById("status");
    status.innerText = "Sending command: " + command;

    const response = await fetch("/api/move", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ command, seconds: 0.5 })
    });

    const data = await response.json();
    status.innerText = JSON.stringify(data);
}

async function sayHello() {
    const response = await fetch("/api/say", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: "Hello HK, Walking Buddy is ready." })
    });

    const data = await response.json();
    document.getElementById("status").innerText = JSON.stringify(data);
}

async function emergencyStop() {
    const status = document.getElementById("status");
    status.innerText = "EMERGENCY STOP sending...";

    const response = await fetch("/api/emergency-stop", {
        method: "POST",
        headers: {"Content-Type": "application/json"}
    });

    const data = await response.json();
    status.innerText = JSON.stringify(data);
}
