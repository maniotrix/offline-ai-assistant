#### Todo 
    add support to view the computer in real time over network
    threading for frontend communication and background tasks in backend, like updating websocket connection
    Do not use dict for communication within the backend
    use separate executor module for processing different stuff in backend pipeline or as required
    look out for improvement in websocket

Okay, here's a comprehensive summary detailing the design and implementation of our personal, vision-based offline AI assistant project. This includes the progression of our architectural choices and the reasoning behind them:

**I. Project Overview:**

The goal is to develop a personal AI assistant that can automate tasks on a user's computer, operating offline and learning from user interactions. The assistant primarily relies on visual input (screenshots) to understand context and intent. It should be adaptable to a single website, transferrable across devices, and require minimal initial setup.

**II. Core Requirements:**

*   **Personalized:** Tailored to the individual user's workflow and preferences.
*   **Vision-Based:** Uses screenshots of the user's screen as primary input.
*   **Offline Operation:** Functions without an internet connection for privacy and reliability.
*   **Autonomous:** Operates proactively, anticipating user needs.
*   **Learning:** Continuously learns from user interactions, feedback, and demonstrations.
*   **Automation:** Performs tasks on behalf of the user (e.g., filling forms, clicking buttons).
*   **Transferable:** Seamlessly moves learned knowledge and configuration between devices.

**III. Architectural Evolution and Design Choices:**

The architecture evolved through several iterations, driven by considerations of data availability, resource constraints, and performance goals.

*   **Initial Approach (Modular):**

    *   **Rationale:** A modular design allows for separate development and testing of individual components.
    *   **Components:**
        *   *Screen Capture Module:* Captures screenshots of the user's screen.
        *   *Vision Processing & Understanding Module:* Identifies UI elements (YOLO), extracts text (OCR), analyzes layout.
        *   *NLP & Intent Recognition Module (SmolLM2):* Processes user commands and determines intent.
        *   *Action Execution Module:* Simulates user actions (mouse clicks, keyboard input).
        *   *Learning & Adaptation Module:* Learns from user interactions and feedback.
        *   *Data Storage & Management:* Stores screenshots, annotations, and learned models.
    *   **Learning:** Utilized a combination of supervised learning, reinforcement learning, and imitation learning.
    *   **Transferability:**  Achieved through model serialization (saving model weights to a file).
    *   **Limitations:** Complex interactions between modules; potential for error propagation; heavy computational requirements for offline operation.

*   **Refined Action Space:**

    *   **Rationale:** Improve robustness and generalizability by moving away from pixel-based coordinates to semantic descriptions of UI elements.
    *   **Action Space:** (action\_type, target\_element), where target\_element includes location, type, OCR text, and image/icon description.

*   **Sectional (End-to-End) Model:**

    *   **Rationale:** Simplify the architecture and enable joint optimization.
    *   **Architecture:** Single model with vision encoder, text encoder, fusion module, and action decoder.
    *   **Learning:** Trained with a combination of cross-entropy loss for action type prediction and MSE loss for coordinate prediction.

*   **Few Shot and RAG:**

    *   *Few Shot training/data augmentation was used in some areas
    *   Was able to handle long range requests using rag
    *   Was easily interpretable

*   **Data-Constrained Learning (One-Shot with User Feedback):**

    *   **Rationale:** Adapt to the scenario of very limited initial training data (only user corrections).
    *   **Learning Strategy:** Leverage pre-trained models; freeze the weights of base models; prompt engineering for initial inference

*   **Seamless Transferability and Continual Learning (Final Design):**

    *   **Rationale:** Combine the benefits of limited shot with seamless transferability and the ability to learn over time.
    *   **Learning Process:** Load all model weights into a singular container, then use the users feedback to inject additional data and training while continuing the loop

**IV. Key Components and Implementation Details:**

*   **Screen Capture Module:**
    *   Platform-specific APIs (DirectX, Metal, X11) for efficient screen capture.
    *   Privacy features to exclude sensitive areas.
*   **Vision Processing & Understanding Module:**
    *   *YOLO:* Object detection of UI elements.
    *   *Tesseract OCR:* Text extraction.
    *   *LayoutParser:* Document Layout Analysis.
    *   *Image Captioning (BLIP or GIT):* Describing images and icons.
    *   Libraries: `torchvision`, `pytesseract`, LayoutParser, Hugging Face Transformers.
*   **NLP & Intent Recognition Module (SmolLM2 or similar):**
    *   Processes user commands and determines intent.
    *   Fine-tuned on web automation tasks.
    *   Library: Hugging Face Transformers.
*   **Action Execution Module:**
    *   Simulates mouse clicks and keyboard input.
    *   Libraries: `pyautogui`, Selenium (for web browsers).
