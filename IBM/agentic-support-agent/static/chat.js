const chat = document.getElementById("chat");
const traceList = document.getElementById("trace-list");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const resetBtn = document.getElementById("reset-btn");

function addMessage(role, text) {
  const wrap = document.createElement("div");
  wrap.className = `msg msg--${role}`;
  wrap.innerHTML = `
    <div class="msg__label">${role === "user" ? "You" : "Agent"}</div>
    <div class="msg__bubble"></div>
  `;
  wrap.querySelector(".msg__bubble").textContent = text;
  chat.appendChild(wrap);
  chat.scrollTop = chat.scrollHeight;
}

function addTraceSteps(trace) {
  trace.forEach((step) => {
    const el = document.createElement("div");
    el.className = "trace-step";
    el.innerHTML = `
      <div class="trace-step__tool">${step.tool}</div>
      <pre>in: ${JSON.stringify(step.input)}\nout: ${JSON.stringify(step.result)}</pre>
    `;
    traceList.appendChild(el);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";
  input.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();

    if (data.error) {
      addMessage("agent", `Sorry, something went wrong: ${data.error}`);
    } else {
      addTraceSteps(data.trace || []);
      addMessage("agent", data.reply);
    }
  } catch (err) {
    addMessage("agent", `Network error: ${err.message}`);
  } finally {
    input.disabled = false;
    input.focus();
  }
});

resetBtn.addEventListener("click", async () => {
  await fetch("/api/reset", { method: "POST" });
  chat.innerHTML = "";
  traceList.innerHTML = "";
  addMessage("agent", "Started a new conversation. How can I help?");
});
