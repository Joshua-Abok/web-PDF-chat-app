from typing import Any, Optional, Union
from uuid import UUID
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from langchain.schema.output import ChatGenerationChunk, GenerationChunk, LLMResult
from queue import Queue
from threading import Thread


load_dotenv()

#instance of Queue()
# queue = Queue()

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
    

chat = ChatOpenAI(
    streaming=True
    # callbacks=[StreamingHandler()]      rem. don't want everyone using same handler
    )

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

# # wrap our lang model inside a chain 
# chain = LLMChain(llm=chat, prompt=prompt)

# for output in chain.stream(input={"content": "tell me a joke"}):
#     print(output)


# messages = prompt.format_messages(content="tell me a joke")

# # print(messages)
# # output = chat.invoke(messages)
# # output = chat.__call__(messages)
# output = chat.stream(messages)  # -> returns generator object BaseChatModel.stream

# # take the output bit by bit 
# for message in chat.stream(messages):
#     print(message.content)


'''Now STREAMING FROM CHAIN  
        1. Need to override the chain's "stream" method
        2. Need the "stream" method to return a generator that produces strings  
        3. The "stream" method should run the chain. 
        4. Need to get info from "on_llm_new_token" into that generator'''

    # 1. Need to override the chain's "stream" method
# subclass LLMChain & override the "stream" function
class StreamingChain(LLMChain): 
    def stream(self, input): 
        '''every time called get isolated queue & handler'''
        queue = Queue()
        handler = StreamingHandler(queue)


        def task(): 
            """assign callbacks - every time run the chain 'input' 
            we're going to use the 'isolated handler' """
            self(input, callbacks=[handler]) # make sure call the chain itself as we call the stream itself


        Thread(target=task).start()


        while True: 
            token = queue.get()
            if token is None: 
                break
            yield token

chain = StreamingChain(llm=chat, prompt=prompt) 

for output in chain.stream(input={"content": "tell me a joke"}):
    print(output)

