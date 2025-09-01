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

# importing os module for directory and file operations
# importing colorama for colored terminal text
import os  
from colorama import init, Fore, Style

# Allows for colored text in terminal and resets color after each print
init(autoreset=True)


# Welcome message
print()
print(f"{Fore.GREEN}Welcome to the Simple Shell!")
print("-----------------------------------------")
print(f"{Fore.GREEN}Available commands: ls, mkdir, cd, pwd, cp, mv, rm, cat, head, tail, grep, wc, chmod, history, !x")
print(f"{Fore.GREEN}Type '<command> --help' for information on a specific command.")
print(f"{Fore.GREEN}Type 'exit' to quit.")
print(f"{Fore.GREEN}Designed and implemented by Tim Haxton and Cooper Wolf.")
print(f"{Fore.GREEN}Don't steal our code, we'll sue.")
print("-----------------------------------------")
print()

# Loop to continuously prompt for user input
# can remove this true condition with while command != "exit" or "quit"
while True:
    
    # Allowed list of commands
    cmd_list = ["ls", "mkdir", "cd", "pwd", "cp", "mv", "rm", "cat", "head", "tail", "grep", "wc", "chmod", "history", "!x"]
    
    # Prompt for user input  
    command = input(f"{Fore.CYAN}{os.getcwd()}{Style.RESET_ALL}% ")
    
    # If user types 'exit', break the loop and exit the shell
    if command == "exit":
        print(f"{Fore.GREEN}Exiting the Simple Shell. Goodbye!")
        break
    # If users tyles invalid command, print error message
    elif cmd not in cmd_list:
        print(f"{cmd}: command not found")
    else:
    
        # Split the command into tokens and parse
        token = command.split()
        cmd = token[0]
        args = token[1:]
    
    # THIS NEEDS TO BE A FUNCTION
    # Running commands that have no arguments
        # STILL NEED: history, !x, and maybe others
        if args == []:
            if cmd == "pwd":
                print(os.getcwd())
            elif cmd == "cd":
                homedir = os.path.expanduser("~")
                os.chdir(homedir)
            elif cmd == "ls":
                for item in os.listdir():
                    print(item)
        
    
    # THIS NEEDS TO BE A FUNCTION
    # Running commands that have arguments
        if args != [] and args[0] != "--help":
        
        # change directory command with arguments
            if cmd == "cd" and len(args) == 1:
            
            # Go back a directory if ".." is the argument
                if args[0] == "..":
                    os.chdir("..")
                
            # Go to directory in argument if it exists
                else:
                    if os.path.isdir(args[0]):
                        os.chdir(args[0])
                    else:
                        print(f"cd: no such file or directory: {args[0]}")
            else:
                print(f"cd: too many arguments")
    
    
    # Help command for each command
        if args and args[0] == "--help" and len(args) == 1:
            if cmd == "ls":
                print()
                print("ls: list directory contents")
                print("Usage: ls [OPTION]... [FILE]...")
                print("List information about the FILEs (the current directory by default).")
                print("Options:")
                print("  -a, do not ignore entries starting with .")
                print("  -l,  use a long listing format")
                print("  -h, print sizes in human readable format (e.g., 1K 234M 2G)")
                print()
            if cmd == "mkdir":
                print()
                print("mkdir: make directories")
                print("Usage: mkdir [OPTION]... DIRECTORY...")
                print("Create the DIRECTORY(ies), if they do not already exist.")
                print()
            if cmd == "cd":
                print()
                print("cd: change directory")
                print("Usage: cd [DIRECTORY]")
                print("Change the shell working directory.")
                print()
            if cmd == "pwd":
                print()
                print("pwd: print working directory")
                print("Usage: pwd")
                print("Print the name of the current working directory.")
                print()
            if cmd == "cp":
                print()
                print("cp: copy files and directories")
                print("Usage: cp [OPTION]... SOURCE... DIRECTORY")
                print("Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.")
                print()
            if cmd == "mv":
                print()
                print("mv: move (rename) files")
                print("Usage: mv [OPTION]... SOURCE... DIRECTORY")
                print("Move SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.")
                print()
            if cmd == "rm":
                print()
                print("rm: remove files or directories")
                print("Usage: rm [OPTION]... FILE...")
                print("Remove (unlink) the FILE(s).")
                print()
            if cmd == "cat":
                print()
                print("cat: concatenate and display files")
                print("Usage: cat [OPTION]... [FILE]...")
                print("Concatenate FILE(s) to standard output.")
                print()
            if cmd == "head":
                print()
                print("head: output the first part of files")
                print("Usage: head [OPTION]... [FILE]...")
                print("Print the first 10 lines of each FILE to standard output.")
                print()
            if cmd == "tail":
                print()
                print("tail: output the last part of files")
                print("Usage: tail [OPTION]... [FILE]...")
                print("Print the last 10 lines of each FILE to standard output.")
                print()
            if cmd == "grep":
                print()
                print("grep: print lines matching a pattern")
                print("Usage: grep [OPTION]... PATTERN [FILE]...")
                print("Search for PATTERN in each FILE.")
                print("Pattern is a basic regular expression.")
                print("Pattern examples:")
                print("  ^abc: lines starting with 'abc'")
                print("  abc$: lines ending with 'abc'")
                print("  abc: lines containing 'abc'")
                print()
            if cmd == "wc":
                print()
                print("wc: print newline, word, and byte counts for each file")
                print("Usage: wc [OPTION]... [FILE]...")
                print("Print newline, word, and byte counts for each FILE.")
                print("-l: print the newline counts")
                print("-w: print the word counts")
                print()
            if cmd == "chmod":
                print()
                print("chmod: change file mode bits")
                print("Usage: chmod [OPTION]... [xxx] .. FILE...")
                print("Change the mode of each FILE to MODE.")
                print("First argument is the mode (e.g., 755), followed by the file name.")
                print("First value is for the owner, second for the group, third for others.")
                print("Mode is a three-digit octal number representing permissions:")
                print("7 = read, write, execute")
                print("5 = read, execute")
                print("4 = read only")
                print()
            if cmd == "history":
                print()
                print("history: display command history")
                print("Usage: history")
                print("Display the list of commands previously entered.")
                print()
            if cmd == "!x":
                print()
                print("!x: execute command from history")
                print("Usage: !x")
                print("Execute the command numbered x from the history list.")
                print()