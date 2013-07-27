from os import stat
from time import time

from zope.interface import implements, Interface


class IFileMonitor(Interface):
    """ Loader uses this to check if template file was modified
    """
    def last_modified(name):
        """ Return file modification time as returned by os.stat() in st_mtime
        attribute.
        """


class IntervalMonitor(object):

    implements(IFileMonitor)

    def __init__(self, interval):
        self.interval = interval
        self.monitored = {}
        self.expire_time = time() + interval

    def last_modified(self, name):
        now = time()
        if now < self.expire_time:
            try:
                return self.monitored[name]
            except KeyError:
                pass
        else:
            self.expire_time = now + self.interval
        self.monitored[name] = last_modified = stat(name).st_mtime
        return last_modified
