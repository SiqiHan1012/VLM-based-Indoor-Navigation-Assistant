import time
import os

class GlobalState:
    def __init__(self):
        # Initial goal from environment or empty
        self.CURRENT_GOAL = os.getenv("DEFAULT_GOAL", "")
        self.GOAL_CENTER_STREAK = 0
        self.GOAL_UPDATED_AT = time.time()
        self.frame_counter = 0

    def set_goal(self, text: str):
        """Update CURRENT_GOAL safely (called by /asr or when form goal is provided)."""
        g = (text or "").strip().replace("\n", " ").replace("\r", " ")
        if len(g) > 160:
            g = g[:160]
        if g:
            self.CURRENT_GOAL = g
            self.GOAL_UPDATED_AT = time.time()
            return g
        return self.CURRENT_GOAL

    def get_goal(self):
        return self.CURRENT_GOAL


nav_state = GlobalState()
