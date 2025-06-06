from dotenv import load_dotenv

load_dotenv()

from graph.graph_def import app
from pprint import pprint

if __name__ == '__main__':
    print("Hello Advanced RAG")
    pprint(app.invoke(input={"question": "what is agent memory?"}))   
    #pprint(app.invoke(input={"question": "how do i make a pizza?"}))