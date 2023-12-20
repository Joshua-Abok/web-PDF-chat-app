from langchain.callbacks.base import BaseCallbackHandler


# class extend BaseCallbackHandler
class StreamingHandler(BaseCallbackHandler): 
    def __init__(self, queue): 
        self.queue = queue   #isolating the queue


    def on_llm_new_token(self, token, **kwargs):
        # print(token)
        self.queue.put(token)

    
    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)

    
    def on_llm_error(self, error, **kwargs):
        '''when something goes wrong'''
        self.queue.put(None)