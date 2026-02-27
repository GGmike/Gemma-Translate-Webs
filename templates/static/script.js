const sourceText   = document.getElementById("sourceText");
const targetText   = document.getElementById("targetText");
const sourceLang   = document.getElementById("sourceLang");
const targetLang   = document.getElementById("targetLang");
const modelSelect  = document.getElementById("modelSelect");
const translateBtn = document.getElementById("translateBtn");
const swapBtn      = document.getElementById("swapBtn");
const clearBtn     = document.getElementById("clearBtn");
const copyBtn      = document.getElementById("copyBtn");
const charCount    = document.getElementById("charCount");
const status       = document.getElementById("translationStatus");

async function loadModels() {
  try {
    const res = await fetch("/models");
    if (!res.ok) throw new Error(`Failed to load models: ${res.status}`);
    
    const data = await res.json();
    const models = data.models;
    
    modelSelect.innerHTML = "";
    
    models.forEach(model => {
      const option = document.createElement("option");
      option.value = model.value;
      option.textContent = model.label;
      modelSelect.appendChild(option);
    });
    
    if (!modelSelect.value) {
      modelSelect.value = models[0]?.value || "";
    }
  } catch (err) {
    console.error("Error loading models:", err);
  }
}

document.addEventListener("DOMContentLoaded", loadModels);

sourceText.addEventListener("input", () => {
  const len = sourceText.value.length;
  charCount.textContent = `${len} character${len !== 1 ? "s" : ""}`;
});

clearBtn.addEventListener("click", () => {
  sourceText.value = "";
  targetText.value = "";
  charCount.textContent = "0 characters";
  status.innerHTML = "&nbsp;";
});

copyBtn.addEventListener("click", async () => {
  if (!targetText.value) return;
  await navigator.clipboard.writeText(targetText.value);
  copyBtn.textContent = "✓ Copied";
  setTimeout(() => (copyBtn.textContent = "⎘ Copy"), 1500);
});

swapBtn.addEventListener("click", () => {
  const tmpLang = sourceLang.value;
  sourceLang.value = targetLang.value;
  targetLang.value = tmpLang;
  
  const tmpText = sourceText.value;
  sourceText.value = targetText.value;
  targetText.value = tmpText;
  
  charCount.textContent =
  `${sourceText.value.length} character${sourceText.value.length !== 1 ? "s" : ""}`;
});

translateBtn.addEventListener("click", async () => {
  const sourceLabel = sourceLang.options[sourceLang.selectedIndex].textContent;
  const targetLabel = targetLang.options[targetLang.selectedIndex].textContent;
  const text = sourceText.value.trim();
  if (!text) { sourceText.focus(); return; }

  translateBtn.disabled = true;
  translateBtn.innerHTML = '<span class="spinner"></span>Translating…';
  status.textContent = "Translating…";

  try {
    const res = await fetch("/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        source_lang: sourceLang.value,
        target_lang: targetLang.value,
        model: modelSelect.value, 
        source_label: sourceLabel,
        target_label: targetLabel,
      }),
    });

    if (!res.ok) throw new Error(`Server error ${res.status}`);

    const data = await res.json();
    targetText.value = data.translated_text;
    status.textContent = "Done ✓";
  } catch (err) {
    status.textContent = "Error — please try again";
    console.error(err);
  } finally {
    translateBtn.disabled = false;
    translateBtn.textContent = "Translate";
  }
});

sourceText.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
    translateBtn.click();
  }
});