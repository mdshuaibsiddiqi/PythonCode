import logging
 
__version__ = "2018.11.03"
 
class BraceMessage(object):
    #see: https://docs.python.org/3/howto/logging-cookbook.html#using-custom-message-objects
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs
 
    def __str__(self):
        try:
            return self.msg.format(*self.args, **self.kwargs)
        except Exception as exc:
            return "Interpolation error during message formatting\n    .format({}, *{}, **{})\n{}: {}".format(
                repr(self.msg), self.args, self.kwargs,
                type(exc).__name__, str(exc))
 
class BraceLogger(logging.getLoggerClass()):
    _reserved = (('exc_info', None), ('extra', None), ('stack_info', False))
    def _log(self, level, msg, args, **kwargs):
        d = {k: kwargs.pop(k, v) for k, v in self._reserved}
        return super()._log(
            level, BraceMessage(msg, *args, **kwargs), (), **d)
     
    def __init__(self, *args, **kwargs):
        raise TypeError('BraceLogger class cannot be directly instantiated')
 
    @classmethod
    def getLogger(cls, name):
        logger = logging.getLogger(name)
        # this is frowned upon, but it is so convenient here!
        logger.__class__ = cls
        return logger
 
 
if __name__ == '__main__':
    logging.basicConfig()
    log = BraceLogger.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    log.info('{} Todays wisdom is that {x} + {y} = {z}', 'Hello!', x=1, z=3, y=2)
    val =5
    log.info("shuaib:{}", val)
    #try:
    #    1./0.
    #except Exception:
    #    log.exception('Something {} happened!', 'BAD')
    log.warning("This is the END...")