
import time

def is_bonus_available(last_bonus_ts):
    return (time.time() - last_bonus_ts) >= 86400

def time_until_next_bonus(last_bonus_ts):
    remaining = 86400 - (time.time() - last_bonus_ts)
    hrs = int(remaining // 3600)
    mins = int((remaining % 3600) // 60)
    return f"{hrs} год {mins} хв"

def get_level(clicks):
    return clicks // 50 + 1
