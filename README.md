# deepfake-detection-Phase-01
Classical Forensic-Based Deepfake Detection

This project is a **Deepfake Detection System** designed to analyze **images and videos** and identify whether a **face has been manipulated or swapped**.  
The system works using **classical computer vision and digital image forensics techniques** — **without using any AI or machine learning models**.

It is intended as a **Phase-1 prototype** for learning, experimentation, and academic demonstration.

---

## What Does This System Actually Do?

This system **does NOT recognize people or verify identity**.

Instead, it performs **forensic analysis** to detect **visual inconsistencies** that are commonly introduced during **face-swap or deepfake generation**.

In simple terms:

The system checks whether a face *looks naturally consistent* or *shows signs of digital manipulation*.

---

## 🔍 How the Detection Works (Core Logic)

The system follows a **multi-step forensic pipeline**:

### 1 Face Detection
- Uses **Haar Cascade (OpenCV)** to detect faces in images or video frames.
- Only the **face region** is extracted.
- Background, clothing, and surroundings are ignored.

This prevents false similarity caused by similar backgrounds.

---

### 2 Face Region Normalization
- The detected face is:
  - Cropped tightly
  - Resized to a fixed resolution
  - Converted to grayscale where required

This ensures **fair and consistent comparison**.

---

### 3 Structural Similarity Analysis (SSIM)
- Measures **visual similarity** between two face images.
- Detects differences in:
  - Texture
  - Structure
  - Contrast

SSIM does **not** detect identity — only visual consistency.

---

### 4 Color Consistency Analysis
- Compares **skin color distributions** using color histograms.
- Face swaps often introduce subtle color mismatches due to:
  - Blending
  - Lighting differences
  - Skin tone mismatch

This is a **strong indicator of face replacement**.

---

### 5 Frequency Domain Analysis (FFT)
- Analyzes the image in the **frequency domain**.
- Deepfake models often:
  - Over-smooth skin
  - Remove high-frequency details

This step helps detect **AI-generated smoothing artifacts**.

---

### 6 Edge & Sharpness Analysis
- Uses edge density and Laplacian variance.
- AI-generated faces often show:
  - Unnatural smoothness
  - Reduced fine details

---

### 7 Risk Scoring & Verdict
All forensic signals are **combined using rule-based logic** to compute:

- **Deepfake Risk Percentage**
- **Human-readable verdict**
  - `Likely Same Real Face`
  - `Likely Manipulated / Face Swap`

No randomness, no black-box decisions.

---

## Result

First, an image of the original person is uploaded (usually a celebrity or well-known individual, since deepfake images commonly involve public figures), for example:

![Orignal picture](images/pics/target_03.jpeg)

Next, the suspected image is uploaded, where the face may have been swapped or manipulated using a celebrity’s face, for example:

<img src="images/pics/swap_03.jpeg" width="200" height="300" />


After uploading both images, the system performs face-only forensic analysis and generates a JSON-based result containing structural similarity, manipulation risk, and an overall verdict.

Sample result output:
You can view the generated JSON result here:
[Report](images\report\result.txt)

## What This System Is Good At

 Detecting face swaps  
 Identifying manipulation artifacts  
 Educational and academic use  
 Explainable forensic decisions  
 Lightweight & fast execution  

---

## What This System Does NOT Do

- Identity recognition  
- Face authentication  
- Legal or court-grade verification  
- AI model training  
- Dataset-based learning  

---

## Technologies Used

- **Python**
- **Flask** – Web backend
- **OpenCV** – Face detection & image processing
- **NumPy** – Numerical computation
- **Scikit-Image** – SSIM computation
- **Chart.js** – Visual risk charts (frontend)

---

## Project Intent

This project is designed for:
- Students
- Cybersecurity learners
- Digital forensics practice
- Phase-1 deepfake research

It serves as a **foundation** that can later be extended with **pretrained AI models** in future phases.

---

## Future Enhancements (Optional)

- Facial landmark ratio analysis
- Temporal consistency checks for videos
- Pretrained deep learning embeddings (no training)
- Automated forensic report generation
- Tampering heatmaps

---

## Final Note

This system focuses on **detecting manipulation**, not identifying people.

That distinction is **intentional, ethical, and technically accurate**.

---

