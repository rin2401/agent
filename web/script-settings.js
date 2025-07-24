document.addEventListener("DOMContentLoaded", function() {
  // --- Settings Modal Logic ---
  const settingsBtn = document.getElementById("settingsBtn");
  const settingsModal = document.getElementById("settingsModal");
  const closeModal = document.getElementById("closeModal");
  const apiKeyInput = document.getElementById("apiKeyInput");
  const saveApiKeyBtn = document.getElementById("saveApiKeyBtn");
  const saveStatus = document.getElementById("saveStatus");

  settingsBtn.addEventListener("click", () => {
    settingsModal.style.display = "block";
    apiKeyInput.value = localStorage.getItem("api-key") || "";
    saveStatus.style.display = "none";
  });
  closeModal.addEventListener("click", () => {
    settingsModal.style.display = "none";
  });
  window.addEventListener("click", (event) => {
    if (event.target === settingsModal) {
      settingsModal.style.display = "none";
    }
  });
  saveApiKeyBtn.addEventListener("click", () => {
    const key = apiKeyInput.value.trim();
    if (key) {
      localStorage.setItem("api-key", key);
      saveStatus.style.display = "block";
      saveStatus.textContent = "Saved!";
      setTimeout(() => { saveStatus.style.display = "none"; }, 1200);
    }
  });
});
