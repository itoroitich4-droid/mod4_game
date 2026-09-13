from game.daily_challenge import get_daily_questions


def test_daily_challenge():

    questions = get_daily_questions()

    assert len(questions) == 1