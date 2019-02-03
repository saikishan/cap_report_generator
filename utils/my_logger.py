import logging,threading
from utils.email_dispatcher import PostMan
mailler = PostMan(__name__)


class MyLogger(logging.Logger):
    def __init__(self, name, level = logging.NOTSET):
        self._count = 0
        self._countLock = threading.Lock()
        super(MyLogger, self).__init__(name, level)

    def error(self, msg, *args, **kwargs):
        def get_args_msg():
            msg = ""
            for x in args:
                msg += str(x)+ "  \n"
            return msg

        def get_kwargs_msg():
            msg = ""
            for x in kwargs:
                msg += str(x) + " : " + " + "+  str(kwargs[x]) + "\n"
            return msg

        error_message = """
            list of args: 
            {args_msg}
            
            list of **kwargs:
            {kwargs_msg}
        """.format(args_msg = get_args_msg(), kwargs_msg= get_kwargs_msg())
        mailler.developer_alert(subject=msg, text=error_message)
        super(MyLogger, self).error(msg,*args,**kwargs)