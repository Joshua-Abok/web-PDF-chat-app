from langfuse.model import CreateTrace
from app.chat.tracing.langfuse import langfuse

class TraceableChain: 
    def __call__(self, *args, **kwargs):
        """
        override default implementation on parent class 
        this function gets executed every time run chain 
        -> Now let's override it & add in args we need to be present"""
        # print("HI THERE!")
        # print(self.metadata)  # convo metadata 

        trace = langfuse.trace(
            CreateTrace(
                id=self.metadata["conversation_id"], 
                metadata=self.metadata
            )
        )
        # one of **kwargs -> list of callbacks, if doesn't exist default to empty list
        callbacks = kwargs.get("callbacks", [])
        callbacks.append(trace.getNewHandler()) # append
        kwargs["callbacks"] = callbacks       # reassign list of callbacks back to kwargs
        return super().__call__(*args, **kwargs)