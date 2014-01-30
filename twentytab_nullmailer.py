"""
Copyright 2014 20Tab S.r.l.
"""
import os
import asyncore
import time
from smtpd import SMTPServer

class Nullmailer(SMTPServer):

    __counter__ = 0
    __pid__ = os.getpid()
    __queue__ = "/var/spool/nullmailer/queue"
    __tmp__ = "/var/spool/nullmailer/tmp"
    __trigger__ = "/var/spool/nullmailer/trigger"

    def fsyncspool(self):
        """
        Call fsync() on the queue directory
        """
        fd = -1
        try:
            fd = os.open(self.__queue__, os.O_RDONLY)
            os.fsync(fd)
        finally:
            if fd > -1: os.close(fd)

    def trigger(self):
        """
        Wakeup nullmailer writing to its trigger fifo
        """
        fd = -1
        try:
            fd = os.open(self.__trigger__, os.O_WRONLY|os.O_NONBLOCK)
            os.write(fd, "\0")
        finally:
            if fd > -1: os.close(fd)
    

    def process_message(self, peer, mailfrom, rcpttos, data):
        self.__counter__ += 1
        filename = "%f_%s_%d_%d" % (time.time(), time.strftime("%Y.%m.%d.%H.%M.%S"), self.__pid__, self.__counter__)
        tmp = "%s/%s" % (self.__tmp__, filename)
        spool = "%s/%s" % (self.__queue__, filename)

        with open(tmp, 'w') as f:
            f.write(mailfrom + '\n')
            for rcpt in rcpttos:
                f.write(rcpt + '\n')
            f.write('\n' + data)

        try:
            os.link(tmp, spool)
            self.fsyncspool() 
            self.trigger()
        finally:
            os.unlink(tmp)
    

if __name__ == '__main__':
    server = Nullmailer(('127.0.0.1', 1025), None)
    asyncore.loop()
