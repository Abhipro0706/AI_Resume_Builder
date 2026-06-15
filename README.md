# ✦ ResumeAI — AI Resume & Portfolio Builder

> **An AI-powered career document generator for students built with Streamlit + Groq (LLaMA 3.3)**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Free](https://img.shields.io/badge/API-100%25%20Free-brightgreen?style=flat-square)

---

## 📌 Problem Statement

Many students struggle to present their skills and projects in an attractive, professional format. Generic resume templates don't highlight individual strengths. This AI-powered solution automatically generates tailored resumes, cover letters, and portfolios based on student data — improving job and internship opportunities.

---

## 🚀 Live Demo

🔗 **[Try the App](https://ai-resume-builder-yourname.streamlit.app)**

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Resume Generator** | ATS-optimised resumes in 4 styles and 3 formats |
| ✉️ **Cover Letter Writer** | Personalised cover letters with tone control |
| 🌐 **Portfolio Builder** | Complete HTML portfolio website — downloadable |
| 💡 **Interview Prep Kit** | Custom Q&A with STAR method answers |
| 🔍 **Resume Analyzer** | Score /100 + actionable feedback on existing resumes |

---

## 🛠️ Tech Stack

- **Frontend & Backend** — Streamlit
- **AI Model** — LLaMA 3.3 70B via Groq API (Free)
- **Language** — Python 3.9+
- **Deployment** — Streamlit Community Cloud

---

## 📁 Project Structure

```
ai-resume-builder/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
└── README.md           ← Project documentation
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-resume-builder.git
cd ai-resume-builder
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get Free Groq API Key
- Go to **console.groq.com**
- Sign up → API Keys → Create Key
- Copy the key (starts with `gsk_...`)

### 5. Run the App
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🔑 API Key Setup

### For Local Use
Paste your Groq API key directly in the app sidebar.

### For Deployment (Streamlit Cloud)
Go to **App Settings → Secrets** and add:
```
GROQ_API_KEY = "gsk_your_key_here"
```

---

## 📸 Screenshots

### Home Page
![Home](https://via.placeholder.com/800x400?text=ResumeAI+Home+Page)

### Resume Generator
![Resume](https://via.placeholder.com/800x400?text=Resume+Generator)

### Cover Letter
![Cover Letter](https://via.placeholder.com/800x400?text=Cover+Letter+Writer)

---

## 🎯 How to Use

1. **Enter API Key** — Paste your free Groq key in the sidebar
2. **Fill Profile** — Add your education, skills, projects, experience
3. **Click Save Profile**
4. **Choose a Tab** — Resume / Cover Letter / Portfolio / Interview Prep / Analyzer
5. **Generate** — Get your AI-crafted document in seconds
6. **Download** — Save as .txt or .html file

---

## 🌐 Deploy Your Own

### Streamlit Community Cloud (Free)
1. Fork this repository
2. Go to **share.streamlit.io**
3. Connect your GitHub → Select this repo
4. Set main file: `app.py`
5. Add your Groq API key in Secrets
6. Click Deploy ✅

---

## 💡 Future Enhancements

- [ ] PDF export for resumes
- [ ] LinkedIn profile auto-fill
- [ ] Multiple resume version saving
- [ ] Email cover letter directly
- [ ] Dark mode toggle
- [ ] Resume templates gallery

---

## 👨‍💻 Author

**Abhinav Patel**
- GitHub: [@yourusername](https://github.com/abhipro0706)


---

## 📄 License

This project is licensed under the MIT License — free to use and modify.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io) — for the amazing web framework
- [Groq](https://groq.com) — for the free and blazing fast LLM API
- [Meta LLaMA](https://llama.meta.com) — for the open source LLaMA 3.3 model

---

⭐ **If this project helped you, please give it a star on GitHub!**