*   **Learning & Adaptation Module:**
    *   Continual learning techniques to update the model with new data and prevent catastrophic forgetting.
    *   Replay buffer to store past experiences.
*   **Data Storage & Management:**
    *   Local database (SQLite or RocksDB) to store screenshots, annotations, and models.
*   **Device Transfer:**
    *   Model serialization (torch.save) to save the entire model.
*   **High-Level Structure:**

    *   The project will use modules and functions in order to orchestrate the results to provide better responses. It will include helper functions that perform similar actions.
    *   Prompts are created in this part

**V. Training Process and Techniques:**

*   **Data Acquisition:** Leverage existing pre-trained models and manually correct annotations.
*   **Learning Strategy:** Few-shot learning, fine-tuning, prompt-tuning, and PEFT techniques.
*   **Training Loop:**
    *   Pre-training Vision and Text Encoders on General Datasets (e.g., ImageNet, WebText).
    *   One-Shot Learning with User Correction.
    *   Evaluate Action Sequence Accuracy, Action Accuracy, Task Completion Rate, and Inference Time.

**VI. Model Evaluation:**

*   *Action Sequence Accuracy:* Percentage of correctly predicted action sequences.
*   *Action Accuracy:* Percentage of correct actions at each step.
*   *Task Completion Rate:* Percentage of tasks successfully completed.
*   *Inference Time:*  Average time to predict the next action.

**VII. Transferability:**

*   *Model Serialization:*  Use PyTorch's `torch.save` to save the entire model state.

**VIII. Challenges and Considerations:**

*   *Tradeoffs*: Prioritization between model accuracy, training time, inference speed, and data requirements.
*   *Hardware* and memory
*   *Data Quality*: Accuracy of object detection, OCR, and image captioning.
*   *Website Changes*: Implement strategies to adapt to changes in website layouts and functionality.
*   *Ambiguity Handling:* The system must be able to handle ambiguity in user instructions and visual input.

**IX. Directory Structure**

```
Offline_AI_Assistant/
├── data/                # Data storage (screenshots, annotations, etc.)
│   ├── screenshots/     # Store screenshots organized by task and step
│   │   ├── task1/       # Task 1: e.g., "Search cats on YouTube"
│   │   │   ├── step1.png
│   │   │   ├── step2.png
│   │   │   └── ...
│   │   ├── task2/
│   │   │   └── ...
│   ├── annotations/     # Store annotation data (JSON files)
│   │   ├── task1/
│   │   │   ├── step1.json # Annotations for step1.png
│   │   │   ├── step2.json
│   │   │   └── ...
│   │   ├── task2/
│   │   │   └── ...
│   └── prompts/         # Store prompts used with LLMs
│       ├── rag_prompts.txt   # Examples for Rag based code
├── models/               # Trained models and configuration
│   ├── vision/          # Vision models (YOLO, ScreenEncoder)
│   │   ├── yolo_model/  # Saved YOLO model
│   │   │   ├── weights.pth
│   │   │   ├── config.yaml
│   │   ├── screen_encoder/ # Saved ScreenEncoder model
│   │   │   ├── weights.pth
│   │   │   ├── config.json
│   ├── language/        # Language models (SmolLM2, action predictor)
│   │   ├── smol_lm2/    # Saved fine-tuned SmolLM2
│   │   │   ├── weights.pth
│   │   │   ├── tokenizer/
│   │   │   │   ├── ...
│   │   │   ├── config.json
│   │   ├── action_predictor/ # Action prediction model
│   │   │   ├── weights.pth
│   │   │   ├── config.json
│   ├── model.pth        # Top level system weights saved when used as a module for seamless transfer
├── modules/              # Implementation of components
│   ├── screen_capture.py  # Screen capture module
│   ├── vision_agent.py    # Screen vision agent module
│   ├── action_execution.py # Action execution module (pyautogui, etc.)
│   ├── action_prediction.py # Action prediction module
│   ├── prompt_engineering.py # Pormpt and response handling
├── scripts/
│   ├── data_collection.py # User interaction capture
│   ├── training_script.py # script to train models
│   ├── evaluation_script.py # Script to evaluate model performance
├── utils/                # Utility functions (data loading, etc.)
│   ├── data_utils.py
│   ├── model_utils.py
├── requirements.txt      # Project dependencies
├── README.md
└── main.py               # Main script to run the assistant
```

**X. Conclusion:**

This project aims to create a personal AI assistant capable of automating tasks offline. The key challenges lie in balancing accuracy, efficiency, and generalizability with limited data and computational resources. While the initial code and models can be retrieved from many sources as pre-trained weights, all weights that are loaded onto the model *must* be transferred in order to achieve the seamless integration described. The system must also be modular so that we are able to test, evaluate, and replace when needed.