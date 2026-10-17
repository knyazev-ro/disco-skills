from langchain.tools import tool
from random import randint
from typing import Optional

def roll_dice() -> int:
    """
    This method roll random D20 dice. Output value is integer from 1 to 20 included.  
    """
    return randint(1, 20)

def dice_treshold_pass(difficulty: int, rolled: int):
    return rolled >= difficulty

@tool
def determine_skill_check_difficulty(difficulty: int) -> int:
    """
    Based on skill check information you should determine what difficulty level is this check.
    Args:
        - difficulty: int. Accepted values: from 1 to 20 included.
    """
    return max(1, min(int(difficulty), 20))

def difficulty_label(d: int) -> str:
    if d <= 7:
        return "Trivial"
    elif d <= 9:
        return "Easy"
    elif d <= 11:
        return "Medium"
    elif d == 12:
        return "Challenging"
    elif d == 13:
        return "Formidable"
    elif d == 14:
        return "Legendary"
    elif d == 15:
        return "Heroic"
    elif d <= 17:
        return "Godly"
    else:
        return "Impossible"

@tool
def should_use_skill(skill: Optional[str]) -> Optional[str]:
    """
    This tool helps to determine is skill needed if passed specific skill name or if None we could tell that there is no need for skill response.
    Args:
        - skill: None | str
    """
    return skill

@tool
def select_subskill(subskill: str) -> str:
    """
    This tool selects subskill. Accept `subskill` string value - name of subskill.
    Args:
        - subskill: str
    """
    return subskill

@tool
def boolean_response(value: bool) -> bool:
    """
    Tool for boolean response. Returns boolean.
    Args:
        - value: bool
    """
    return bool(value)
