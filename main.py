import pygame
import sys
import time
from utils.storage import DataStorage
from utils.auth import hash_password
from models.user import User
from models.game import GameSession, QUESTIONS_DB

WIDTH, HEIGHT = 900, 650
BG_COLOR = (24, 20, 37)
CARD_BG = (38, 35, 58)
TEXT_COLOR = (255, 255, 255)
ACCENT_GREEN = (75, 180, 100)
ACCENT_BLUE = (60, 120, 210)
ACCENT_RED = (200, 60, 60)

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("101 GAME - Two Truths & 1 Lie")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier", 18, bold=True)
        self.title_font = pygame.font.SysFont("Courier", 24, bold=True)
        
        self.current_screen = "home"
        self.current_user = None
        self.p2_user = None
        self.show_streak_popup = False
        
        self.user_db_path = "data/users.json"
        self.session = None
        self.p2_session = None

        # Input buffers
        self.input_user = ""
        self.input_pass = ""
        self.input_confirm = ""
        self.active_field = "user"
        self.feedback = ""

    # --- RENDER HELPERS ---
    def draw_text(self, text, x, y, color=TEXT_COLOR, font=None):
        f = font if font else self.font
        surf = f.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def draw_btn(self, text, x, y, w, h, bg=ACCENT_GREEN):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, bg, rect, border_radius=6)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=6)
        t_surf = self.font.render(text, True, (255, 255, 255))
        tx = x + (w - t_surf.get_width()) // 2
        ty = y + (h - t_surf.get_height()) // 2
        self.screen.blit(t_surf, (tx, ty))
        return rect

    def draw_streak_modal(self):
        modal = pygame.Rect(200, 150, 500, 320)
        pygame.draw.rect(self.screen, CARD_BG, modal, border_radius=12)
        pygame.draw.rect(self.screen, ACCENT_GREEN, modal, 4, border_radius=12)
        
        self.draw_text("DAILY STREAK NOTIFICATION!", 240, 180, ACCENT_GREEN, self.title_font)
        self.draw_text(f"Welcome back, {self.current_user.username}!", 240, 240)
        self.draw_text(f"Weekly Streak: {self.current_user.streak} / 7 Days", 240, 280, (255, 230, 100))
        self.draw_text("Keep playing daily to preserve your streak!", 230, 320)
        
        return self.draw_btn("Continue", 350, 370, 200, 40)

    def get_users_list(self):
        raw = DataStorage.load_json(self.user_db_path)
        return [User(**data) for data in raw.values()]

    def save_user(self, user: User):
        raw = DataStorage.load_json(self.user_db_path)
        raw[user.username] = user.to_dict()
        DataStorage.save_json(self.user_db_path, raw)

    # --- SCREENS ---
    def render_home(self):
        self.draw_text("=== 101 GAME: TWO TRUTHS & 1 LIE ===", 220, 60, font=self.title_font)
        return {
            "login": self.draw_btn("Login", 300, 160, 300, 45),
            "register": self.draw_btn("Register", 300, 230, 300, 45),
            "demo": self.draw_btn("Demo Play (Unregistered)", 300, 300, 300, 45, ACCENT_BLUE),
            "exit": self.draw_btn("Exit", 300, 370, 300, 45, ACCENT_RED)
        }

    def render_login(self):
        self.draw_text("=== LOGIN ===", 370, 80, font=self.title_font)
        self.draw_text(f"Username: {self.input_user}{'|' if self.active_field=='user' else ''}", 250, 180)
        self.draw_text(f"Password: {'*' * len(self.input_pass)}{'|' if self.active_field=='pass' else ''}", 250, 240)
        btn_enter = self.draw_btn("Enter", 300, 320, 300, 45)
        btn_back = self.draw_btn("Back", 300, 380, 300, 45, ACCENT_BLUE)
        self.draw_text(self.feedback, 250, 450, ACCENT_RED)
        return {"enter": btn_enter, "back": btn_back}

    def render_register(self):
        self.draw_text("=== REGISTER ===", 350, 60, font=self.title_font)
        self.draw_text(f"Name: {self.input_user}{'|' if self.active_field=='user' else ''}", 250, 140)
        self.draw_text(f"Password: {'*' * len(self.input_pass)}{'|' if self.active_field=='pass' else ''}", 250, 200)
        self.draw_text(f"Confirm Password: {'*' * len(self.input_confirm)}{'|' if self.active_field=='confirm' else ''}", 250, 260)
        btn_submit = self.draw_btn("Register", 300, 330, 300, 45)
        btn_back = self.draw_btn("Back", 300, 390, 300, 45, ACCENT_RED)
        self.draw_text(self.feedback, 250, 460, ACCENT_RED)
        return {"submit": btn_submit, "back": btn_back}

    def render_main_menu(self):
        self.draw_text(f"Welcome, {self.current_user.username} | Points: {self.current_user.total_points}", 200, 50, font=self.title_font)
        return {
            "solo": self.draw_btn("Solo Play", 300, 140, 300, 45),
            "p2": self.draw_btn("Two Player (Local Split-Screen)", 300, 210, 300, 45),
            "leaderboard": self.draw_btn("Leaderboard Rankings", 300, 280, 300, 45, ACCENT_BLUE),
            "users": self.draw_btn("User Activity Statuses", 300, 350, 300, 45, ACCENT_BLUE),
            "logout": self.draw_btn("Logout", 300, 420, 300, 45, ACCENT_RED)
        }

    def render_solo_menu(self):
        self.draw_text("=== SOLO PLAY MENU ===", 320, 60, font=self.title_font)
        btn_qp = self.draw_btn("Quickplay (Choose Category)", 250, 150, 400, 45)
        btn_daily = self.draw_btn("Daily Challenge (1 Play / 24hrs)", 250, 220, 400, 45)
        btn_back = self.draw_btn("Back", 250, 290, 400, 45, ACCENT_RED)
        self.draw_text(self.feedback, 250, 360, ACCENT_RED)
        return {"qp": btn_qp, "daily": btn_daily, "back": btn_back}

    def render_category_select(self):
        self.draw_text("=== CHOOSE CATEGORY ===", 300, 80, font=self.title_font)
        btns = {}
        y = 180
        for cat in QUESTIONS_DB.keys():
            btns[cat] = self.draw_btn(cat, 300, y, 300, 45)
            y += 65
        btns["back"] = self.draw_btn("Back", 300, y, 300, 45, ACCENT_RED)
        return btns

    def render_leaderboard(self):
        self.draw_text("=== LEADERBOARD (RANKINGS) ===", 250, 40, font=self.title_font)
        users = sorted(self.get_users_list(), key=lambda u: u.total_points, reverse=True)
        y = 110
        for rank, u in enumerate(users, 1):
            is_me = "(You)" if self.current_user and u.username == self.current_user.username else ""
            self.draw_text(f"#{rank} {u.username} {is_me} - Points: {u.total_points}", 250, y)
            y += 35
        return {"back": self.draw_btn("Back", 300, 520, 300, 45)}

    def render_user_statuses(self):
        self.draw_text("=== ALL USER STATUSES ===", 300, 40, font=self.title_font)
        users = self.get_users_list()
        y = 110
        for u in users:
            color = ACCENT_GREEN if u.status == "online" else (ACCENT_RED if u.status == "offline" else (240, 180, 50))
            self.draw_text(f"{u.username} - Status: {u.status.upper()}", 200, y, color=color)
            y += 35
        return {"back": self.draw_btn("Back", 300, 520, 300, 45)}

    def render_p2_select(self):
        self.draw_text("=== SELECT PLAYER 2 ===", 300, 40, font=self.title_font)
        users = [u for u in self.get_users_list() if u.username != self.current_user.username]
        btns = {}
        y = 110
        for u in users:
            btns[u.username] = self.draw_btn(f"Play with {u.username}", 250, y, 400, 40)
            y += 50
        btns["back"] = self.draw_btn("Back", 250, y, 400, 40, ACCENT_RED)
        return btns

    def render_gameplay(self):
        q = self.session.get_current_question()
        if not q:
            if self.current_user:
                self.current_user.add_points(self.session.score)
                self.current_user.set_status("online")
                self.save_user(self.current_user)
            self.current_screen = "solo_menu" if self.current_user else "home"
            return {}

        self.draw_text(f"Mode: {self.session.mode.upper()} | Score: {self.session.score}", 50, 30)
        if self.session.mode == "demo":
            self.draw_text(f"Question {self.session.current_index+1}/5", 650, 30)
        elif self.session.mode == "quickplay":
            self.draw_text(f"Question {self.session.current_index+1}/10", 650, 30)

        self.draw_text(q["prompt"], 80, 110, color=(255, 230, 100))
        btn_a = self.draw_btn(q["options"][0], 80, 200, 740, 50, CARD_BG)
        btn_b = self.draw_btn(q["options"][1], 80, 270, 740, 50, CARD_BG)
        btn_c = self.draw_btn(q["options"][2], 80, 340, 740, 50, CARD_BG)
        return {"A": btn_a, "B": btn_b, "C": btn_c}

    def render_p2_gameplay(self):
        q1 = self.session.get_current_question()
        q2 = self.p2_session.get_current_question()

        if not q1 or not q2:
            self.current_user.add_points(self.session.score)
            self.p2_user.add_points(self.p2_session.score)
            self.current_user.set_status("online")
            self.p2_user.set_status("offline")
            self.save_user(self.current_user)
            self.save_user(self.p2_user)
            self.current_screen = "main_menu"
            return {}

        pygame.draw.line(self.screen, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 3)

        # Player 1 Side
        self.draw_text(f"{self.current_user.username}: {self.session.score} PTS", 20, 20)
        self.draw_text(q1["prompt"][:26], 20, 80, (255, 230, 100))
        p1_a = self.draw_btn(q1["options"][0], 20, 180, 400, 45, CARD_BG)
        p1_b = self.draw_btn(q1["options"][1], 20, 240, 400, 45, CARD_BG)
        p1_c = self.draw_btn(q1["options"][2], 20, 300, 400, 45, CARD_BG)

        # Player 2 Side
        self.draw_text(f"{self.p2_user.username}: {self.p2_session.score} PTS", 470, 20)
        self.draw_text(q2["prompt"][:26], 470, 80, (255, 230, 100))
        p2_a = self.draw_btn(q2["options"][0], 470, 180, 400, 45, CARD_BG)
        p2_b = self.draw_btn(q2["options"][1], 470, 240, 400, 45, CARD_BG)
        p2_c = self.draw_btn(q2["options"][2], 470, 300, 400, 45, CARD_BG)

        return {"p1": {"A": p1_a, "B": p1_b, "C": p1_c}, "p2": {"A": p2_a, "B": p2_b, "C": p2_c}}

    # --- ENGINE LOOP ---
    def run(self):
        running = True
        while running:
            self.screen.fill(BG_COLOR)
            m_pos = pygame.mouse.get_pos()
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.current_user:
                        self.current_user.set_status("offline")
                        self.save_user(self.current_user)
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
                elif event.type == pygame.KEYDOWN and self.current_screen in ["login", "register"]:
                    if event.key == pygame.K_TAB:
                        if self.current_screen == "login":
                            self.active_field = "pass" if self.active_field == "user" else "user"
                        else:
                            fields = ["user", "pass", "confirm"]
                            self.active_field = fields[(fields.index(self.active_field) + 1) % 3]
                    elif event.key == pygame.K_BACKSPACE:
                        if self.active_field == "user": self.input_user = self.input_user[:-1]
                        elif self.active_field == "pass": self.input_pass = self.input_pass[:-1]
                        elif self.active_field == "confirm": self.input_confirm = self.input_confirm[:-1]
                    else:
                        if self.active_field == "user": self.input_user += event.unicode
                        elif self.active_field == "pass": self.input_pass += event.unicode
                        elif self.active_field == "confirm": self.input_confirm += event.unicode

            if self.current_screen == "home":
                btns = self.render_home()
                if click:
                    if btns["login"].collidepoint(m_pos): self.current_screen = "login"; self.feedback = ""
                    elif btns["register"].collidepoint(m_pos): self.current_screen = "register"; self.feedback = ""
                    elif btns["demo"].collidepoint(m_pos):
                        self.session = GameSession(mode="demo")
                        self.current_screen = "gameplay"
                    elif btns["exit"].collidepoint(m_pos): running = False

            elif self.current_screen == "login":
                btns = self.render_login()
                if click:
                    if btns["enter"].collidepoint(m_pos):
                        users = {u.username: u for u in self.get_users_list()}
                        if self.input_user in users and users[self.input_user].verify_password(self.input_pass):
                            self.current_user = users[self.input_user]
                            self.current_user.update_streak()
                            self.current_user.set_status("online")
                            self.save_user(self.current_user)
                            self.show_streak_popup = True
                            self.current_screen = "main_menu"
                        else: self.feedback = "Invalid Username or Password"
                    elif btns["back"].collidepoint(m_pos): self.current_screen = "home"

            elif self.current_screen == "register":
                btns = self.render_register()
                if click:
                    if btns["submit"].collidepoint(m_pos):
                        users = {u.username: u for u in self.get_users_list()}
                        if not self.input_user or not self.input_pass: self.feedback = "Fill all fields"
                        elif self.input_pass != self.input_confirm: self.feedback = "Passwords mismatch"
                        elif self.input_user in users: self.feedback = "Username exists"
                        else:
                            new_u = User.create_new(self.input_user, self.input_pass)
                            self.save_user(new_u)
                            self.current_user = new_u
                            self.show_streak_popup = True
                            self.current_screen = "main_menu"
                    elif btns["back"].collidepoint(m_pos): self.current_screen = "home"

            elif self.current_screen == "main_menu":
                btns = self.render_main_menu()
                if self.show_streak_popup:
                    btn_close = self.draw_streak_modal()
                    if click and btn_close.collidepoint(m_pos):
                        self.show_streak_popup = False
                elif click:
                    if btns["solo"].collidepoint(m_pos): self.current_screen = "solo_menu"; self.feedback = ""
                    elif btns["p2"].collidepoint(m_pos): self.current_screen = "p2_select"
                    elif btns["leaderboard"].collidepoint(m_pos): self.current_screen = "leaderboard"
                    elif btns["users"].collidepoint(m_pos): self.current_screen = "user_statuses"
                    elif btns["logout"].collidepoint(m_pos):
                        self.current_user.set_status("offline")
                        self.save_user(self.current_user)
                        self.current_user = None
                        self.current_screen = "home"

            elif self.current_screen == "solo_menu":
                btns = self.render_solo_menu()
                if click:
                    if btns["qp"].collidepoint(m_pos): self.current_screen = "category_select"
                    elif btns["daily"].collidepoint(m_pos):
                        now = time.time()
                        if now - self.current_user.last_daily < 86400:
                            self.feedback = "Daily Challenge completed! Check back in 24 hrs."
                        else:
                            self.current_user.last_daily = now
                            self.current_user.set_status("engaged - playing another game")
                            self.save_user(self.current_user)
                            self.session = GameSession(mode="daily")
                            self.current_screen = "gameplay"
                    elif btns["back"].collidepoint(m_pos): self.current_screen = "main_menu"

            elif self.current_screen == "category_select":
                btns = self.render_category_select()
                if click:
                    for cat, btn in btns.items():
                        if btn.collidepoint(m_pos):
                            if cat == "back": self.current_screen = "solo_menu"
                            else:
                                self.current_user.set_status("engaged - playing another game")
                                self.save_user(self.current_user)
                                self.session = GameSession(mode="quickplay", category=cat)
                                self.current_screen = "gameplay"

            elif self.current_screen in ["leaderboard", "user_statuses"]:
                btns = self.render_leaderboard() if self.current_screen == "leaderboard" else self.render_user_statuses()
                if click and btns["back"].collidepoint(m_pos): self.current_screen = "main_menu"

            elif self.current_screen == "p2_select":
                btns = self.render_p2_select()
                if click:
                    for uname, btn in btns.items():
                        if btn.collidepoint(m_pos):
                            if uname == "back": self.current_screen = "main_menu"
                            else:
                                users = {u.username: u for u in self.get_users_list()}
                                self.p2_user = users[uname]
                                self.current_user.set_status("engaged - playing another game")
                                self.p2_user.set_status("engaged - playing another game")
                                self.save_user(self.current_user)
                                self.save_user(self.p2_user)
                                self.session = GameSession(mode="quickplay", category="Technology")
                                self.p2_session = GameSession(mode="quickplay", category="Technology")
                                self.current_screen = "p2_gameplay"

            elif self.current_screen == "gameplay":
                btns = self.render_gameplay()
                if click and btns:
                    for opt in ["A", "B", "C"]:
                        if btns[opt].collidepoint(m_pos):
                            is_correct = self.session.submit_answer(opt)
                            if self.session.mode == "daily" and not is_correct:
                                self.current_user.add_points(self.session.score)
                                self.current_user.set_status("online")
                                self.save_user(self.current_user)
                                self.current_screen = "solo_menu"
                            else:
                                self.session.current_index += 1

            elif self.current_screen == "p2_gameplay":
                btns = self.render_p2_gameplay()
                if click and btns:
                    for opt in ["A", "B", "C"]:
                        if btns["p1"][opt].collidepoint(m_pos):
                            self.session.submit_answer(opt)
                            self.session.current_index += 1
                        if btns["p2"][opt].collidepoint(m_pos):
                            self.p2_session.submit_answer(opt)
                            self.p2_session.current_index += 1

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameEngine()
    game.run()