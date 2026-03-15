import tkinter as tk
from tkinter import messagebox
import random

# -----------------------------
# Questions database
# -----------------------------
questions = [
    # Minecraft questions
    {"question": "Which block is used to craft a crafting table?",
     "options": ["Stone", "Wood", "Iron Block", "Sand"], "answer": "B"},
    {"question": "Which mob does NOT burn in daylight?",
     "options": ["Zombie", "Creeper", "Skeleton", "Enderman"], "answer": "D"},
    {"question": "Which is the hardest block in Minecraft?",
     "options": ["Stone", "Diamond Ore", "Bedrock", "Lapis Lazuli Ore"], "answer": "C"},
    {"question": "Which material is used to craft an Enchanting Table?",
     "options": ["Emerald", "Obsidian", "Redstone", "Gold Ingot"], "answer": "B"},
    {"question": "In Creative Mode, does the player take damage?",
     "options": ["Yes", "No", "Sometimes", "Not sure"], "answer": "B"},
    # Minecraft Dungeons
    {"question": "Which artifact in Minecraft Dungeons shoots a fireball?",
     "options": ["Soul Healer", "Fireworks Arrow", "Cursed Bow", "Fireworks Rocket"], "answer": "D"},
    {"question": "Which enemy appears as the final boss in the default campaign?",
     "options": ["Arch-Illager", "Redstone Golem", "Evoker", "Creeper King"], "answer": "A"},
    {"question": "Which gear increases your movement speed?",
     "options": ["Boots of Swiftness", "Golden Armor", "Heart of the Sea", "Chainmail Boots"], "answer": "A"},
    {"question": "What is the default currency in Minecraft Dungeons?",
     "options": ["Gold", "Emeralds", "Coins", "Diamonds"], "answer": "A"},
    {"question": "Which mob throws fireballs at you in Dungeons?",
     "options": ["Creeper", "Firebrand", "Evoker", "Vindicator"], "answer": "C"},
    # Minecraft Legends
    {"question": "Who is the main protagonist in Minecraft Legends?",
     "options": ["Alex", "Steve", "Illager Leader", "Arch-Illager"], "answer": "B"},
    {"question": "Which biome is the starting area in Minecraft Legends?",
     "options": ["Plains", "Savanna", "Forest", "Desert"], "answer": "A"},
    {"question": "Which creature is NOT a threat in Legends?",
     "options": ["Pillager", "Spider", "Illager Army", "Wolf"], "answer": "D"},
    {"question": "What resource do you collect to upgrade your army in Legends?",
     "options": ["Gold", "Emeralds", "Iron", "Diamonds"], "answer": "B"},
    {"question": "Which building allows you to train units in Legends?",
     "options": ["Barracks", "Forge", "Town Hall", "Blacksmith"], "answer": "A"},
]

