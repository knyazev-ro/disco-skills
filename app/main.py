from app.model.graph import disco_graph
from langchain.messages import HumanMessage, AnyMessage
from app.model.graph import MessagesState
from app.voices.flow import narrate
from app.voices.rvc import rvc
from app.voices.tts import tts_model

def display_dialog(history: list[AnyMessage]):
    for m in history:
        if isinstance(m, HumanMessage):
            print(f"YOU {m.content}")
        else:
            meta = m.additional_kwargs
            print(f"{meta['role']} [{meta['d_label']}: {'Success' if meta['p'] else 'Fail'}] {m.content}")
        print('\n')

messages: list[AnyMessage] = []

while True:
    income_message = input('>: ') 

    state: MessagesState = {
        "messages": messages + [HumanMessage(content=income_message)],
        "skill": None,
        "subskill": None,
        "difficulty": None,
        "rolled_dice": None,
        "is_passed": None,
    }

    response = disco_graph.invoke(state)
    
    messages = response['messages']
    last = messages[-1]
    display_dialog(messages)
    
    text = last.text
    
    narrate(str(last.text))
    