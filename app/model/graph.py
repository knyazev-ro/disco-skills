from langchain.messages import AnyMessage, AIMessage
from typing_extensions import TypedDict, Annotated
from app.model.brain import decider
from langchain.messages import SystemMessage, ToolMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from app.model.prompts import pull_prompt
from app.model.tools import should_use_skill, select_subskill, determine_skill_check_difficulty, roll_dice, dice_treshold_pass, difficulty_label, boolean_response
from typing import Optional
import operator

DEPTH_LIMIT = 4

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    skill: Optional[str]
    subskill: Optional[str]
    difficulty: Optional[int]
    rolled_dice: Optional[int]
    is_passed: Optional[bool]
    depth: Optional[int]

def check_if_skill_response_needed(state: MessagesState):
    
    response = decider.invoke([
        SystemMessage(
            content=pull_prompt('skill_decision_prompt')
        ),
    ] + state['messages'])
    tool_response = None
    for tool_call in response.tool_calls:
        if tool_call['name'] == "should_use_skill":
            tool_response = should_use_skill.invoke(tool_call['args'])

    return {
        'skill': tool_response,
        'difficulty': None,
        'rolled_dice': None,
        'is_passed': None,
    }

def determine_skill(state: MessagesState):
    # what skill should we use to respond or ignore such a pussy
    if state['skill']:
    # if True:
        return "determine_subskill"
    else:
        return END

def check_if_subskill_is_set(state: MessagesState):
    # what skill should we use to respond or ignore such a pussy
    if state['subskill']:
    # if True:
        return "determine_skill_check"
    else:
        return END


def determine_subskill(state: MessagesState):
    # if skill X then what subskill Y
    response = decider.invoke([
        SystemMessage(
            content=pull_prompt('subskill_decision_prompt', skill=state['skill'], old_subskill=state['subskill'])
        ),
    ] + state['messages'])

    tool_response = None
    for tool_call in response.tool_calls:
        if tool_call['name'] == "select_subskill":
            tool_response = select_subskill.invoke(tool_call['args'])
    return {
        'subskill': tool_response,
    }

def determine_skill_check(state: MessagesState):
    # if there is skill check  or usual response - determine it
    response = decider.invoke([
        SystemMessage(
            content=pull_prompt('is_there_difficulty')
        ),
    ] + state['messages'])
    tool_response = None
    for tool_call in response.tool_calls:
        if tool_call['name'] == "determine_skill_check_difficulty":
            tool_response = determine_skill_check_difficulty.invoke(tool_call['args'])

    if tool_response is None:
        return {
        'difficulty': 1,
        'rolled_dice': 1,
        'is_passed': True,
    }
    
    rolled_dice = roll_dice()
    is_passed = dice_treshold_pass(tool_response, rolled_dice)
    return {
        'difficulty': tool_response,
        'rolled_dice': rolled_dice,
        'is_passed': is_passed,
    }

def generate_subskill_response(state: MessagesState):
    response = decider.invoke([
        SystemMessage(
            content=pull_prompt('HARDCOOORE!', **state)
        ),
    ] + state['messages'])

    response.additional_kwargs = {
        'role': state['subskill'],
        'd': state['difficulty'],
        'd_label': difficulty_label(state['difficulty']),
        'r': state['rolled_dice'],
        'p': state['is_passed'],
    }

    return {
        'messages': [response],
        "depth": (0 if state['depth'] is None else state['depth']) + 1
    }

def is_response_over(state: MessagesState):
    response = decider.invoke([
        SystemMessage(
            content=pull_prompt('is_response_over')
        ),
    ] + state['messages'])

    tool_response = None
    for tool_call in response.tool_calls:
        if tool_call['name'] == "boolean_response":
            tool_response = boolean_response.invoke(tool_call['args'])

    if tool_response and (0 if state['depth'] is None else state['depth']) <= DEPTH_LIMIT:
        return "check_if_skill_response_needed"
    else:
        return END


disco_builder = StateGraph(MessagesState)

disco_builder.add_node('check_if_skill_response_needed', check_if_skill_response_needed)
disco_builder.add_node('determine_subskill', determine_subskill)
disco_builder.add_node('determine_skill_check', determine_skill_check)
disco_builder.add_node('generate_subskill_response', generate_subskill_response)

disco_builder.add_edge(START, 'check_if_skill_response_needed')
disco_builder.add_conditional_edges('check_if_skill_response_needed', determine_skill, ['determine_subskill', END])
# disco_builder.add_edge('determine_subskill', 'determine_skill_check')
disco_builder.add_conditional_edges('determine_subskill', check_if_subskill_is_set, ['determine_skill_check', END])

disco_builder.add_edge('determine_skill_check', 'generate_subskill_response')
disco_builder.add_conditional_edges('generate_subskill_response', is_response_over, ['check_if_skill_response_needed', END])
# disco_builder.add_edge('generate_subskill_response', END)

disco_graph = disco_builder.compile()
