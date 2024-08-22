from sys import stdout
from time import sleep

class UI:
    
    def __init__(self):
        pass
    
    def delay_print(self, string):
        i = 0
        string += "\n"
        for char in string:
            stdout.write(char)
            stdout.flush()
            sleep(0.00) #0.04
            i += 1
            
            if i == len(string):
                sleep(0) #1   