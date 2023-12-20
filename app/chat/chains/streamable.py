from flask import current_app
from queue import Queue
from threading import Thread
from app.chat.callbacks.stream import StreamingHandler


class StreamableChain: 
    def stream(self, input): 
        '''every time called get isolated queue & handler'''
        queue = Queue()
        handler = StreamingHandler(queue)


        def task(app_context): 
            """assign callbacks - every time run the chain 'input' 
            we're going to use the 'isolated handler' 
            Now receive app_context arg. passed in  """
            app_context.push()  # give access(curr user, db, etc.) to context inside the thread
            self(input, callbacks=[handler]) # make sure call the chain itself as we call the stream itself

        # pass an arg to task func 
        Thread(target=task, args=[current_app.app_context() ]).start()


        while True: 
            token = queue.get()
            if token is None: 
                break
            yield token