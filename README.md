# IntelliInterview — Smart Interview Bot

> AI-powered mock interview simulator with real-time emotion detection and personalized feedback.

## What it does
IntelliInterview simulates realistic job interview scenarios through a conversational AI chatbot. It adapts its questions based on whether the candidate is a student or working professional, analyzes facial expressions via webcam in real-time, and provides detailed post-interview feedback on both content and emotional performance.

## Key Features
- **Aaptive questioning** — Dynamically generates role-relevant questions using Google Gemini API, tailored to the candidate's background and previous answers
- **Emotion detection** — Live webcam analysis using DeepFace + OpenCV detects confidence, nervousness, anxiety during the interview
- **Real-time feedback** — Tracks confidence levels throughout the session
- **Post-interview report** — AI-generated feedback covering answer quality, emotional state, confidence score, and improvement suggestions
- **Downloadable feedback** — Users can save their performance report as a .txt file

## Tech Stack
| Language | Python |
| UI | Tkinter |
| AI / LLM | Google Gemini API (gemini-2.0-flash) |
| Emotion Detection | DeepFace, OpenCV |
| Image Processing | Pillow, NumPy |

## How it works
1. User starts a session and specifies if they are a student or professional
2. Chatbot generates dynamic interview questions via Gemini API based on conversation history
3. Webcam activates (optional) — DeepFace detects dominant emotion every 100ms
4. After the interview, AI analyzes the full conversation + emotion log and generates personalised feedback
5. Feedback can be downloaded as a report

## Screenshots

<img width="1919" height="1137" alt="Screenshot 1" src="https://github.com/user-attachments/assets/167e8cc9-1723-4be6-a5a1-f53aed31c23e" />
<img width="1920" height="1128" alt="Screenshot 3" src="https://github.com/user-attachments/assets/d452aa89-8ef9-4b94-b475-df1ea29c8139" />
<img width="902" height="798" alt="Screenshot 7" src="https://github.com/user-attachments/assets/036cd0f8-98f9-4fa9-8953-d17fad15bd5e" />
<img width="1920" height="1128" alt="Screenshot 5" src="https://github.com/user-attachments/assets/7d5c059d-3257-48a3-8b7f-36b18aecd24e" />

## My Role
Led a team of 3 as part of our Minor Project (B.E. Information Technology, Vidyalankar Institute of Technology, 2024–25). Responsible for product direction, feature scoping, system architecture, and coordinating development.

**Team:** Sampurna Prabhu · Gargi Kshirsagar · Anushka Thacore
**Supervisor:** Prof. Rohit Barve

## Results
- 88% accuracy in evaluating interview responses vs human interviewers (tested on 500 mock cases)
- 85% of users found feedback useful for improving interview performance
- 4.6/5 usability score across 50 test participants

## Future Scope
- Voice analysis for tone, pitch, and speech clarity
- Mobile app version
- Multilingual support
- More advanced emotion recognition models
