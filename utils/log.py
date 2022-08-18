import time

TIME_PATTERN = "%Y-%m-%d %H:%M:%S"

class Log:

    @staticmethod
    def _show_time():
        return time.strftime(TIME_PATTERN, time.localtime())

    @staticmethod
    def info(*arg):
        print("[Mog][INFO]({}):".format(Log._show_time()), *arg)
    
    @staticmethod
    def warn(*arg):
        print("[Mog][WARN]({}):".format(Log._show_time()), *arg)
    
    @staticmethod
    def error(*arg):
        print("[Mog][ERROR]({}):".format(Log._show_time()), *arg)