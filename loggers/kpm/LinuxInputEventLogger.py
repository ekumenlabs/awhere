import struct
import os
import time
from threading import Thread
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

class LinuxInputEventLogger:
    '''
    Parameters:
     - (optional, default=1) rate: (in seconds) record keystrokes ever <rate> seconds
    '''
    def __init__(self, rate=1):
        self.fn_kbd = self.detect_input_filename('event-kbd')[0]
        print "Found keyboard input interface in file: %s" % self.fn_kbd
        self.rate = rate

    '''
    Finds a device input file that matches the provided search string
    '''
    def detect_input_filename(self, search_string):
        candidates = os.listdir('/dev/input/by-path')
        candidates = filter(lambda x: x.find( search_string) != -1, candidates)
        if len(candidates) < 1:
            raise Exception("Couldn't find keyboard input event device file")
        candidates = map(lambda x: '/dev/input/by-path/%s' % x, candidates)
        return candidates
        
    def start( self):
        self.daemon = InputReaderDaemon( self.fn_kbd)
        self.daemon.start()

        while True:
            time.sleep(self.rate)
            print "KPS = %d (%d seconds)" % (self.daemon.counter,self.rate)
            self.daemon.counter = 0

    
class InputReaderDaemon(Thread):
    input_event_fmt = 'llHHl'
    input_event_names = ('seconds','microseconds','type','code','value')
    input_event_size = struct.calcsize(input_event_fmt)

    def __init__(self, filename):
        Thread.__init__(self)
        self.daemon = True
        self.f = open( filename, 'r')

        self.counter = 0

    def run(self):
        while True:
            stroke = self.read_code( self.f)
            if stroke['type'] == 1 and stroke['value'] == 1:
                self.counter += 1

    def read_code( self, input_file):
        values = struct.unpack( self.input_event_fmt, input_file.read( self.input_event_size))
        return dict(zip( self.input_event_names,values))

