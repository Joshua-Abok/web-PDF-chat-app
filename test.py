from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

# wrap our lang model inside a chain 
chain = LLMChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "tell me a joke"}):
    print(output)


# messages = prompt.format_messages(content="tell me a joke")

# # print(messages)
# # output = chat.invoke(messages)
# # output = chat.__call__(messages)
# output = chat.stream(messages)  # -> returns generator object BaseChatModel.stream

# # take the output bit by bit 
# for message in chat.stream(messages):
#     print(message.content)