import os
import time
import unittest


class IntervalMonitorTests(unittest.TestCase):

    def makeOne(self, *args, **kwargs):
        from pyramid_breve.monitor import IntervalMonitor
        return IntervalMonitor(*args, **kwargs)

    def setUp(self):
        self.file_name = os.tempnam()
        file(self.file_name, 'w').close()

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.unlink(self.file_name)

    def test_interval(self):
        delay = 1

        monitor = self.makeOne(delay * 3)
        file_name = self.file_name

        last_mod = monitor.last_modified(file_name)

        time.sleep(delay)
        os.utime(file_name, None)
        assert last_mod == monitor.last_modified(file_name)

        time.sleep(delay * 3)
        os.utime(file_name, None)
        assert last_mod < monitor.last_modified(file_name)
