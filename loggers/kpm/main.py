#!/usr/bin/python

import struct

input_event_fmt = 'llHHl'
input_event_names = ('seconds','microseconds','type','code','value')

'''
struct input_event {
         struct timeval time;
         __u16 type;
         __u16 code;
         __s32 value;
};

total size = 32 + 16 + 16 + 32 + 32 = 128

 20 struct timeval {
 21         __kernel_time_t         tv_sec;         /* seconds */ --- long
 22         __kernel_suseconds_t    tv_usec;        /* microseconds */ --- 
 23 };

#define __BITS_PER_LONG 32

typedef long		__kernel_suseconds_t;
typedef long		__kernel_time_t;

'''
    
def read_code():
    values = struct.unpack( input_event_fmt, keyb.read(input_event_size))
    return dict(zip(input_event_names,values))

input_event_size = struct.calcsize(input_event_fmt)

keyb = open('/dev/input/event3','r')
while True:
#for i in range(50):
    stroke = read_code()
    if stroke['type'] == 1 and stroke['value'] == 1:
        print "Pressed key: %s (%s)" % (stroke['code'] , stroke['value'])
    
