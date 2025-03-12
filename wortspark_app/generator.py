from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.chat_models import ChatOpenAI
import json, os
from validate_syntax import is_valid_code
from icl import SampleGenerator
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
openai_api_key= os.getenv('openai_api_key')
sample_generator = SampleGenerator()
icl_samples= sample_generator.demonstrations()
class WandelScriptGenerator:
    def __init__(self, model="gpt-4"):
        self.model = model

    def generate_code(self, state):
        system_msg, user_msg = state['system_msg'], state['user_msg']
        messages = [
            SystemMessage(content=system_msg, **{"icl_samples": icl_samples}),
            HumanMessage(content=user_msg)
        ]
        llm = ChatOpenAI(openai_api_key=openai_api_key,
                         temperature=0.7,
                         model=self.model,
                         verbose=True)
        result = llm.invoke(messages)
        generated_output = json.loads(result.content)
        return {
            "system_msg": system_msg,
            "user_msg": user_msg,
            "generated_code": generated_output["code"]
        }

    def validate_code(self, state):
        code = state["generated_code"]
        is_valid, error_msg = is_valid_code(code)
        state["is_valid"] = is_valid
        state["error_msg"] = error_msg
        return state

    def prepare_retry_prompt(self, state):
        consolidated_prompt = (
            f"The previous code generation failed due to the following syntax errors:\n"
            f"{state['error_msg']}\n\n"
            f"Task Description: {state['user_msg']}\n\n"
            f"Generated Code:\n{state['generated_code']}\n\n"
            f"Please regenerate a syntactically correct script that resolves the above errors."
        )
        return {
            "system_msg": state["system_msg"],
            "user_msg": consolidated_prompt
        }