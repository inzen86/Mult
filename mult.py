'''
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
with IDLE.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

'''

import os

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select


class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)


    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getche(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''

        if os.name == 'nt':
            return msvcrt.getche().decode('utf-8')

        else:
            return sys.stdin.read(1)


    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getche().
        '''

        if os.name == 'nt':
            msvcrt.getche() # skip 0xE0
            c = msvcrt.getche()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []

'''
# Test    
if __name__ == "__main__":

    kb = KBHit()

    print('Hit any key, or ESC to exit')

    while True:

        if kb.kbhit():
            c = kb.getche()
            if ord(c) == 27: # ESC
                    
            print(c)

    kb.set_normal_term()
'''

import time

class TimeoutExpired(Exception):
    pass

def input_with_timeout(prompt, timeout=10, timer=time.monotonic):
    print(prompt)
    endtime = timer() + timeout
    result = []
    kb = KBHit()
    while timer() < endtime:
        if kb.kbhit():
            c = kb.getche()
            result.append(c)
            if c == '\r':   #XXX check what Windows returns here
                kb.set_normal_term()
                return ''.join(result[:-1])
    kb.set_normal_term()
    raise TimeoutExpired

import random
timeout = int(input('Palju aega vastamiseks tahad?(sec)'))
while True:
    random.seed()
    num1 = random.randint(3,9)
    num2 = random.randint(3,9)
    prompt = str("What is  {} x {}? ".format(num1,num2))

    try:
        input = input_with_timeout(prompt, timeout)
        if input != '':
            guess = int(input)
        else:
            print('Too Slow! It\'s '+ str(num1 * num2))
            continue
    except TimeoutExpired:
        print('Too Slow! It\'s '+ str(num1 * num2))
    else:
        answer = num1*num2
        if guess == answer:
            print("Correct!")
        else :
            print("Sorry, the answer is", answer, ".")