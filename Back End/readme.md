# VQA  Application

This directory contains the **backend** implementation of the Text-to-Speech (TTS) application. The backend handles core functionalities such as text processing, audio generation, and language translation.

---

## Features
* Text-to-Speech processing using the `gtts` library.
* Language translation with the `googletrans` library.
* API support for frontend-backend communication.

---

## Prerequisites
* Python 3.7 or above installed.

---

## Setup

1. Clone the repository and navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   streamlit run apps.py
   ```

---

## File Structure
```
backend/
├── apps.py          # Main Streamlit application
├── requirements.txt # Dependencies for the backend
└── ...other files
```

---

## Future Enhancements
* Optimize API responses for faster processing.
* Add support for additional audio formats.
* Deploy the backend to a cloud platform for scalability.

---
