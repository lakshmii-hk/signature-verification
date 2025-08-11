
# ✍ Signature Verification System  

A Python-based desktop application that verifies whether two signatures match using *OpenCV* image processing and *Tkinter* for the GUI. It uses *ORB feature detection* and a *FLANN-based matcher* to compare keypoints between the input and reference signatures.  

---

## 🚀 Features  
- 📂 Load and display input & reference signature images  
- 🔍 ORB-based feature extraction & FLANN-based matching  
- 📊 Displays match percentage and result (✅ Verified / ❌ Not Verified)  
- 🎨 User-friendly GUI with a clean layout and colors  

---

## 🛠 Installation  

1️⃣ *Clone this repository*  
```bash
git clone https://github.com/YOUR-USERNAME/signature-verification.git
cd signature-verification

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Run the application

python main.py


---

📦 Requirements

opencv-python
pillow

(tkinter comes pre-installed with Python on most systems.)


---

💡 Usage

1. 🖼 Click Load Input Signature → select the test signature image


2. 🖼 Click Load Reference Signature → select the original signature image


3. ✅ Click Verify Signature → view result & match percentage




---
