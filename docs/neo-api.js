(() => {
  const DEFAULT_API_BASE = "https://nexus-ai-backend-dx6m.onrender.com";
  const API_BASE = (window.NEXUS_NEO_API_BASE || DEFAULT_API_BASE).replace(/\/$/, "");
  const SESSION_KEY = "nexus-neo-session-v1";

  function sessionId() {
    let id = sessionStorage.getItem(SESSION_KEY);
    if (!id) {
      id = (crypto.randomUUID ? crypto.randomUUID() : "neo-" + Date.now() + "-" + Math.random().toString(36).slice(2));
      sessionStorage.setItem(SESSION_KEY, id);
    }
    return id;
  }

  async function askNeo(message) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 60000);
    try {
      const response = await fetch(API_BASE + "/api/neo/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message, session_id: sessionId()}),
        signal: controller.signal
      });
      let data = {};
      try { data = await response.json(); } catch (_) {}
      if (!response.ok) {
        throw new Error(data.detail || ("NEO HTTP " + response.status));
      }
      if (!data.reply) throw new Error("Empty NEO response");
      return data.reply;
    } catch (error) {
      if (error && (error.name === "AbortError" || /aborted/i.test(error.message || ""))) {
        return "استغرقت الاستجابة وقتاً أطول من المتوقع. جرّب إرسال الرسالة مرة أخرى.";
      }
      return "تعذّر الاتصال بـ NEO الآن. جرّب مرة أخرى بعد لحظات.";
    } finally {
      clearTimeout(timeout);
    }
  }

  function connect() {
    if (!window.NexusNEO) {
      setTimeout(connect, 50);
      return;
    }
    window.NexusNEO.onMessage = askNeo;
    window.dispatchEvent(new CustomEvent("nexus:neo-connected", {detail: {apiBase: API_BASE}}));
  }

  connect();
})();