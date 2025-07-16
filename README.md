# NextHire.AI
NextHire.AI – An AI-powered web platform that simulates job interviews and provides real-time feedback.(🚧 In Progress)


NextHire.AI is an AI-powered web-based platform that simulates technical and behavioral job interviews. Built using Flask and integrated with Gemini API, it aims to help students and professionals practice interviews in a structured, realistic environment.


⚙️ Tech Stack
Frontend: HTML, CSS, JavaScript (Jinja2 Templating, CodeMirror IDE)
Backend: Python, Flask
AI Integration: Google Gemini API (for dynamic question generation + response feedback)

Upcoming: SQLite/Firestore (to store interview history), Scoring Logic, User Authentication


🔍 Features (Current)
🔹 Route-based interview flow via Flask

🔹 Gemini API integration for generating domain-specific questions

🔹 Interview type selection (DSA, HR, SQL, etc.)

🔹 🖥️ Integrated CodeMirror IDE for solving DSA questions during technical rounds

🔹 Planned voice/text I/O (partial implementation started)


🚧 Planned Features
✅ Structured interview flow (intro → Q&A → feedback)

✅ Scoring logic with final evaluation + strengths/weaknesses

🔐 User login/signup

💾 Store previous interviews in a database

📊 Dashboard with performance analytics

🎙️ Voice input/output using Web APIs or Python libraries


📁 Folder Structure

NextHire.AI/
├── app.py
├── templates/
│   ├── index.html
│   ├── interview.html
│   └── code_editor.html
├── static/
│   ├── style.css
│   ├── codemirror/
│   └── ...
├── requirements.txt
└── README.md


💻 How to Run Locally

git clone https://github.com/harshraj0049/NextHire.AI.git
cd NextHire.AI
pip install -r requirements.txt
python app.py
Open browser and go to http://localhost:5000


🛠️ Status
🚧 Work in Progress: Core interview logic and Gemini integration are functional. IDE environment is integrated for technical rounds. Full feedback system, database storage, and dashboard are coming soon.
