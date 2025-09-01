"""
Program: Simple Shell
Description:
    This program implements a basic Unix-like shell in Python.
    It supports common commands such as:
        - ls, mkdir, cd, pwd, cp, mv, rm, cat, head, tail
        - grep, wc, chmod, history, !x
    The shell allows users to execute commands,
    navigate directories, and manage files interactively.

Features:
    - Execute commands with arguments
    - Directory navigation (cd, pwd)
    - File manipulation (cp, mv, rm, chmod)
    - Viewing files (cat, head, tail)
    - Searching with grep
    - Word/line counts with wc
    - Command history tracking with recall (!x)
    - Error handling for invalid commands

Authors: Tim Haxton, Cooper Wolf
Date:    9/1/2024
"""

# importing os module  
import os  

# Loop to continuously prompt for user input
while True:
    # Prompt for user input  
    command = input("% ")
    
    if command in ["exit", "quit"]:
        break
    else:
        print("Command: ", command)
    
