#!/usr/bin/env python
"""
This file is about using getch to capture input and handle certain keys 
when the are pushed. The 'command_helper.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.

"""
# Need comment for imports
import os 
import sys 
import pwd
import grp
import stat
from getch import Getch
from colorama import init, Fore, Style
from time import sleep
import shutil

##################################################################################
##################################################################################

getch = Getch()  # create instance of our getch class

prompt = f"{Fore.CYAN}{os.getcwd()}{Style.RESET_ALL}$ "



def pwd_():
    """
    Print the current working directory.
    This function retrieves and prints the absolute path of the current working directory.
    Parameters:
        None
    Returns:
        None
    """
    
    # This should return instead of print
    print(os.getcwd())


def print_cmd(cmd):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    
    width = shutil.get_terminal_size((80, 20)).columns  

    # Clear line with spaces equal to width
    padding = " " * width
    sys.stdout.write("\r" + padding)
    sys.stdout.write("\r")

    # Print prompt + cleaned command
    clean_cmd = cmd.replace("\r", "")
    sys.stdout.write(f"{prompt}{clean_cmd}")
    sys.stdout.flush()


if __name__ == "__main__":
    cmd = ""  # empty cmd variable

    print_cmd(cmd)  # print to terminal

    while True:  # loop forever

        char = getch()  # read a character (but don't print)

        if char == "\x03" or cmd == "exit":  # ctrl-c
            raise SystemExit("Bye.")

        elif char == "\x7f":  # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)

        elif char in "\x1b":  # arrow key pressed
            null = getch()  # waste a character
            direction = getch()  # grab the direction

            if direction in "A":  # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)
                cmd += "\u2191"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "B":  # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                cmd += "\u2193"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "C":  # right arrow pressed
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                cmd += "\u2192"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "D":  # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                cmd += "\u2190"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            print_cmd(cmd)  # print the command (again)

        elif char in "\r":  # return pressed
            print()

            #sleep(1)

            ## YOUR CODE HERE
            ## Parse the command
            token = cmd.split()
            if token:
                cmd_ = token[0]
                #flag = token[1] if len(token) > 1 else None
                args = token[1:]
            
            if cmd == "pwd" and len(args) == 0:
                pwd_()
                
            
            ## Figure out what your executing like finding pipes and redirects

            cmd = ""  # reset command to nothing (since we just executed it)

            print_cmd(cmd)  # now print empty cmd prompt
        else:
            cmd += char 
            # add typed character to our "cmd"
            #print_cmd(cmd)  # print the cmd out