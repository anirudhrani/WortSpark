import os, json
from icl import SampleGenerator
from prompts import prompt

from dotenv import load_dotenv, find_dotenv
from langchain_openai import  ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
load_dotenv(find_dotenv())

sample_generator = SampleGenerator()
icl_samples= sample_generator.demonstrations()

class WandelScriptGenerator():
    """Calls the open ai API with the prompt, human input and generates relevant wandelscript code.
    system_msg: The prompt template
    user_msg: Human Input (Natural language query).
    """
    def __init__(self, system_msg, user_msg):
        self.messages= messages= [
    SystemMessage(content= system_msg, **{"icl_samples":icl_samples}),
    HumanMessage(content= user_msg)
]
    def execute(self,  model="gpt-4o-mini", json_output= True):
        """Calls the open AI api, captures and returns the response.
        model: model name as a string.
        json_output:Bool -> If the user requires the output in a json format."""
        llm= chat_model= ChatOpenAI(openai_api_key= os.getenv("OPENAI_API_KEY"),
                    temperature= 0.7,
                    model= model,
                    verbose= True)
        result= llm.invoke(self.messages)
        if json_output:
            json_obj = json.loads(result.content)
            return json_obj
        return result

gen= WandelScriptGenerator(system_msg= prompt, user_msg="Move from home to a position A with a UR5 robot.")
print(gen.execute()['code'])