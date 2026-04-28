import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import google.generativeai as genai
import cv2
from PIL import Image, ImageTk
import numpy as np
# from deepface import DeepFace
import random

genai.configure(api_key=' ADD YOUR API KEY HERE ')


class SmartInterviewChatbot:
    def __init__(self, master):
        self.master = master
        self.master.title("Smart Interview Chatbot")
        self.master.geometry("1000x700")
        self.master.configure(bg="#1A1A1A")  # Dark background

        self.chat_history = []
        self.question_count = 0
        self.is_student = None
        self.camera_on = False
        self.emotion_data = []
        self.confidence_levels = []

        self.create_widgets()

    def create_widgets(self):
        self.welcome_frame = tk.Frame(self.master, bg="#1A1A1A")
        self.welcome_frame.pack(expand=True, fill=tk.BOTH)

        welcome_label = tk.Label(self.welcome_frame, text="Welcome to Smart Interview Chatbot", font=(
            "Helvetica", 28, "bold"), bg="#1A1A1A", fg="#ECF0F1")
        welcome_label.pack(pady=20)

        motivation_quotes = [
            "Believe you can and you're halfway there.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "The only way to do great work is to love what you do.",
            "Your time is limited, don't waste it living someone else's life.",
            "The future belongs to those who believe in the beauty of their dreams."
        ]
        motivation_label = tk.Label(self.welcome_frame, text=random.choice(motivation_quotes), font=(
            "Helvetica", 16, "italic"), bg="#1A1A1A", fg="#3498DB", wraplength=600)
        motivation_label.pack(pady=20)

        start_button = tk.Button(self.welcome_frame, text="Start Interview", command=self.start_interview, bg="#E74C3C", fg="white", font=(
            "Helvetica", 18, "bold"), padx=30, pady=15, relief=tk.RAISED, borderwidth=3)
        start_button.pack(pady=30)

        self.main_frame = tk.Frame(self.master, bg="#1A1A1A")

        self.camera_frame = tk.Label(self.main_frame, bg="#2C3E50")
        self.camera_frame.place(x=10, y=10, width=240, height=180)

        self.emotion_label = tk.Label(self.main_frame, text="", font=(
            "Helvetica", 12), bg="#1A1A1A", fg="#ECF0F1")
        self.emotion_label.place(x=10, y=200)

        self.chat_frame = tk.Frame(self.main_frame, bg="#2C3E50")
        self.chat_frame.place(x=260, y=10, relwidth=0.7, relheight=0.8)

        self.chat_display = tk.Text(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED,
                                    bg="#2C3E50", fg="#ECF0F1", font=("Helvetica", 14))
        self.scrollbar = ttk.Scrollbar(
            self.chat_frame, orient=tk.VERTICAL, command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=self.scrollbar.set)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.input_frame = tk.Frame(self.main_frame, bg="#1A1A1A")
        self.input_frame.place(x=260, rely=0.85, relwidth=0.7, relheight=0.15)

        self.user_input = tk.Entry(self.input_frame, font=(
            "Helvetica", 14), bg="#34495E", fg="#ECF0F1", insertbackground="#ECF0F1")
        self.user_input.pack(side=tk.LEFT, expand=True,
                             fill=tk.BOTH, padx=(0, 10))

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message,
                                     bg="#2ECC71", fg="white", font=("Helvetica", 12, "bold"))
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.camera_button = tk.Button(self.main_frame, text="Turn On Camera",
                                       command=self.toggle_camera, bg="#3498DB", fg="white", font=("Helvetica", 12, "bold"))
        self.camera_button.place(x=10, y=230)

        self.end_button = tk.Button(self.main_frame, text="End Interview", command=self.end_interview,
                                    bg="#E74C3C", fg="white", font=("Helvetica", 12, "bold"))
        self.end_button.place(x=10, y=270)

    def start_interview(self):
        self.welcome_frame.pack_forget()
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.add_message(
            "Chatbot", "Welcome to the interview simulation! Let's start with a brief introduction. Are you currently a student or do you have professional experience?")

    def add_message(self, sender, message):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self):
        user_message = self.user_input.get()
        if user_message:
            self.add_message("You", user_message)
            self.user_input.delete(0, tk.END)
            self.process_user_input(user_message)

    def process_user_input(self, user_message):
        if self.is_student is None:
            self.is_student = "student" in user_message.lower()
            self.add_message(
                "Chatbot", "Great! Let's begin. Please introduce yourself briefly.")
        else:
            self.chat_history.append(f"User: {user_message}")
            self.question_count += 1
            next_question = self.get_next_question()
            self.chat_history.append(f"Chatbot: {next_question}")
            self.add_message("Chatbot", next_question)

    def get_next_question(self):
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""
        Based on the following chat history and user profile, generate the next appropriate interview question:
        
        User is a {'student' if self.is_student else 'professional'}
        Chat history: {' '.join(self.chat_history)}
        Current question count: {self.question_count}

        Rules:
        1. Ask only one question at a time.
        2. Do not repeat questions.
        3. For students, focus on educational background, projects, and career aspirations.
        4. For professionals, focus on work experience, challenges, and career growth.
        5. Include some technical or coding questions appropriate for the candidate's background.
        6. Ensure questions are relevant to the desired position (which should be inferred from the conversation).
        7. Keep the tone professional but friendly.
        8. Do not ask about experience if the user is a student.
        9. Focus more on asking questions related to the desired position.

        Generate the next question:
        """

        response = model.generate_content(prompt)
        return response.text

    def toggle_camera(self):
        if not self.camera_on:
            self.camera_on = True
            self.camera_button.config(text="Turn Off Camera")
            self.start_camera()
        else:
            self.camera_on = False
            self.camera_button.config(text="Turn On Camera")
            self.cap.release()
            self.camera_frame.configure(image='')
            self.emotion_label.config(text="")

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    def update_camera(self):
        if self.camera_on:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (240, 180))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_frame.imgtk = imgtk
                self.camera_frame.configure(image=imgtk)

                try:
                    result = DeepFace.analyze(
                        frame, actions=['emotion'], enforce_detection=False)
                    emotion = result[0]['dominant_emotion']
                    confidence = result[0]['emotion'][emotion]
                    self.emotion_data.append(emotion)
                    self.confidence_levels.append(confidence)
                    self.emotion_label.config(
                        text=f"Current emotion: {emotion.capitalize()} (Confidence: {confidence:.2f}%)")
                except:
                    pass

            self.master.after(100, self.update_camera)

    def end_interview(self):
        self.add_message(
            "Chatbot", "Thank you for participating in this interview simulation. Would you like to receive feedback on your performance?")
        self.end_button.configure(
            text="Get Feedback", command=self.provide_feedback)

    def provide_feedback(self):
        feedback_prompt = f"""
        Analyze the following interview conversation and provide constructive feedback:
        
        {' '.join(self.chat_history)}
        
        Emotion data: {self.emotion_data}
        Confidence levels: {self.confidence_levels}
        
        Evaluate if the candidate's answers are good enough to pass an interview. Offer personalized tips for improvement, suggest relevant courses if necessary, and comment on the overall performance. Include tips on dressing etiquette for interviews. Provide specific areas for improvement. 

        Analyze the emotion data and confidence levels, providing detailed feedback on the candidate's emotional state and confidence during the interview. Offer specific suggestions for improving confidence and maintaining a positive emotional state during interviews.

        Calculate and include the overall confidence level based on the confidence levels data. Provide a percentage and a qualitative assessment (e.g., "Your overall confidence level was 75%, which is good but there's room for improvement."). Offer tailored advice on how to boost confidence for future interviews.
        """

        model = genai.GenerativeModel('gemini-2.0-flash')
        feedback = model.generate_content(feedback_prompt)

        feedback_window = tk.Toplevel(self.master)
        feedback_window.title("Interview Feedback")
        feedback_window.geometry("600x500")
        feedback_window.configure(bg="#1A1A1A")

        feedback_text = tk.Text(feedback_window, wrap=tk.WORD, font=(
            "Helvetica", 14), bg="#2C3E50", fg="#ECF0F1")
        feedback_text.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        feedback_text.insert(tk.END, feedback.text)
        feedback_text.configure(state=tk.DISABLED)

        download_button = tk.Button(feedback_window, text="Download Feedback", command=lambda: self.download_feedback(
            feedback.text), bg="#3498DB", fg="white", font=("Helvetica", 14, "bold"))
        download_button.pack(pady=20)

    def download_feedback(self, feedback):
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(feedback)
            messagebox.showinfo("Download Complete",
                                f"Feedback has been saved to {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartInterviewChatbot(root)
    root.mainloop()
