import random

QUESTIONS_DB = {
    "Technology": [
        {"prompt": "Find the LIE about programming:", "options": ["A. Python named after a snake.", "B. Pygame came in 2000.", "C. JSON is JavaScript notation."], "lie": "A"},
        {"prompt": "Find the LIE about OS:", "options": ["A. Linux kernel created in 1991.", "B. Windows 95 came in 1995.", "C. MacOS is based on Windows."], "lie": "C"}
    ],
    "Gaming": [
        {"prompt": "Find the LIE about games:", "options": ["A. Mario first in Donkey Kong.", "B. Tetris made in Russia.", "C. Minecraft made in 12 days."], "lie": "C"}
    ]
}

class GameSession:
    def __init__(self, mode="quickplay", category=None):
        self.mode = mode
        self.score = 0
        self.current_index = 0

        if mode == "demo":
            all_q = [q for cat in QUESTIONS_DB.values() for q in cat]
            self.questions = random.sample(all_q, min(5, len(all_q)))
        elif mode == "quickplay":
            pool = QUESTIONS_DB.get(category, [])
            self.questions = (pool * 10)[:10] 
        elif mode == "daily":
            all_q = [q for cat in QUESTIONS_DB.values() for q in cat]
            self.questions = all_q
            random.shuffle(self.questions)

    def get_current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def submit_answer(self, choice: str) -> bool:
        q = self.get_current_question()
        if not q: return False
        is_correct = (choice.upper() == q["lie"])
        if is_correct: self.score += 1
        return is_correct