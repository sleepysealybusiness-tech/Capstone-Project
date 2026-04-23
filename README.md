# AI Text Summarizer (Flask + Groq)

This project is a Python Flask web application that accepts uploaded `.txt` files, sends their contents to the Groq API, and displays both the original content and a summarized result.

## Features

- Upload `.txt` files from the browser
- Validate file type, empty uploads, and file size
- Summarize content with Groq
- Display original text and summary side-by-side
- Show clear success/error messages in the UI

## Project Structure

```text
Capstone-Project/
├── app.py
├── templates/
│   ├── base.html
│   └── index.html
├── static/
│   └── css/
│       └── style.css
├── requirements.txt
└── README.md
```

## Setup

### 1) Create and activate a virtual environment

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Set environment variables

Set your Groq API key (required):

```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
```

Optional (recommended) Flask secret key:

```powershell
$env:FLASK_SECRET_KEY="a_long_random_secret"
```

### 4) Run the app

```powershell
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Notes

- Only UTF-8 encoded `.txt` files are accepted.
- Maximum file size is 2 MB.
