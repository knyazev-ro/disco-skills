from app.model.graph import disco_graph
from langchain.messages import HumanMessage, AnyMessage
from app.model.graph import MessagesState

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
        'depth': None,
    }

    response = disco_graph.invoke(state)

    # if (len(response['messages']) <= len(messages)):
    #     continue

    messages = response['messages']
    print(len(messages))
    display_dialog(messages)