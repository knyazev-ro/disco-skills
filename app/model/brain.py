from langchain_ollama import ChatOllama
from app.model.tools import should_use_skill, select_subskill, determine_skill_check_difficulty, boolean_response

decider = ChatOllama(
    model="gemma4:31b-cloud",
    temperature=1,
).bind_tools([
    should_use_skill,
    select_subskill,
    determine_skill_check_difficulty,
    boolean_response,
])