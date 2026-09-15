"""Точка входа: запускает игру с графическим интерфейсом."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ui import run_app

if __name__ == "__main__":
    run_app()
