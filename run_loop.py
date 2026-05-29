"""Uruchamia News Agent w pętli co LOOP_INTERVAL_MIN minut.

Najprostszy harmonogram — działa dopóki okno jest otwarte. Do uruchomienia
w tle / po restarcie systemu użyj Harmonogramu zadań Windows (patrz README).
"""

import time
import traceback
from datetime import datetime
from main import main
from config import LOOP_INTERVAL_MIN


def loop():
    print(f"News Agent w pętli — co {LOOP_INTERVAL_MIN} min. Ctrl+C aby przerwać.\n")
    while True:
        print(f"\n========== {datetime.now():%Y-%m-%d %H:%M:%S} ==========")
        try:
            main()
        except Exception:
            traceback.print_exc()
        print(f"\n[sleep] Następne uruchomienie za {LOOP_INTERVAL_MIN} min...")
        time.sleep(LOOP_INTERVAL_MIN * 60)


if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        print("\nZatrzymano.")
