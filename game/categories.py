from models.question import Question
from utils.file_handler import load_questions


def get_categories():
    data = load_questions()["categories"]

    return list(data.keys())


def get_category_questions(category):
    data = load_questions()["categories"]

    questions = []

    for item in data[category]:
        questions.append(
            Question(
                item["statements"],
                item["answer"],
                category
            )
        )

    return questions