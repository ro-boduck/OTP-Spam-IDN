document.addEventListener("DOMContentLoaded", () => {
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    const phoneInput = document.getElementById("phone-input");
    const form = document.getElementById("spam-form");
    const terminalOutput = document.getElementById("terminal-output");
    const apiOutput = document.getElementById("api-monitor-output");
    const statusIndicator = document.getElementById("status-indicator");
    const errorMessage = document.getElementById("error-message");

    let isRunning = false;
    let pollInterval = null;
    let lastIndexLogs = 0;
    let lastIndexApi = 0;

    const addLog = (text) => {
        const div = document.createElement("div");
        div.textContent = `> ${text}`;
        terminalOutput.appendChild(div);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    };

    const addApiLog = (log) => {
        const tr = document.createElement("tr");
        const isDead = Boolean(log.dead);
        const statusClass = isDead ? "api-dead" : "api-success";
        
        tr.innerHTML = `
            <td>${log.method}</td>
            <td>${log.domain || "Unknown"}</td>
            <td class="${statusClass}">${log.status}</td>
        `;
        
        apiOutput.appendChild(tr);
        apiOutput.parentElement.parentElement.scrollTop = apiOutput.parentElement.parentElement.scrollHeight;
    };

    const updateStatus = (running) => {
        isRunning = running;
        if (running) {
            statusIndicator.textContent = "RUNNING";
            statusIndicator.className = "status running";
            startBtn.disabled = true;
            stopBtn.disabled = false;
            phoneInput.disabled = true;
        } else {
            statusIndicator.textContent = "IDLE";
            statusIndicator.className = "status idle";
            startBtn.disabled = false;
            stopBtn.disabled = true;
            phoneInput.disabled = false;
        }
    };

    const pollStatus = async () => {
        try {
            const res = await fetch(`/api/status?last_index_logs=${lastIndexLogs}&last_index_api=${lastIndexApi}`);
            if (!res.ok) throw new Error("Status check failed.");
            const data = await res.json();
            
            if (data.logs && data.logs.length > 0) {
                if (lastIndexLogs === 0) terminalOutput.innerHTML = "";
                data.logs.forEach(log => addLog(log));
                lastIndexLogs = data.last_index_logs;
            }

            if (data.api_logs && data.api_logs.length > 0) {
                if (lastIndexApi === 0) apiOutput.innerHTML = "";
                data.api_logs.forEach(log => addApiLog(log));
                lastIndexApi = data.last_index_api;
            }

            if (data.is_running !== isRunning) {
                updateStatus(data.is_running);
                if (!data.is_running) {
                    clearInterval(pollInterval);
                    addLog("SEQUENCE TERMINATED.");
                }
            }
        } catch (error) {
            console.error("Polling error:", error);
        }
    };

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const phone = phoneInput.value.trim();
        if (!phone) return;

        errorMessage.classList.add("hidden");
        
        try {
            startBtn.textContent = "INITIALIZING...";
            startBtn.disabled = true;

            const res = await fetch("/api/start", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ phone })
            });
            
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Failed to start.");
            
            terminalOutput.innerHTML = "";
            apiOutput.innerHTML = "";
            lastIndexLogs = 0;
            lastIndexApi = 0;
            updateStatus(true);
            pollInterval = setInterval(pollStatus, 1000);
            
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove("hidden");
            startBtn.textContent = "INITIALIZE";
            startBtn.disabled = false;
        }
    });

    stopBtn.addEventListener("click", async () => {
        try {
            stopBtn.textContent = "ABORTING...";
            stopBtn.disabled = true;

            const res = await fetch("/api/stop", { method: "POST" });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Failed to stop.");
            
            stopBtn.textContent = "ABORT";
        } catch (error) {
            console.error("Stop error:", error);
            stopBtn.textContent = "ABORT";
            stopBtn.disabled = false;
        }
    });

    // Initial check on load
    fetch("/api/status").then(r => r.json()).then(data => {
        if (data.is_running) {
            updateStatus(true);
            lastIndexLogs = 0;
            lastIndexApi = 0;
            pollInterval = setInterval(pollStatus, 1000);
        }
    }).catch(console.error);
});
