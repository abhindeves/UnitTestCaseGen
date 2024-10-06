import datetime
import os
import openai


class AICaller:
    def __init__(self,model:str):
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        self.model = model


    def call_model(self,prompt: dict,max_tokens=4096):
        if "system" not in prompt or "user" not in prompt:
            raise ValueError("Prompt must contain both 'system' and 'user' keys")
        
        if prompt["system"] == "":
            message = [{'role':'user','content':prompt["user"]}]
        else:
            message = [{'role':'system','content':prompt["system"]},{'role':'user','content':prompt["user"]}]

        completion_params = {
            "model": self.model,
            "messages": message,
            "max_tokens": max_tokens,
            "temperature": 0.4,
        }
        
        response = self.client.chat.completions.create(**completion_params)
        return(response.choices[0].message.content,response.usage.prompt_tokens,response.usage.completion_tokens)






        
        