# Karna: Vision-Based UI Automation Framework

> **⚠️ EXPERIMENTAL ALERT:** This system is in early development and experimental phase. Components, implementations, and APIs may change significantly. Performance, accuracy, and reliability are being actively refined. Use for research and exploration purposes only.

This README combines two modules of the Karna system:

1. **[Karna Cortex Vision Module](cortex_vision.md)** – A biomimetic, modular system inspired by human vision for general UI automation.
2. **[ChatGPT Web Interface Automation](chatgpt_test_README.md)** – A practical implementation of Karna’s core vision stack for automating the ChatGPT interface.

---

## 🚀 Overview: Visual Automation Like a Human

Karna enables AI to automate any desktop application by perceiving and interacting with the user interface just like a human—through visual input, not APIs or code hooks.

At its core, Karna operates via:
- **Computer Vision**: Detect UI elements using image patches, OCR, and object detection.
- **Declarative Task Schemas**: Describe *what* to do, not how.
- **Mouse/Keyboard Simulation**: Control applications non-invasively.

Unlike fragile coordinate-based or DOM-selectors, Karna works across any OS or app—including legacy systems—with high resilience and portability.

---

## 🧠 Architecture: Mimicking the Human Visual Cortex

Karna modules mirror parts of the human brain:

| Brain Area | Vision Function | Module/Script | Tech Stack |
|------------|------------------|----------------|-------------|
| V1/V2 | Low-level features | `omniparser.py` | CNN-based OCR, YOLOv5, ResNet50 embeddings |
| V3/V4 | Form & color | `patch_matcher.py`, `image_comparison.py` | CNN similarity, pixel-level image diff |
| MT/V5 | Motion detection | `dynamic_area_detector.py`, `image_diff_creator.py` | Temporal differencing, heatmap generation |
| IT Cortex | Object grouping | `clustering.py`, `vertical_patch_matcher.py` | ResNet embeddings, hierarchical clustering |
| Parietal | Spatial attention | `attention_controller.py` | Attention field generation, spatial bias weighting |
| Prefrontal | Task memory | `task_schema.py`, `task_schema_generator.py` | JSON schema, declarative memory models |
| Frontal | Planning | `TaskPlanner` | Rule-based goal execution, step reasoning |
| Motor Cortex | Action | `TaskExecutor`, `clipboard_utils.py` | Mouse/keyboard simulation, system I/O |
| Association Cortex | Integration | `chatgpt_test.py` | Multimodal pipeline orchestration || Vision Function | Module/Script |


These modules process UI like the brain processes vision—bottom-up for saliency, top-down for goals.

---

## 🛠️ Practical Use: ChatGPT Web UI Automation

The `chatgpt_test.py` script shows how to automate ChatGPT's interface using only a **subset** of the full Karna stack:

- **Used**: `TaskSchema`, `TaskExecutor`, `VerticalPatchMatcher`, clipboard
- **Omitted**: `AttentionController`, `DynamicAreaDetector`, clustering (for simplicity/performance)

This design is **task-minimal** and pragmatic:
- UI is static → no need for motion detection
- Layout is known → patch matching suffices

### Features:
- Automates question submission and response capture
- Supports VLM mode (uploads image + text)
- Visualizes task execution
- Handles app switching

### Task Schema Execution:
```
TaskSchemaGenerator → _memory_generated.json + patches → TaskPlanner → TaskExecutor → Chrome UI Automation
```

---

## ✅ Benefits

| Benefit | Description |
|--------|-------------|
| Cross-App Automation | Works across any app without internal hooks |
| Human-Like | Uses mouse, keyboard, screen—no detectable bot signatures |
| Modular & Debuggable | Each stage (attention, detection, planning) can be isolated |
| Vision-Only | No need for APIs, DOM, or accessibility hooks |
| Theme-Aware | Patch-based detection supports light/dark UIs (with training) |

---

## ⚠️ Limitations

| Limitation | Description |
|------------|-------------|
| Theme Sensitivity | Schema trained in light mode may fail in dark mode |
| CAPTCHA/Popups | Not handled yet in `chatgpt_test.py` |
| No Gaze Tracking | Click history used as gaze proxy in attention modules |
| Not End-to-End Learning | Relies on hand-tuned configs and pre-trained models |

---

## 🧪 Developer Notes

Set these flags in `chatgpt_test.py` to use VLM mode and visualize steps:
```python
use_as_vlm = True
show_tasks_viz = True
directory_path = "test_chatgpt_upload_dir"
```

---

## 🧩 Vision Component Summary

| Component | Purpose |
|-----------|---------|
| `Omniparser` | OCR, YOLO-based detection of text and UI elements |
| `VerticalPatchMatcher` | Match patches visually to UI regions |
| `TaskSchema` | Declarative automation plan (JSON format) |
| `TaskExecutor` | Executes plan via vision + mouse/keyboard |
| `AttentionController` | Visual focus prioritization (optional) |
| `DynamicAreaDetector` | Detects changes in screen regions (optional) |

---

## 📦 File/Folder Structure (Example)
```
generated_task_schema_sample_chatgpt/
├── chat_with_chatgpt_steps_train_memory_generated.json
└── patches/
    ├── patch_step1.png
    ├── patch_step3.png
```

---

## 📚 Conclusion

Karna bridges the gap between traditional UI automation and AI-based visual interaction. Whether used to control complex multi-app workflows or simply to automate a chat window, its human-inspired architecture and modular design has the potential to make it adaptable, powerful, and future-proof.
