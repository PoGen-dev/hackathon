import logging
import functools

class Decorator: 

    def CommonDecorator(logger: logging.Logger, success: str = None, fail: str = None):
        def Decor(func):
            @functools.wraps(func)
            def Wrapper(**kwargs): 
                try: 
                    result = func(**kwargs)
                    if success: logger.info(success)
                    return result
                except Exception as e:
                    logger.exception(e)
                    if fail: 
                        logger.error(fail)
                        for key, value in kwargs.items(): 
                            try: logger.error(key, ': ', value)
                            except: logger.error("I can't write this option!")
                    return False
            return Wrapper
        return Decor