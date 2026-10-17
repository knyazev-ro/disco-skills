from app.model.graph import disco_graph
from langchain.messages import HumanMessage, AnyMessage
from app.model.graph import MessagesState


messages: list[AnyMessage] = [HumanMessage(content="Uh... I don't know what happend to me...")]
initial_state: MessagesState = {
    "messages": messages,
    "skill": None,
    "subskill": None,
    "difficulty": None,
    "rolled_dice": None,
    "is_passed": None,
}

response = disco_graph.invoke(initial_state)
print(response)