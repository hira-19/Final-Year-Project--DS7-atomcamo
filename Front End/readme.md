# Visual Question Answering Application

This repository contains a **Text-to-Speech (TTS) web application** built with a separate **backend** and **frontend** architecture. The backend, developed with Streamlit, handles text processing and audio generation, while the frontend, designed using Bootstrap and JavaScript, provides an intuitive user interface.

---

## Project Structure

```
project_root/
├── backend/     # Backend implementation using Streamlit
├── frontend/    # Frontend implementation using Bootstrap and JavaScript
└── README.md    # Project documentation
```

---
## 1 Frontend

The frontend provides a user-friendly interface for the application, implemented using **Bootstrap** and **JavaScript**.

### Features
- Text input box for user input.
- Buttons for processing and audio playback.
- Responsive design suitable for desktop and mobile devices.

### Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Open the `index.html` file in a web browser:
   ```
   open index.html
   ```

### File Structure
```
frontend/
├── index.html       # Main HTML file
├── styles.css       # Custom CSS 
├── script.js        # JavaScript for handling UI interactions
└── assets/          # Folder for additional resources like images or icons
```

## 3. Audio Integration

Currently, there is an issue with integrating audio playback between the backend and frontend. The backend generates the audio file successfully, but the frontend needs to fetch and play it dynamically.


## Future Enhancements
- Resolve audio integration issues between backend and frontend.
- Add support for additional languages and voices.
- Deploy the complete application to a cloud platform.
- Enhance the user interface for accessibility and aesthetics.

