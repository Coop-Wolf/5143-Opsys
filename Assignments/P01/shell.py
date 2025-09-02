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
    - Directory listing (ls)
    - Directory creation (mkdir)
    - File manipulation (cp, mv, rm, chmod)
    - Viewing files (cat, head, tail)
    - Searching with grep
    - Word/line counts with wc
    - Command history tracking with recall (!x)
    - Error handling for invalid commands

Authors: Tim Haxton, Cooper Wolf
Date:    9/1/2024
"""

# Need comment for imports
import os  
import pwd
import grp
import stat
from colorama import init, Fore, Style



def WelcomeMessage():
    """
    Prints the welcome message for the shell.

    This function displays a formatted introduction to the shell,
    including available commands and usage instructions.
    It uses colored text for better visibility.

    Parameters:
        None
    Returns:
        None
    """
    print()
    print(f"{Fore.GREEN}Welcome to the Simple Shell!")
    print("---------------------------------------------------------------------")
    print(f"{Fore.GREEN}Available commands: clear, ls, mkdir, cd, pwd, cp, mv, rm, cat, head, tail, grep, wc, chmod, history, !x")
    print(f"{Fore.GREEN}Type '<command> --help' for information on a specific command.")
    print(f"{Fore.GREEN}Type 'exit' to quit.")
    print(f"{Fore.GREEN}Designed and implemented by Tim Haxton and Cooper Wolf.")
    print(f"{Fore.GREEN}Don't steal our code, we'll sue.")
    print("---------------------------------------------------------------------")
    print()


def exit_shell():
    """
    Exits the shell program.

    This function prints a goodbye message and exits the program.

    Parameters:
        None
    Returns:
        None
    """
    print(f"{Fore.GREEN}Exiting Shell. Goodbye!")
    print()
    exit()
    
    
def cd():
    """
    Change to the home directory.
    This function changes the current working directory to the user's home directory.
    Parameters:
        None
    Returns:
        None
    """
    homedir = os.path.expanduser("~")
    os.chdir(homedir)
    
def pwd_():
    """
    Print the current working directory.
    This function retrieves and prints the absolute path of the current working directory.
    Parameters:
        None
    Returns:
        None
    """
    print(os.getcwd())
    
def clear():
    """
    Clear the terminal screen.
    This function clears the terminal screen by executing the appropriate system command.
    Parameters:
        None
    Returns:
        None
    """
    os.system("clear")
    
def ls():
    """
    List non-hidden files and directories in the current directory.
    This function lists all files and directories in the current working directory,
    excluding hidden files (those starting with a dot).
    Parameters:
        None
    Returns:
        None
    """
    for item in os.listdir():
            
        # Only print non-hidden files
        if not item.startswith('.'):
            print(item)
    
    
    
# NEEDS FUNCTION COMMENT
# STILL NEED: history, !x, and maybe others
def Command_With_No_Agrs(cmd):
    
    # If user types 'clear', clear the terminal
    if cmd == "clear":
        clear()
    
    # If user types 'pwd', print current working directory
    elif cmd == "pwd":
        pwd_()
        
    # If user types 'cd' go to home directory
    elif cmd == "cd":
        cd()
        
    # If user types 'ls', list files and directories in current directory that aren't hidden
    elif cmd == "ls":
        ls()
            
    # If user types 'history', print command history
   #elif cmd == "history":
        #history()
   #elif cmd == "!x":
        #notx()
   #elif cmd == "head":
    #    head()
   #elif cmd == "tail":
    #    tail()
   #elif cmd == "ll":
    #    ll()
    
  
def cd_with_args(args):
    """
    Change directory with arguments.

    Handles the 'cd' command when arguments are provided.
    - If args[0] == "..", goes back one directory.
    - Otherwise, tries to change into the given path.

    Parameters:
        args (list): arguments passed to 'cd'
    Returns:
        None
    """
    if args[0] == "..":
        os.chdir("..")
    else:
        if os.path.isdir(args[0]):
            os.chdir(args[0])
        else:
            print(f"cd: no such file or directory: {args[0]}")
        
        
    
def mkdir_with_args(args):
    """
    Handle the 'mkdir' command with arguments.

    Allows users to create a new directory at a specified path.
    Supports both relative and absolute paths.

    Parameters:
        args (list): List of arguments passed to the 'mkdir' command.
                     - args[0]: Name or path of the directory to create.

    Returns:
        None
    """

    # if relative path, join with current working directory
    if not os.path.isabs(args[0]):
        
        # Getting new directory name, current working directory
        # and joining them to create full path
        new_dir = args[0]
        cwd     = os.getcwd()
        path    = os.path.join(cwd, new_dir)
        
    elif os.path.isabs(args[0]):
        
        # Getting the absolute path from argumen
        path = args[0]
        
    # Creating the directory and handling errors
    try:
        os.mkdir(path)
        print("Directory created at:", path)
    except OSError as e:
        print("Error:", e)




def ls_with_args(args):
    """
    Handle the 'ls' command when arguments are provided.

    Supports listing directory contents with various options:
      - -a   Include hidden files
      - -l   Long listing format with detailed file information
      - -h   Human-readable file sizes (not fully implemented)
    Options can be combined, e.g. "-al", "-lh", etc.

    Parameters:
        args (list): List of arguments passed to the 'ls' command.
                     - args[0]: Option string (e.g., "-a", "-l", "-al", "-lh").

    Returns:
        None
    """
        
    # Using -h alone prints the same as no args
    if args[0] == "-h":
        for item in os.listdir():
            if not item.startswith('.'):
                print(item)
            
    # Using -a alone or with -h prints all files including hidden
    elif args[0] == "-a" or args[0] == "ah" or args[0] == "ha":
        for item in os.listdir():
            print(item)
        
    # Using -l alone
    elif args[0] == "-l":
        
        total_size = 0
        
        for item in os.listdir():
            if not item.startswith('.'):
                file_info = os.stat(item)
                total_size += file_info.st_blocks
        
        print("total", total_size)
        
        # Print details for each file
        for item in os.listdir():
            if not item.startswith('.'):
                
                # Get file info
                file_info = os.stat(item)  
                
                # Extract and format details  
                permissions = stat.filemode(file_info.st_mode)
                links       = file_info.st_nlink
                owner       = pwd.getpwuid(file_info.st_uid).pw_name
                group       = grp.getgrgid(file_info.st_gid).gr_name
                size        = file_info.st_size
                mod_time    = file_info.st_mtime
                
                # Print file details
                print(permissions, links, owner, group, size, mod_time, item)
         
    # Using -al or -la prints all files in long format
    elif args[0] == "-al" or args[0] == "-la":
                
        total_size = 0
        
        # Calculate total size of all files in directory
        for item in os.listdir():
            file_info = os.stat(item)
            total_size += file_info.st_blocks
        
        print("total", total_size)
        
        # Print details for each file
        for item in os.listdir():
                
            # Get file info
            file_info = os.stat(item)  
                
            # Extract and format details  
            permissions = stat.filemode(file_info.st_mode)
            links       = file_info.st_nlink
            owner       = pwd.getpwuid(file_info.st_uid).pw_name
            group       = grp.getgrgid(file_info.st_gid).gr_name
            size        = file_info.st_size
            mod_time    = file_info.st_mtime
                
            # Print file details
            print(permissions, links, owner, group, size, mod_time, item)
        
    # Using -lh or -hl prints files in long format with human readable sizes
    elif args[0] == "-lh" or args[0] == "-hl":
        
        total_size = 0
        
        # Calculate total size of all non-hidden files in directory
        
        
        #THIS NEEDS TO BE CONVERTED TO HUMAN READABLE##################$#$#$#
        for item in os.listdir():
            if not item.startswith('.'):
                file_info = os.stat(item)
                total_size += file_info.st_blocks
        
        print("total", total_size)
        
        # Print details for each file
        for item in os.listdir():
            if not item.startswith('.'):
                
                # Get file info
                file_info = os.stat(item)  
                
                # Extract and format details  
                permissions = stat.filemode(file_info.st_mode)
                links       = file_info.st_nlink
                owner       = pwd.getpwuid(file_info.st_uid).pw_name
                group       = grp.getgrgid(file_info.st_gid).gr_name
                size        = file_info.st_size
                mod_time    = file_info.st_mtime
                
                # Print file details
                print(permissions, links, owner, group, size, mod_time, item)
        
    # Using -alh or any combo of those three prints all files in long format with human readable sizes
    #elif args[0] == "-alh" or args[0] == "-ahl" or args[0] == "-lah" or args[0] == "-lha" or args[0] == "-hal" or args[0] == "-hla":
        
    # Invalid option
    else:
        print("ls: invalid option.")
        print("Try 'ls --help' for more information.")
            

#def cp_with_args(args):
#def mv_with_args(args):
#def rm_with_args(args):
#def cat_with_args(args):
#def head_with_args(args):
#def tail_with_args(args):
#def grep_with_args(args):
#def wc_with_args(args):
#def chmod_with_args(args):
 


##########################################
# Help Command Functions
#
# These functions print usage information for each supported shell command.
# Each function follows the same pattern:
#    - Print the command name
#    - Print usage syntax
#    - Print a short description
#    - Print available options (if any)
#
# Functions:
#    ls_help()       : Prints help for 'ls'
#    mkdir_help()    : Prints help for 'mkdir'
#    cd_help()       : Prints help for 'cd'
#    pwd_help()      : Prints help for 'pwd'
#    cp_help()       : Prints help for 'cp'
#    mv_help()       : Prints help for 'mv'
#    rm_help()       : Prints help for 'rm'
#    cat_help()      : Prints help for 'cat'
#    head_help()     : Prints help for 'head'
#    tail_help()     : Prints help for 'tail'
#    grep_help()     : Prints help for 'grep'
#    wc_help()       : Prints help for 'wc'
#    chmod_help()    : Prints help for 'chmod'
#    history_help()  : Prints help for 'history'
#    bangx_help()    : Prints help for '!x'
#    clear_help()    : Prints help for 'clear'
#
# Returns:
#    None (all functions only print to stdout)
##########################################
def ls_help():
    print()
    print("ls: list directory contents")
    print("Usage: ls [OPTION]... [FILE]...")
    print("List information about the FILEs (the current directory by default).")
    print("Options:")
    print("  -a, do not ignore entries starting with .")
    print("  -l,  use a long listing format")
    print("  -h, print sizes in human readable format (e.g., 1K 234M 2G)")
    print("Example: ls -alh")
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
    print("Usage: cd .. (to go back one directory)")
    print("If no argument is given, changes to the home directory.")
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

def notx_help():
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

# Print welcome message
WelcomeMessage()

# Loop to continuously prompt for user input
# can remove this true condition with while command != "exit" or "quit"
while True:
    
    # Allowed list of commands
    cmd_list = ["clear", "ls", "mkdir", "cd", "pwd", "cp", "mv", "rm", "cat", "head", "tail", "grep", "wc", "chmod", "history", "!x", "ll", "more", "less"]
    
    # Prompt for user input  
    command = input(f"{Fore.CYAN}{os.getcwd()}{Style.RESET_ALL}% ")
    
    # Split the command into tokens and parse
    token = command.split()
    cmd = token[0]
    #flag = token[1] if len(token) > 1 else None
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
                cd_with_args(args)
                
            # Make Directory
            elif cmd == "mkdir" and len(args) == 1:
                mkdir_with_args(args)
                
            # List Directory
            elif cmd == "ls" and len(args) == 1:
                ls_with_args(args) 
            #elif cmd == "cp" and len(args) == 2:
                #cp_with_args(args)
            #elif cmd == "mv" and len(args) == 2:
                #mv_with_args(args)
            #elif cmd == "rm" and len(args) == 1:
                #rm_with_args(args)
            #elif cmd == "cat" and len(args) == 1:
                #cat_with_args(args)
            #elif cmd == "head" and len(args) == 1:
                #head_with_args(args)
            #elif cmd == "tail" and len(args) == 1:
                #tail_with_args(args)
            #elif cmd == "grep" and len(args) == 2:
                #grep_with_args(args)
            #elif cmd == "wc" and len(args) == 1:
                #wc_with_args(args)
            #elif cmd == "chmod" and len(args) == 2:
                #chmod_with_args(args)
            
            else:
                print("Command not recognized or not yet implemented.")
    
    
        # Printing help messages for each command
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
                notx_help()
            elif cmd == "clear":
                clear_help()
            else:
                print("Command not recognized.")