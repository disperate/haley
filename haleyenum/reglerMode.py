from enum import Enum

class ReglerMode(Enum):
    TO_MIDDLE = 0   # Differenz von rechter und lnker Distanz auf 0 regeln
    TO_LEFT = 1     # Distanz zur linken Bande auf 0 regeln
    TO_RIGHT = 2    # Distanz zur rechten Bande auf 0 regeln