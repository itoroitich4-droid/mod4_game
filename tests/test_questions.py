from utils.file_handler import load_questions


def test_categories():

    data = load_questions()

    categories = data["categories"]

    assert len(categories) == 10