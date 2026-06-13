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


async function captureCamera() {
    const status = document.getElementById("status");
    status.innerText = "Capturing image...";

    const response = await fetch("/api/camera/capture", {
        method: "POST",
        headers: {"Content-Type": "application/json"}
    });

    const data = await response.json();
    status.innerText = JSON.stringify(data);

    const img = document.getElementById("latest-camera-image");
    if (img) {
        img.src = "/api/camera/latest?t=" + new Date().getTime();
    }

    const analyzeResponse = await fetch("/api/camera/analyze");
    const analyzeData = await analyzeResponse.json();

    const obstacleStatus = document.getElementById("obstacle-status");
    if (obstacleStatus) {
        obstacleStatus.innerText = analyzeData.message + " | Brightness: " + analyzeData.brightness;
        obstacleStatus.className = analyzeData.obstacle_possible ? "danger" : "safe";
    }
    const visionResponse = await fetch("/api/vision/detect");
    const visionData = await visionResponse.json();

    const detectedObjects = document.getElementById("detected-objects");
    if (detectedObjects) {
        if (visionData.detections && visionData.detections.length > 0) {
            detectedObjects.innerText = visionData.detections
                .map(item => item.label + " (" + Math.round(item.confidence * 100) + "%)")
                .join(", ");
        } else {
            detectedObjects.innerText = "No known objects detected.";
        }
    }


}



