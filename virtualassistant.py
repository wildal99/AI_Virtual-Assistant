from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

#used for connecting to wiz lights
import pywizlight

load_dotenv()

#inspired from: https://www.youtube.com/watch?v=XZdY15sHUa8


#tools
@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmeric calculations with numbers"""
    print("Tool has been called.")
    return f"The sum of {a} and {b} is {a + b}"
    
@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user"""
    print("Tool has been called.")
    return f"Hello {name}, I hope you are well today"

@tool
def adjustLight(light: str) -> str:
    """useful for adjusting a light"""
    print("adjust light tool has been called")
    light = wizlight("192.168.1.27")
    timeout = 10 
    light.turn_on(PilotBuilder(rgb = (255, 0, 0)))
    return f"I have adjusted the {light}"

@tool
def startCar(car: str) -> str:
    """useful for remote starting a car"""
    print("Tool has been called")
    print("this would be an api call to your IoT.")
    return f"I have started your {car}"

#main function
def main():
    model = ChatOpenAI(temperature=0)
    
    tools = [calculator, say_hello, adjustLight, startCar]
    agent_executor = create_react_agent(model, tools)
    
    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")
    
    #get user input
    while True:
        user_input = input("\nYou: ").strip()
        
        #quit
        if user_input == "quit":
            break
        
        #stream agent responses word by word
        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()
        
#run this when started from a terminal
if __name__ == "__main__":
    main()