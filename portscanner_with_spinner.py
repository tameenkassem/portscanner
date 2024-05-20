#pip install rich

import pyfiglet
import sys
import socket
import threading
from datetime import datetime
from queue import Queue
import time
import itertools
import time
import threading

def spinner():
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while not all_scans_done.is_set():  # all_scans_done is a threading.Event
        sys.stdout.write(next(spinner))  # write the next spinner character
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')  # use backspace to erase the last character



ascii_banner = pyfiglet.figlet_format ("PORT SCANNER")
print(ascii_banner)

#creates a lockk to prevent multiple threads from printing to the console at the same time, which can jumble the output
print_lock = threading.Lock()

#creating variable for user to input target IP as string
target = input(str("Target IP: "))

#banner
print("_" * 50)
print("Scanning Target: " + target)
print("Scanning started at: " + str(datetime.now()))
print("_" * 50)

all_scans_done = threading.Event()
spinner_thread = threading.Thread(target=spinner)
spinner_thread.start()


def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.5)

    try:
        result = s.connect_ex((target,port))
        if result == 0:
            with print_lock:
                print("[*] Port {} is open".format(port))
            s.close
    except:
        pass


#threader function
def threader():
    while True:
        #gets a worker (port) from the queue
        worker = q.get()
        #scans that worker(port)
        scan(worker)
        #completed with the job
        q.task_done()

q = Queue()

#how many threads are we going to allow for
for x in range(100): #n. of threads
    t = threading.Thread(target=threader)
    #classifying as a daemon, so they will die when  the main dies.
    t.daemon = True
    #begins, must come after daemon definition
    t.start()

#each job assigned to new worker in queue
for worker in range(1, 65535):
    q.put(worker)

#wait until the thread terminates.
q.join()

# After q.join(), which waits for all scanning tasks to complete
all_scans_done.set()  # Signal that all scans are done
spinner_thread.join()  # Wait for the spinner thread to finish

print("Scanning completed at:" + str(datetime.now()))

        


#scan every port on target ip
#try:
    #for port in range(1, 65535):
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       # socket.setdefaulttimeout(0.5)

        #return open port (finds open port, create the variable named result
        #result = socket target & port, if result is 0 = successful, prints string with port 
        #result = s.connect_ex((target,port))
        #if result == 0:
         #   print("[*] Port {} is open".format(port))
        #s.close

#except KeyboardInterrupt:
 #       print("\n Exiting :(")
  #      sys.exit()

#except socket.error:
    #    print("\ Host not responding :(")
   #     sys.exit()
    

    