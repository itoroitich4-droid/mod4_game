from utils.file_handler import load_questions


def test_file_handler():

    data = load_questions()

    assert "categories" in data