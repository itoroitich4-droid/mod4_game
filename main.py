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

        self.input_user = ""
        self.input_pass = ""
        self.input_confirm = ""
        self.active_field = "user"
        self.feedback = ""

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
        """Pop-up notification for Weekly Streak"""
        modal = pygame.Rect(200, 150, 500, 300)
        pygame.draw.rect(self.screen, CARD_BG, modal, border_radius=12)
        pygame.draw.rect(self.screen, ACCENT_GREEN, modal, 4, border_radius=12)
        
        self.draw_text("DAILY STREAK POP-UP!", 320, 180, ACCENT_GREEN, self.title_font)
        self.draw_text(f"Welcome back, {self.current_user.username}!", 240, 240)
        self.draw_text(f"Weekly Streak: {self.current_user.streak} / 7 Days", 240, 280, (255, 230, 100))
        btn_claim = self.draw_btn("Continue", 350, 350, 200, 40)
        return btn_claim

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

    def render_main_menu(self):
        self.draw_text(f"Welcome, {self.current_user.username} | Points: {self.current_user.total_points}", 200, 50, font=self.title_font)
        return {
            "solo": self.draw_btn("Solo Play", 300, 140, 300, 45),
            "p2": self.draw_btn("Two Player (Local Split-Screen)", 300, 210, 300, 45),
            "leaderboard": self.draw_btn("Leaderboard Rankings", 300, 280, 300, 45, ACCENT_BLUE),
            "users": self.draw_btn("User Activity Statuses", 300, 350, 300, 45, ACCENT_BLUE),
            "logout": self.draw_btn("Logout", 300, 420, 300, 45, ACCENT_RED)
        }

    def render_user_statuses(self):
        self.draw_text("=== ALL USER STATUSES ===", 300, 40, font=self.title_font)
        users = self.get_users_list()
        y = 110
        for u in users:
            color = ACCENT_GREEN if u.status == "online" else (ACCENT_RED if u.status == "offline" else (240, 180, 50))
            self.draw_text(f"{u.username} - Status: {u.status.upper()}", 200, y, color=color)
            y += 35
        return {"back": self.draw_btn("Back", 300, 520, 300, 45)}

    def run(self):
        running = True
        while running:
            self.screen.fill(BG_COLOR)
            m_pos = pygame.mouse.get_pos()
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.current_user:
                        self.current_user.status = "offline"
                        self.save_user(self.current_user)
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

            if self.current_screen == "home":
                btns = self.render_home()
                if click:
                    if btns["login"].collidepoint(m_pos):
                        users = {u.username: u for u in self.get_users_list()}
                        # Mock auto-login for demonstration
                        if users:
                            self.current_user = list(users.values())[0]
                            self.current_user.update_streak()
                            self.current_user.status = "online"
                            self.save_user(self.current_user)
                            self.show_streak_popup = True
                            self.current_screen = "main_menu"
                    elif btns["exit"].collidepoint(m_pos): running = False

            elif self.current_screen == "main_menu":
                btns = self.render_main_menu()
                if self.show_streak_popup:
                    btn_claim = self.draw_streak_modal()
                    if click and btn_claim.collidepoint(m_pos):
                        self.show_streak_popup = False
                elif click:
                    if btns["users"].collidepoint(m_pos): self.current_screen = "user_statuses"
                    elif btns["logout"].collidepoint(m_pos):
                        self.current_user.status = "offline"
                        self.save_user(self.current_user)
                        self.current_user = None
                        self.current_screen = "home"

            elif self.current_screen == "user_statuses":
                btns = self.render_user_statuses()
                if click and btns["back"].collidepoint(m_pos):
                    self.current_screen = "main_menu"

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameEngine()
    game.run() 