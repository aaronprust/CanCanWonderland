#! /usr/bin/python3

import threading

# placeholder class to deal with the process that manages
class LightStrip (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        controlFunction(self.name, self.counter, 5)
        print "Exiting " + self.name
    def hole_in_one_pattern(self):
        print "\n()()()()()()()()()()()()\n"
        print "Make the hole in one lights go"
        print "\n()()()()()()()()()()()()\n"
        
def controlFunction(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1


"""Check for input every 0.1 seconds. Treat available input
immediately, but do something else if idle."""


import sys
import select
import time
import socket

program_id = 1
host = 'localhost'
port = 50000
size = 1024
global s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.setblocking(0)

# files monitored for input
read_list = [sys.stdin]
# select() should wait for this many seconds for input.
# A smaller number means more cpu usage, but a greater one
# means a more noticeable delay between input becoming
# available and the program starting to work on it.
timeout = 0.1 # seconds
last_work_time = time.time()
data = "default data"

def treat_input(linein):
  global last_work_time
  global s
  global pole
  print("Sending message from prompt:", linein)
  message_to_send = str(program_id) + "=" + linein
  s.send(message_to_send)
  try:
    data = s.recv(size)
    print("Message received after prompt send:", data)
    lhs, rhs = data.split("=", 1)
    print("lhs:", lhs)
    print("rhs:", rhs)
    if lhs == program_id:
      if rhs == "got_message":
        print ""
      else:            
        sys.stdout.write(str(program_id))
        sys.stdout.write("data is:" + data + ":")
        sys.stdout.write("\n=======================\n")
    elif lhs == "0":
      if rhs == "hole_in_one":
        pole.hole_in_one_pattern()
  except socket.error:
    pass
  sys.stdout.write("\n++++++++++++++++++++++++\n")
  #time.sleep(1) # working takes time
  print('Done')
  last_work_time = time.time()

def idle_work():
  global last_work_time
  global s
  global pole
  now = time.time()
  message_to_send = str(program_id) + "=" + "idle0"
  #s.send(message_to_send)
  try:
    data = s.recv(size)
    lhs, rhs = data.split("=", 1)
    lhs, rhs = data.split("=", 1)
    if lhs == program_id:
      if rhs == "got_message":
        print ""
      else:            
        sys.stdout.write(str(program_id))
        sys.stdout.write(data)
        sys.stdout.write("\n----------------------------\n")
    elif lhs == "0":
      if rhs == "hole_in_one":
        pole.hole_in_one_pattern()
  except socket.error:
    pass
    
  # do some other stuff every 2 seconds of idleness
  if now - last_work_time > 2:
    last_work_time = now

def main_loop():
  global read_list
  global pole
  pole = LightStrip(1, "Pole", 1)
  # while still waiting for input on at least one file
  while read_list:
    ready = select.select(read_list, [], [], timeout)[0]
    if not ready:
      idle_work()
    else:
      for file in ready:
        line = file.readline()
        if not line: # EOF, remove file from input list
          read_list.remove(file)
        elif line.rstrip(): # optional: skipping empty lines
          treat_input(line)

try:
    main_loop()
except KeyboardInterrupt:
  pass