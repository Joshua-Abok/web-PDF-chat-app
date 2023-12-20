from typing import Any, Dict, List, Optional
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.messages import BaseMessage


# class extend BaseCallbackHandler
class StreamingHandler(BaseCallbackHandler): 
    def __init__(self, queue): 
        self.queue = queue   #isolating the queue
        self.streaming_run_ids = set()  # keep track of all run_ids corresponding to the model 
                                            #  with streaming=True


    def on_chat_model_start(self, serialized, messages, run_id, **kwargs):
        # print("this is conf_of_lang_model", serialized)
        # print("this is random_gen_id", run_id)
        if serialized["kwargs"]["streaming"]: 
            # print("This is a streaming model! I should listen to events with run_id", run_id)
            self.streaming_run_ids.add(run_id)


    def on_llm_new_token(self, token, **kwargs):
        # print(token)
        self.queue.put(token)

    
    def on_llm_end(self, response, run_id, **kwargs):
        if run_id in self.streaming_run_ids: 
            self.queue.put(None)
            self.streaming_run_ids.remove(run_id) # run_id not needed anywhere

    
    def on_llm_error(self, error, **kwargs):
        '''when something goes wrong'''
        self.queue.put(None)