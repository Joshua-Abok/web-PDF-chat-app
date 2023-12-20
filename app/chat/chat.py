import random
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map

# from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from langchain.chat_models import ChatOpenAI
from app.web.api import (
    set_conversation_components, 
    get_conversation_components
)


def select_component(
        component_type, component_map, chat_args
):
    components = get_conversation_components(
        chat_args.conversation_id
    )
    previous_component = components[component_type]

    if previous_component: 
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_name = random.choice(list(component_map.keys()))
        builder = component_map[random_name]
        return random_name, builder(chat_args)



def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """
    
    # build retriever -> nicely scoped 
    # retriever = build_retriever(chat_args)
    retriever_name, retriever = select_component(
        "retriever", 
        retriever_map, 
        chat_args
    )

    llm_name, llm = select_component(
        "llm",
        llm_map,
        chat_args
    )

    memory_name, memory = select_component(
        "memory", 
        memory_map,
        chat_args
    )

    print(f"running CHAIN with \n memory: {memory_name}, llm: {llm_name}, retriever: {retriever_name}")

    # update the conversation with new components 
    set_conversation_components(
        chat_args.conversation_id, 
        llm=llm_name,
        retriever=retriever_name, 
        memory=memory_name
    )


    # build chain & return it 
    # llm = build_llm(chat_args)
    # separating the condense_question_llm w False 
    condense_question_llm = ChatOpenAI(streaming=False)
    # memory = build_memory(chat_args)

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm, 
        condense_question_llm=condense_question_llm,
        memory=memory, 
        retriever=retriever
    )

