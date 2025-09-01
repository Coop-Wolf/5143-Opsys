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


# NEEDS FUNCTION COMMENT
def WelcomeMessage():
    # Welcome message
    print()
    print(f"{Fore.GREEN}Welcome to the Simple Shell!")
    print("-----------------------------------------")
    print(f"{Fore.GREEN}Available commands: clear, ls, mkdir, cd, pwd, cp, mv, rm, cat, head, tail, grep, wc, chmod, history, !x")
    print(f"{Fore.GREEN}Type '<command> --help' for information on a specific command.")
    print(f"{Fore.GREEN}Type 'exit' to quit.")
    print(f"{Fore.GREEN}Designed and implemented by Tim Haxton and Cooper Wolf.")
    print(f"{Fore.GREEN}Don't steal our code, we'll sue.")
    print("-----------------------------------------")
    print()
    
# NEEDS FUNCTION COMMENT
def exit_shell():
    print(f"{Fore.GREEN}Exiting Shell. Goodbye!")
    exit()
    
# NEEDS FUNCTION COMMENT
# STILL NEED: history, !x, and maybe others
def Command_With_No_Agrs(cmd):
    
    # If user types 'clear', clear the terminal
    if cmd == "clear":
        os.system("clear")
    
    # If user types 'pwd', print current working directory
    elif cmd == "pwd":
        print(os.getcwd())
        
    # If user types 'cd' go to home directory
    elif cmd == "cd":
        homedir = os.path.expanduser("~")
        os.chdir(homedir)
        
    # If user types 'ls', list files and directories in current directory
    elif cmd == "ls":
        for item in os.listdir():
            print(item)
            
    # If user types 'history', print command history
   #elif cmd == "history":
    
# NEEDS FUNCTION COMMENT
def change_dir(args):
    
    # Go back a directory if ".." is the argument
    if args[0] == "..":
        os.chdir("..")
                
    # Go to directory in argument if it exists
    else:
        if os.path.isdir(args[0]):
            os.chdir(args[0])
        else:
            print(f"cd: no such file or directory: {args[0]}")


#Help Functions for each command
def ls_help():
    print()
    print("ls: list directory contents")
    print("Usage: ls [OPTION]... [FILE]...")
    print("List information about the FILEs (the current directory by default).")
    print("Options:")
    print("  -a, do not ignore entries starting with .")
    print("  -l,  use a long listing format")
    print("  -h, print sizes in human readable format (e.g., 1K 234M 2G)")
    print()

def mkdir_help():
    print()
    print("mkdir: make directories")
    print("Usage: mkdir [OPTION]... DIRECTORY...")
    print("Create the DIRECTORY(ies), if they do not already exist.")
    print()

def cd_help():
    print()
    print("cd: change directory")
    print("Usage: cd [DIRECTORY]")
    print("Change the shell working directory.")
    print()

def pwd_help():
    print()
    print("pwd: print working directory")
    print("Usage: pwd")
    print("Print the name of the current working directory.")
    print()

def cp_help():
    print()
    print("cp: copy files and directories")
    print("Usage: cp [OPTION]... SOURCE... DIRECTORY")
    print("Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.")
    print()

def mv_help():
    print()
    print("mv: move (rename) files")
    print("Usage: mv [OPTION]... SOURCE... DIRECTORY")
    print("Move SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.")
    print()

def rm_help():
    print()
    print("rm: remove files or directories")
    print("Usage: rm [OPTION]... FILE...")
    print("Remove (unlink) the FILE(s).")
    print()

def cat_help():
    print()
    print("cat: concatenate and display files")
    print("Usage: cat [OPTION]... [FILE]...")
    print("Concatenate FILE(s) to standard output.")
    print()

def head_help():
    print()
    print("head: output the first part of files")
    print("Usage: head [OPTION]... [FILE]...")
    print("Print the first 10 lines of each FILE to standard output.")
    print()

def tail_help():
    print()
    print("tail: output the last part of files")
    print("Usage: tail [OPTION]... [FILE]...")
    print("Print the last 10 lines of each FILE to standard output.")
    print()

def grep_help():
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

def wc_help():
    print()
    print("wc: print newline, word, and byte counts for each file")
    print("Usage: wc [OPTION]... [FILE]...")
    print("Print newline, word, and byte counts for each FILE.")
    print("-l: print the newline counts")
    print("-w: print the word counts")
    print()

def chmod_help():
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

def history_help():
    print()
    print("history: display command history")
    print("Usage: history")
    print("Display the list of commands previously entered.")
    print()

def bangx_help():
    print()
    print("!x: execute command from history")
    print("Usage: !x")
    print("Execute the command numbered x from the history list.")
    print()

def clear_help():
    print()
    print("clear: clear the terminal screen")
    print("Usage: clear")
    print("Clear the terminal screen.")
    print()



########################### Beginning of the shell program ###########################

# Allows for colored text in terminal and resets color after each print
init(autoreset=True)

# Welcome message
WelcomeMessage()

# Loop to continuously prompt for user input
# can remove this true condition with while command != "exit" or "quit"
while True:
    
    # Allowed list of commands
    cmd_list = ["ls", "mkdir", "cd", "pwd", "cp", "mv", "rm", "cat", "head", "tail", "grep", "wc", "chmod", "history", "!x"]
    
    # Prompt for user input  
    command = input(f"{Fore.CYAN}{os.getcwd()}{Style.RESET_ALL}% ")
    
    # Split the command into tokens and parse
    token = command.split()
    cmd = token[0]
    args = token[1:]
    
    # If user types 'exit', break the loop and exit the shell
    if command == "exit":
        exit_shell()
    # If users tyles invalid command, print error message
    elif cmd not in cmd_list:
        print(f"{cmd}: command not found")
    else:
    
        # If command has no arguments
        if args == []:
            Command_With_No_Agrs(cmd)
    
        # THIS NEEDS TO BE A FUNCTION
        # Running commands that have arguments
        elif args != [] and args[0] != "--help":
        
        # change directory command with arguments
            if cmd == "cd" and len(args) == 1:
                change_dir(args)
                
            # Make Directory
            #elif cmd == "mkdir" and len(args) == 1:
            
            else:
                print("Command not recognized or not yet implemented.")
    
    
        # Help command for each command
        elif args and args[0] == "--help" and len(args) == 1:
            if cmd == "ls":
                ls_help()
            elif cmd == "mkdir":
                mkdir_help()
            elif cmd == "cd":
                cd_help()
            elif cmd == "pwd":
                pwd_help()
            elif cmd == "cp":
                cp_help()
            elif cmd == "mv":
                mv_help()
            elif cmd == "rm":
                rm_help()
            elif cmd == "cat":
                cat_help()
            elif cmd == "head":
                head_help()
            elif cmd == "tail":
                tail_help()
            elif cmd == "grep":
                grep_help()
            elif cmd == "wc":
                wc_help()
            elif cmd == "chmod":
                chmod_help()
            elif cmd == "history":
                history_help()
            elif cmd == "!x":
                bangx_help()
            elif cmd == "clear":
                clear_help()
            else:
                print("Command not recognized.")