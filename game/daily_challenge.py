import random
from models.question import Question
from utils.file_handler import load_questions


def get_daily_questions():
    data = load_questions()["categories"]

    questions = []

    for category in data:
        for item in data[category]:
            questions.append(
                Question(
                    item["statements"],
                    item["answer"],
                    category
                )
            )

    random.shuffle(questions)

    return questions[:30]