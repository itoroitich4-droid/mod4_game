import random
import questions.py


class QuizGame:

  def __init__(
      self,
      category_name: str | None = None,
      total_rounds: int = 5,
      is_daily_challenge: bool = False,
      mode: str = "standard",
  ):
    self.category_name = category_name
    self.total_rounds = total_rounds
    self.is_daily_challenge = is_daily_challenge
    self.mode = mode  # "standard", "daily", or "truth_lie"
    self.score = 0
    self.asked_question_ids = []

  def get_next_question(self):
    """Retrieves a single question for standard/daily modes."""
    question = db.fetch_random_question(
        category_name=self.category_name,
        exclude_ids=self.asked_question_ids,
    )
    if question:
      self.asked_question_ids.append(question["id"])
    return question

  def get_truth_and_lie_round(self):
    """Fetches 3 questions to generate 2 truths and 1 lie."""
    raw_questions = []

    # Fetch 3 distinct questions
    for _ in range(3):
      q = self.get_next_question()
      if q:
        raw_questions.append(q)

    if len(raw_questions) < 3:
      return None  # Not enough questions left to form a round

    # Pick 2 questions to use as TRUTHS (show correct answers)
    truth_1 = {
        "statement": (
            f"{raw_questions[0]['question_text']} ->"
            f" {raw_questions[0]['option_' + raw_questions[0]['correct_option'].lower()]}"
        ),
        "is_lie": False,
    }
    truth_2 = {
        "statement": (
            f"{raw_questions[1]['question_text']} ->"
            f" {raw_questions[1]['option_' + raw_questions[1]['correct_option'].lower()]}"
        ),
        "is_lie": False,
    }

    # Pick 1 question to use as LIE (pick any wrong option)
    correct_opt = raw_questions[2]["correct_option"].lower()
    wrong_opts = [
        opt for opt in ["a", "b", "c", "d"] if opt != correct_opt
    ]
    chosen_wrong_opt = random.choice(wrong_opts)

    lie = {
        "statement": (
            f"{raw_questions[2]['question_text']} ->"
            f" {raw_questions[2]['option_' + chosen_wrong_opt]}"
        ),
        "is_lie": True,
    }

    # Combine and shuffle statements so the lie isn't always option C
    statements = [truth_1, truth_2, lie]
    random.shuffle(statements)

    # Assign labels A, B, C and find correct key (the lie)
    round_data = {"options": {}}
    lie_label = ""

    for idx, key in enumerate(["A", "B", "C"]):
      item = statements[idx]
      round_data["options"][key] = item["statement"]
      if item["is_lie"]:
        lie_label = key

    round_data["correct_lie_option"] = lie_label
    return round_data

  def submit_answer(
      self, user_answer: str, correct_option: str
  ) -> bool:
    """Validates user choice against the expected correct option."""
    is_correct = user_answer.strip().upper() == correct_option
    if is_correct:
      points = (
          15
          if self.is_daily_challenge
          else (20 if self.mode == "truth_lie" else 10)
      )
      self.score += points
    return is_correct


# --- CLI Game Engine Loop ---
def play_game():
  print("=== Welcome to the Quiz Game ===")
  print("1) Category Mode (5 rounds)")
  print("2) Daily Challenge (10 rounds across all categories)")
  print("3) Two Truths and a Lie (5 rounds - Find the FALSE statement)")

  mode = input("\nChoose Mode (1, 2, or 3): ").strip()

  if mode == "3":
    print("\n--- Starting Two Truths and a Lie ---")
    game = QuizGame(
        category_name=None, total_rounds=5, mode="truth_lie"
    )
  elif mode == "2":
    print("\n--- Starting Daily Challenge (10 Rounds) ---")
    game = QuizGame(
        category_name=None,
        total_rounds=10,
        is_daily_challenge=True,
        mode="daily",
    )
  else:
    category = input(
        "\nChoose Category (e.g., Science, History): "
    ).strip()
    print(f"\n--- Starting Game in Category: {category} ---")
    game = QuizGame(category_name=category, total_rounds=5, mode="standard")

  for round_num in range(1, game.total_rounds + 1):
    print(f"\nRound {round_num}/{game.total_rounds}:")

    # --- Mode 3 Logic ---
    if game.mode == "truth_lie":
      round_data = game.get_truth_and_lie_round()
      if not round_data:
        print("Not enough questions left to generate this round!")
        break

      print("Spot the LIE (Find the false statement):")
      print(f"A) {round_data['options']['A']}")
      print(f"B) {round_data['options']['B']}")
      print(f"C) {round_data['options']['C']}")

      user_choice = input("Which one is FALSE? (A/B/C): ").upper()
      correct_answer = round_data["correct_lie_option"]

    # --- Standard / Daily Logic ---
    else:
      question = game.get_next_question()
      if not question:
        print("\nNo more questions available!")
        break

      if game.is_daily_challenge and "category" in question:
        print(f"[{question['category'].upper()}]")

      print(question["question_text"])
      print(f"A) {question['option_a']}")
      print(f"B) {question['option_b']}")
      print(f"C) {question['option_c']}")
    

      user_choice = input("Your answer (A/B/C): ").upper()
      correct_answer = question["correct_option"]

    # --- Score Validation ---
    if game.submit_answer(user_choice, correct_answer):
      print(" Correct!")
    else:
      print(f" Wrong! The correct selection was {correct_answer}")

  print(f"\n--- Game Over! Final Score: {game.score} pts ---")


if __name__ == "__main__":
  play_game()