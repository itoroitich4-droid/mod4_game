class Game:
    def __init__(self, questions):
        self.questions = questions
        self.current = 0
        self.score = 0

    def check_answer(self, answer):
        if answer == self.questions[self.current].answer:
            self.score += 1
            return True

        return False