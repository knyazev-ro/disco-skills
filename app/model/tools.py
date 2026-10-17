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