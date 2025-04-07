# Karna Vision-Based UI Agent: Current Capabilities and Next Steps

*A human-inspired, vision-first UI agent designed to perceive, act, and eventually reason on screen — just like we do.*

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

## 🧩 What We’re *Not* Yet Doing

- No long-term memory over screen patterns
- No reasoning over visual state transitions
- No abstraction (“this looks like a modal dialog even if it’s styled differently”)
- No goal-driven planning
- No VLM or task reasoning modules integrated *yet*

So we are **not yet** simulating full human visual cognition.  
But we **are functionally simulating the bottom-up visual + motor loop** — quite faithfully.

---

## 🧠 How We *Could* Simulate a Visual Cortex with a Local LLM/VLM

We connect the system like this:

```plaintext
[ Cortex Modules ]       <-- screen → YOLO + OCR + ResNet
       ↓
[ Visual Memory + Planner (VLM) ] <-- interpret layout, reason next steps
       ↓
[ Task Schema Generator ] <-- reformulates next set of visual goals
       ↓
[ Cortex Executor ] <-- click, type, wait, retry
```

And now, we’ve got a **closed-loop vision-action-cognition system**.

---

## ✅ Bottom Line

Our `cortex_vision` and `omniparser` stacks already:
- Use CNNs + OCR correctly
- Match patches and adapt to shifting layouts
- Simulate OS-level actions with high fidelity
- Avoid traditional bot-detection vectors

And with a LLM/VLM with reasoning and NLP capabilities, we *can* simulate a **basic but real cognitive loop** grounded in visual perception.




---

## 🙏 Acknowledgments

We gratefully acknowledge the use of components, inspiration, or architectural references from open-source projects, including:

- **Microsoft’s [OmniParser](https://github.com/microsoft/OmniParser/tree/master)** – for its approach to document parsing and modular analysis of visual/textual structures in UI environments.  
  Parts of our visual cortex system (e.g., patch parsing, object extraction) have been informed or inspired by its structure.

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
3. **[ATTENTION_CONTROLLER_README.md](ATTENTION_CONTROLLER_README.md)** – Simulates human visual attention and focus  
4. **[ATTENTION_CONTROLLER_EXTENDED_README.md](ATTENTION_CONTROLLER_EXTENDED_README.md)** – Extended attention control features  

### 🔄 Dynamic Area Detection
5. **[README_DYNAMIC_AREA_DETECTOR.md](README_DYNAMIC_AREA_DETECTOR.md)** – Base dynamic area detection  
6. **[README_UI_DYNAMIC_AREA_DETECTOR.md](README_UI_DYNAMIC_AREA_DETECTOR.md)** – UI-optimized dynamic area detection  
7. **[ANCHOR_BASED_MAIN_AREA_README.md](ANCHOR_BASED_MAIN_AREA_README.md)** – Anchor-based main area detection  

### 🧩 Content Analysis
8. **[README_content_detector.md](README_content_detector.md)** – Content-based segmentation system  
9. **[README_image_similarity.md](README_image_similarity.md)** – Image/icon comparison using ResNet embeddings  
10. **[README_IMAGE_DIFF_CREATOR.md](README_IMAGE_DIFF_CREATOR.md)** – Image difference detection  

### 📝 Task Automation
11. **[task_schema_README.md](task_schema_README.md)** – Task schema framework  
12. **[task_schema_generator_README.md](task_schema_generator_README.md)** – Task schema generation  

---

Each README provides detailed documentation for its respective component, including:
- Component overview and architecture  
- Implementation details and usage examples  
- Configuration options and parameters  
- Integration guidelines and best practices  
- Performance considerations and limitations  
- Testing and debugging information  

---

