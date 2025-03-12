import os, json, utils
from icl import SampleGenerator
from prompts import prompt
from generator import WandelScriptGenerator
from validate_syntax import is_valid_code
from argparse import ArgumentParser

from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.chat_models import ChatOpenAI
from prompts import prompt

load_dotenv(find_dotenv())
parser= ArgumentParser()
parser.add_argument("--query", type= str, help="User query")
args = parser.parse_args()
task_description= args.query

def build_graph(image:bool= True):

    # Instantiate Generator
    ws_gen = WandelScriptGenerator()

    # Build LangGraph State Machine
    builder = StateGraph(state_schema=dict)

    # Node 1: Generate code
    builder.add_node("Generate WS", ws_gen.generate_code)

    # Node 2: Validate code
    builder.add_node("Validate WS", ws_gen.validate_code)

    # Node 3: Prepare retry prompt
    builder.add_node("retry_prompt", ws_gen.prepare_retry_prompt)

    # Node 4: Return output node (clean end)
    builder.add_node("return_output", lambda state: state)

    # Edges
    builder.set_entry_point("Generate WS")
    builder.add_edge("Generate WS", "Validate WS")
    builder.add_conditional_edges(
        "Validate WS",
        path=lambda state: "return_output" if state.get("is_valid") else "retry_prompt"
    )
    builder.add_edge("retry_prompt", "Generate WS")
    builder.add_edge("return_output", END)

    # Compile Graph
    graph = builder.compile()

    # Run
    initial_state = {
        "system_msg": prompt,
        "user_msg": task_description
    }
    final_state = graph.invoke(initial_state)

    # Output result
    print(f"Task description: {task_description}")
    print("\nGenerated WandelScript:\n")
    if "generated_code" in final_state:
        print(final_state["generated_code"])
    else:
        print("Code not returned. Final state:\n", final_state)
    if image:
        utils.build_graph_img(graph)
    return final_state["generated_code"]

build_graph()