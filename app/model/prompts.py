from app.model.skills import skills
import json

def pull_prompt(name: str, **kwargs):

    if name == 'skill_decision_prompt':
        return f"""
        Person's brain full of aspects. Based on dialog context you should role-play with person. You play one of person's aspects of personality. 
        Aspects of personality  we call `skills`. So, each skill is different aspect of persons personality and played like different character.
        Your task is to determine which of aspects need to respond to person. 
        Using tool `should_use_skill` pass as argument None if skill response is not neccesary or one of skill names listed below if skill response would be nice touch to conversation:
        - [{", ".join(skills.keys())}]
        """
    elif name == 'subskill_decision_prompt':
        major_skill = str(kwargs.get('skill'))
        subskills = json.dumps(skills.get(major_skill), indent=4)
        return f"""
        You need to decide based on skill what subskill we need to use. *Current skill* is `{major_skill}`.
        List of related to this skill subskills:
        - {subskills}
        Your current task is crucial: based on context of dialog and current skill you need select subskill name using tool `select_subskill`.
        """
    elif name == "is_there_difficulty":
        return f"""
        You need to determine is there diffculty check or no. Its role-play, so there should be element of fun. Be creative when selects difficulty.
        For this use tool called `determine_skill_check_difficulty`. You need to pass in the arguments integer from 1 to 20 included based on dialog context (message history)
        and to not make it annoying keep track on if previous message already contained high difficulty check.
        If you think that there is no need for difficulty check then don't use this tool at all. 
        You should decide should there be this check or not, what level of difficulty should be here and etc. based on would it make dialog interesting rather than annoying or not. 
        """
    elif name == "HARDCOOORE!":
        d = int(kwargs.get('difficulty', 10))
        r = int(kwargs.get('rolled_dice', 10))
        p = kwargs.get('is_passed', True)
        skill = str(kwargs.get('skill'))
        subskill = str(kwargs.get('subskill'))
        subskill_info = json.dumps(skills[skill][subskill], indent=4)
        score = abs(int(d) - int(r))
        return f"""
        It's a step-by-step roll-dice (d20) dnd-like game. 
        Current difficulty: {d} / Current rolled dice value: {r}
        DIFFICULTY CHECK: {"PASSED" if p else "FAIL"}
        SCORE: {score}

        Based on `DIFFICULTY CHECK` result and how high is `SCORE` make perfect aunthenic response.
        NOTE: 
         - If `DIFFICULTY CHECK` is `FAIL`, then your response should NOT be helpful, it's like you don't know, have no single clue or you response is pretty obvious. Your answer should still be *in character*.
         - If `DIFFICULTY CHECK` is `PASSED`, then your response should be helpful and/or interesting. 

        Your answer *should* be IN *characher*. There is description of characher you are playing:
        {subskill_info}
        """
