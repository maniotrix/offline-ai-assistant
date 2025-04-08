# Karna Vision-Based UI Agent: Current Capabilities and Next Steps

*A human-inspired, vision-first UI agent designed to perceive, act, and eventually reason on screen — just like we do.*
*Once trained for an app, Karna can repeat that task across different devices, screen resolutions, and themes — without retraining. Its visual memory operates layout-agnostically, matching elements like a human would: by appearance, not code.*

[🔍 ChatGPT LLM Interaction Demo – Vision-Based Automation (YouTube)](https://youtu.be/PpPhaN1ZoPE)



>##### 🔗 **Must Read Related Readme Files**
>1. **[ChatGPT Web Interface Automation](chatgpt_test_README.md)** – A practical implementation of Karna’s core vision stack for automating the ChatGPT interface.
>2. **[Vision Based UI Automation Demo](vision_based_ui-automation_demo.md)**
>3. **[Karna Cortex Vision Module](cortex_vision.md)** – A biomimetic, modular system inspired by human vision for general UI automation.

---
## ✅ What We Currently Achieve (Factually)


### 🔍 **1. CNN-Based Visual Detection**
- **YOLO-style object detection** (labelled `box_yolo_content_yolo`) for interactive UI components like `icons` or `icon + text`.
- **ResNet embeddings** for patch similarity, enabling:
  - Cross-frame element tracking
  - Layout-agnostic patch matching
  - Spatial tolerance to shifts/resizing

This is our **V1–V4 vision stack** — low-to-mid-level perception.

---

### 🧠 **2. OCR-Based Text Perception**
- We use `easyocr` OCR to extract UI text (`box_ocr_content_ocr`).
- Combined with layout and patch anchors for semantic anchoring.

This simulates **ventral-stream (object + text recognition)** of the human vision pipeline.

---

### 🖱️ **3. OS-Level Execution**
- **Keyboard**: Hotkeys like `Enter` and `End`, to simulate user behavior.
- **Clipboard**: Used for input (prompts) and output (responses) via `pyperclip` or `PowerShell`.
- **Mouse**: Moves to coordinates based on visual detection and clicks accordingly.

This is our **motor cortex / muscle layer** — precise and OS-agnostic.

---

### 🧠 **4. Vision-Only Control = High Anti-Bot Resilience**
Because we:
- **Don't inject into the DOM**
- **Don’t call any browser APIs**
- **Only simulate mouse/keyboard**
- **Work off-screen pixels**, not app internals

→ This makes us resilient against bot detection tools like:
- `navigator.webdriver`
- Selenium fingerprinting
- DOM mutation monitoring
- Network interception

However:
> ⚠️ **We are not immune.**  
Unpredictable behaviors (CAPTCHAs, overlays, loading screens) **can and do break us**.

---

### 📊 **Want to see it in action?**  
* **[ChatGpt as LLM Demo on Youtube](https://youtu.be/PpPhaN1ZoPE)** 
* **[ChatGpt as  VLM Demo on Youtube](https://youtu.be/0eRsXNdk_lE)**

> Check out our step-by-step visualizations in  
> * **[Execution Trace Visual Log](execution_visual_log.md)** — screenshots and match outputs from real test runs.

---

## 🧩 What We’re *Not* Yet Doing

- No long-term memory over screen patterns
- No reasoning over visual state transitions
- No abstraction (“this looks like a modal dialog even if it’s styled differently”)
- No goal-driven planning
- No VLM or task reasoning modules integrated *yet*

So we are **not yet** simulating full human visual cognition.  
But we **are functionally simulating the bottom-up visual + motor loop** — quite faithfully.

---

## 📦 Why Not Just Use GPT-4V, Gemini, or Other VLMs?

The AI landscape is evolving rapidly — and powerful vision-language models (VLMs) like GPT-4V and Gemini are improving fast. But we deliberately chose **not** to rely on them in Karna because:

- ❌ They don’t run well on consumer edge devices (need 24–48GB VRAM or cloud inference)
- ❌ Even small VLMs (like 7B) are slow and compute-heavy
- ❌ They struggle with pixel-accurate UI element detection
- ❌ They require sharing screenshots/data with cloud APIs
- ❌ They're built for perception, not interaction

Instead, **Karna is optimized for where lightweight agents are most needed**:

- ✅ CPU-only or 2GB GPU systems (even 6–7 year old PCs)
- ✅ Private, offline environments (no cloud)
- ✅ Tasks requiring precision clicks, typing, retry logic
- ✅ Low-latency, real-time local control

> We're not against VLMs — we just believe in using them where they matter most.  
> Karna fills the gap where *they can't go yet*.
> 🔗 **[Full breakdown: Why We Built Karna From Scratch Instead of Using a VLM](why_not_just_use_vlm.md)**

## 🧠 How We can Simulate Visual Reasoning with a Local LLM/VLM (Current + Future Steps)

If we structure the system like this:

```plaintext
[ Visual Cortex Modules ]        ← screen → YOLO + OCR + ResNet
        ↓
[ Visual Semantic Layer ]        ← interprets layout, extracts features, stores visual memory
        ↓
[ Local LLM + RAG + Tool Calls ]← answers questions, reasons about the scene, plans next steps
        ↓
[ Task Schema & Executor ]       ← performs clicks, typing, scrolls, retries based on intent
```


This gives us a **closed-loop vision–language–action system**.
And with an LLM/VLM capable of reasoning and natural language understanding, we can simulate a **basic but real cognitive loop grounded in visual perception.**

---


### ✅ What it can already do:
- Answer visual questions from screenshots (VQA)
- Extract UI structure and features
- Plan tasks like clicking, inputting, or retrying steps
- Dynamically call tools to assist with reasoning and interaction

---

### 🧠 Brain-Inspired Notes (Functional Analogy Only):
- **Visual Cortex Modules** ≈ V1–V4 → object, text, icon recognition  
- **Visual Semantic Layer** ≈ IT + associative cortex → forms structured understanding  
- **LLM + RAG + Tools** ≈ prefrontal cortex → question answering, reasoning, planning  
- **Executor** ≈ motor cortex → takes action, monitors feedback

---

## 🙏 Acknowledgments

We gratefully acknowledge the use of components, inspiration, or architectural references from open-source projects, including:

- **Microsoft’s [OmniParser](https://github.com/microsoft/OmniParser/tree/master)** – for its approach to document parsing and modular analysis of visual/textual structures in UI environments.  
  Parts of our visual cortex system (e.g., UI Object Detection, Feature Extraction) have been built upon or inspired by its structure.

We thank all open-source contributors and maintainers who made this research and experimentation possible.

---

---

## ⚖️ Legal and Usage Clarity

This project is experimental and intended for developers or researchers.  
It is not a plug-and-play product and may require environment configuration or patch updates.

We affirm:

- We use **our own code**, built on **open-source libraries** (YOLO, ResNet, EasyOCR, etc.).
- Our system interacts with **publicly accessible web UIs** like ChatGPT’s **as a user would**, through vision and keyboard/mouse simulation.
- We do **not** reverse-engineer, scrape undocumented APIs, or redistribute proprietary models.
- We do **not** impersonate, misuse, or misrepresent any affiliation with OpenAI.
- All behavior follows public web access patterns, and no internal OpenAI code or infrastructure is involved.
- This project is released under an open license and follows responsible OSS practices.

> ℹ️ If OpenAI or any party requests content takedown or usage clarification, we will engage constructively and respectfully.

---


## 📂 Related `cortex_vision` Module Components README Files

### 👁️ Attention and Focus
* **[ATTENTION_CONTROLLER_README.md](ATTENTION_CONTROLLER_README.md)** – Simulates human visual attention and focus  
* **[ATTENTION_CONTROLLER_EXTENDED_README.md](ATTENTION_CONTROLLER_EXTENDED_README.md)** – Extended attention control features  

### 🔄 Dynamic Area Detection
* **[README_DYNAMIC_AREA_DETECTOR.md](README_DYNAMIC_AREA_DETECTOR.md)** – Base dynamic area detection  
* **[README_UI_DYNAMIC_AREA_DETECTOR.md](README_UI_DYNAMIC_AREA_DETECTOR.md)** – UI-optimized dynamic area detection  
* **[ANCHOR_BASED_MAIN_AREA_README.md](ANCHOR_BASED_MAIN_AREA_README.md)** – Anchor-based main area detection  

### 🧩 Content Analysis
* **[README_content_detector.md](README_content_detector.md)** – Content-based segmentation system  
* **[README_image_similarity.md](README_image_similarity.md)** – Image/icon comparison using ResNet embeddings  
* **[README_IMAGE_DIFF_CREATOR.md](README_IMAGE_DIFF_CREATOR.md)** – Image difference detection  

### 📝 Task Automation
* **[task_schema_README.md](task_schema_README.md)** – Task schema framework  
* **[task_schema_generator_README.md](task_schema_generator_README.md)** – Task schema generation 

### 📊 Visualisations
* **[Execution Trace Visual Log](execution_visual_log.md)**
* **[All Cortex related Visual Logs](cortex_vision_all_viz.md)**

---

Each README provides detailed documentation for its respective component, including:
- Component overview and architecture  
- Implementation details and usage examples  
- Configuration options and parameters  
- Integration guidelines and best practices  
- Performance considerations and limitations  
- Testing and debugging information  

---

