
from queue import Queue
from threading import Thread
from app.chat.callbacks.stream import StreamingHandler


class StreamableChain: 
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