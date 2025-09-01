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
# can remove this true condition with while command != "exit" or "quit"
while True:
    # Prompt for user input  
    command = input("% ")
    
    if command is "exit":
        break
    
    # Split the command into tokens and parse
    token = command.split()
    cmd = token[0]
    args = token[1:]
    
    # Running commands that have no arguments
        # STILL NEED: history, !x, and maybe others
    if args is None:
        if cmd == "pwd":
            print(os.getcwd())
        elif cmd == "cd":
            homedir = os.path.expanduser("~")
            os.chdir(homedir)
        elif cmd == "ls":
            for item in os.listdir():
                print(item)
        
    
    # Running commands that have arguments
    # if args is not None:
    
    
    # Help command for each command
    if args[0] is "--help" and len(args) == 1:
        if cmd == "ls":
            print("ls: list directory contents")
            print("Usage: ls [OPTION]... [FILE]...")
            print("List information about the FILEs (the current directory by default).")
            print("Options:")
            print("  -a, do not ignore entries starting with .")
            print("  -l,  use a long listing format")
            print("  -h, print sizes in human readable format (e.g., 1K 234M 2G)")
        if cmd == "mkdir":
            print("mkdir: make directories")
            print("Usage: mkdir [OPTION]... DIRECTORY...")
            print("Create the DIRECTORY(ies), if they do not already exist.")
        if cmd == "cd":
            print("cd: change directory")
            print("Usage: cd [DIRECTORY]")
            print("Change the shell working directory.")
        if cmd == "pwd":
            print("pwd: print working directory")
            print("Usage: pwd")
            print("Print the name of the current working directory.")
        if cmd == "cp":
            print("cp: copy files and directories")
            print("Usage: cp [OPTION]... SOURCE... DIRECTORY")
            print("Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.")
        if cmd == "mv":
            print("mv: move (rename) files")
            print("Usage: mv [OPTION]... SOURCE... DIRECTORY")
            print("Move SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.")
        if cmd == "rm":
            print("rm: remove files or directories")
            print("Usage: rm [OPTION]... FILE...")
            print("Remove (unlink) the FILE(s).")
        if cmd == "cat":
            print("cat: concatenate and display files")
            print("Usage: cat [OPTION]... [FILE]...")
            print("Concatenate FILE(s) to standard output.")
        if cmd == "head":
            print("head: output the first part of files")
            print("Usage: head [OPTION]... [FILE]...")
            print("Print the first 10 lines of each FILE to standard output.")
        if cmd == "tail":
            print("tail: output the last part of files")
            print("Usage: tail [OPTION]... [FILE]...")
            print("Print the last 10 lines of each FILE to standard output.")
        if cmd == "grep":
            print("grep: print lines matching a pattern")
            print("Usage: grep [OPTION]... PATTERN [FILE]...")
            print("Search for PATTERN in each FILE.")
            print("Pattern is a basic regular expression.")
            print("Pattern examples:")
            print("  ^abc: lines starting with 'abc'")
            print("  abc$: lines ending with 'abc'")
            print("  abc: lines containing 'abc'")
        if cmd == "wc":
            print("wc: print newline, word, and byte counts for each file")
            print("Usage: wc [OPTION]... [FILE]...")
            print("Print newline, word, and byte counts for each FILE.")
            print("-l: print the newline counts")
            print("-w: print the word counts")
        if cmd == "chmod":
            print("chmod: change file mode bits")
            print("Usage: chmod [OPTION]... [xxx] .. FILE...")
            print("Change the mode of each FILE to MODE.")
            print("First argument is the mode (e.g., 755), followed by the file name.")
            print("First value is for the owner, second for the group, third for others.")
            print("Mode is a three-digit octal number representing permissions:")
            print("7 = read, write, execute")
            print("5 = read, execute")
            print("4 = read only")
        if cmd == "history":
            print("history: display command history")
            print("Usage: history")
            print("Display the list of commands previously entered.")
        if cmd == "!x":
            print("!x: execute command from history")
            print("Usage: !x")
            print("Execute the command numbered x from the history list.")