# -----------------------------
# Quiz GUI class
# -----------------------------
class QuizGame:
    def __init__(self, root):
        # Initialize window
        self.root = root
        self.root.title("Minecraft Trivia Quiz")
        self.root.geometry("700x500")
        self.root.config(bg="#1a1a1a")

        # Quiz state variables
        self.name = ""
        self.age = 0
        self.score = 0
        self.current_question = 0
        self.user_answers = []
        self.num_questions = 5
        self.selected_questions = []

        # -----------------------------
        # Start frame (name & age input)
        # -----------------------------
        self.start_frame = tk.Frame(root, bg="#1a1a1a")
        self.start_frame.pack(expand=True, fill="both")

        tk.Label(self.start_frame, text="Welcome to Minecraft Trivia Quiz!",
                 font=("Arial", 22, "bold"), fg="lime", bg="#1a1a1a").pack(pady=20)

        tk.Label(self.start_frame, text="Enter your name:", font=("Arial", 14), fg="white", bg="#1a1a1a").pack()
        self.name_entry = tk.Entry(self.start_frame, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        tk.Label(self.start_frame, text="Enter your age:", font=("Arial", 14), fg="white", bg="#1a1a1a").pack()
        self.age_entry = tk.Entry(self.start_frame, font=("Arial", 14))
        self.age_entry.pack(pady=5)

        tk.Button(self.start_frame, text="Next: Choose Difficulty", font=("Arial", 14), bg="orange", fg="white",
                  command=self.show_difficulty).pack(pady=20)

    # -----------------------------
    # Show difficulty selection
    # -----------------------------
    def show_difficulty(self):
        # Validate name & age
        if not self.name or not self.age:
            self.name = self.name_entry.get()
            try:
                self.age = int(self.age_entry.get())
                if not (11 <= self.age <= 18):
                    messagebox.showerror("Error", "This quiz is for ages 11 to 18 only.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid age.")
                return

        # Hide start frame
        self.start_frame.pack_forget()
        if hasattr(self, "diff_frame"):
            self.diff_frame.destroy()

        # Difficulty frame
        self.diff_frame = tk.Frame(self.root, bg="#0d0d0d")
        self.diff_frame.pack(expand=True, fill="both")

        tk.Label(self.diff_frame, text="Select Difficulty",
                 font=("Arial", 22, "bold"), fg="cyan", bg="#0d0d0d").pack(pady=30)
        tk.Button(self.diff_frame, text="Easy (Minecraft only)", font=("Arial", 16),
                  bg="#32cd32", fg="white", command=lambda: self.start_quiz(5, "Easy")).pack(pady=15)
        tk.Button(self.diff_frame, text="Medium (Mix MC/MCD/MCL)", font=("Arial", 16),
                  bg="#1e90ff", fg="white", command=lambda: self.start_quiz(10, "Medium")).pack(pady=15)
        tk.Button(self.diff_frame, text="Hard (All questions)", font=("Arial", 16),
                  bg="#ff4500", fg="white", command=lambda: self.start_quiz(15, "Hard")).pack(pady=15)

    # -----------------------------
    # Start the quiz with difficulty
    # -----------------------------
    def start_quiz(self, num_questions, difficulty="Easy"):
        # Filter questions based on difficulty
        if difficulty == "Easy":
            filtered_questions = questions[:5]  # Minecraft only
        elif difficulty == "Medium":
            mc = questions[:5]
            mcd_mcl = questions[5:]
            filtered_questions = mc + random.sample(mcd_mcl, min(num_questions - len(mc), len(mcd_mcl)))
        else:  # Hard
            filtered_questions = questions

        self.num_questions = min(num_questions, len(filtered_questions))
        self.selected_questions = random.sample(filtered_questions, self.num_questions)

        # Destroy difficulty frame
        if hasattr(self, "diff_frame"):
            self.diff_frame.destroy()

        self.current_question = 0
        self.score = 0
        self.user_answers = []

        self.show_question()

    # -----------------------------
    # Show each question
    # -----------------------------
    def show_question(self):
        if hasattr(self, "q_frame"):
            self.q_frame.destroy()

        self.q_frame = tk.Frame(self.root, bg="#0b0b0b")
        self.q_frame.pack(expand=True, fill="both")

        self.feedback_label = tk.Label(self.q_frame, text="", font=("Arial", 14), fg="white", bg="#0b0b0b")
        self.feedback_label.pack(side="bottom", pady=20)

        q = self.selected_questions[self.current_question]
        tk.Label(self.q_frame, text=f"Question {self.current_question + 1}: {q['question']}",
                 font=("Arial", 16, "bold"), fg="lime", bg="#0b0b0b", wraplength=650).pack(pady=40)

        self.option_buttons = []
        for idx, option in enumerate(q['options']):
            letter = 'ABCD'[idx]
            btn = tk.Button(self.q_frame, text=f"{letter}. {option}", font=("Arial", 14), width=30,
                            bg="#444", fg="white", command=lambda l=letter: self.check_answer(l))
            btn.pack(pady=10)
            self.option_buttons.append(btn)

    # -----------------------------
    # Check answer
    # -----------------------------
    def check_answer(self, answer):
        q = self.selected_questions[self.current_question]
        self.user_answers.append(answer)
        correct = answer == q['answer']

        self.q_frame.config(bg="#1abc9c" if correct else "#e74c3c")
        for btn in self.option_buttons:
            btn.config(state="disabled")

        if correct:
            self.feedback_label.config(text="✅ Correct!", bg="#1abc9c")
            self.score += 1
        else:
            correct_letter = q['answer']
            correct_option = q['options']['ABCD'.index(correct_letter)]
            self.feedback_label.config(text=f"❌ Wrong! Correct: {correct_letter} - {correct_option}", bg="#e74c3c")

        self.root.after(1000, self.next_question)

    # -----------------------------
    # Next question
    # -----------------------------
    def next_question(self):
        self.current_question += 1
        if self.current_question < self.num_questions:
            self.show_question()
        else:
            self.show_results()

    # -----------------------------
    # Show results
    # -----------------------------
    def show_results(self):
        if hasattr(self, "q_frame"):
            self.q_frame.destroy()

        self.result_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.result_frame.pack(expand=True, fill="both")

        tk.Label(self.result_frame, text="Quiz Results", font=("Arial", 22, "bold"), fg="yellow", bg="#0a0a0a").pack(pady=20)
        tk.Label(self.result_frame, text=f"Player: {self.name}, Age: {self.age}", font=("Arial", 16), fg="white", bg="#0a0a0a").pack()
        tk.Label(self.result_frame, text=f"Score: {self.score}/{self.num_questions} ({self.score / self.num_questions * 100:.2f}%)",
                 font=("Arial", 16), fg="lime", bg="#0a0a0a").pack(pady=10)

        tk.Label(self.result_frame, text="Your Answers vs Correct Answers:", font=("Arial", 14, "underline"),
                 fg="cyan", bg="#0a0a0a").pack(pady=10)
        for idx, q in enumerate(self.selected_questions):
            correct_letter = q['answer']
            correct_option = q['options']['ABCD'.index(correct_letter)]
            tk.Label(self.result_frame, text=f"{idx + 1}. Your answer: {self.user_answers[idx]} | Correct: {correct_letter} - {correct_option}",
                     font=("Arial", 12), fg="white", bg="#0a0a0a", anchor="w").pack(fill="x")

        tk.Button(self.result_frame, text="Exit", font=("Arial", 16), bg="red", fg="white",
                  command=self.root.destroy).pack(pady=10)
        tk.Button(self.result_frame, text="Play Again", font=("Arial", 16), bg="orange", fg="white",
                  command=self.play_again).pack(pady=10)

    # -----------------------------
    # Replay game
    # -----------------------------
    def play_again(self):
        # Destroy result frame
        if hasattr(self, "result_frame"):
            self.result_frame.destroy()

        # Reset state
        self.score = 0
        self.current_question = 0
        self.user_answers = []
        self.selected_questions = []

        # Show difficulty selection again
        self.show_difficulty()


# -----------------------------
# Run the GUI
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop()