#!/usr/bin/python

from LinuxInputEventLogger import LinuxInputEventLogger

liel = LinuxInputEventLogger(rate=10)
liel.start()
