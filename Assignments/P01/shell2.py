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
import time
from time import sleep
import shutil

##################################################################################
##################################################################################

getch = Getch()  # create instance of our getch class


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
    print(f"{Fore.GREEN}To see avaiable commands, type 'help' [Need to implement help command].")
    print(f"{Fore.GREEN}Type '<command> --help' for information on a specific command.")
    print(f"{Fore.GREEN}Type 'exit' or ctrl + c to quit.")
    print(f"{Fore.GREEN}Designed and implemented by Tim Haxton, Person 3, and Cooper Wolf.")
    print(f"{Fore.GREEN}Don't steal our code, we'll sue.")
    print("---------------------------------------------------------------------")
    print()


def pwd_():
    """
    Print the current working directory.
    This function retrieves and prints the absolute path of the current working directory.
    Parameters:
        None
    Returns:
        str: The current working directory path.
    """
    
    return os.getcwd()


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
    
    # List to hold directory contents
    items = []
    
    # This should return the list instead of print
    for item in os.listdir():
            
        # Only print non-hidden files
        if not item.startswith('.'):
            
            # Getting the full path of the item
            full_path = os.path.join(os.getcwd(), item)
            
            # If item is a directory, print in blue
            if os.path.isdir(full_path):
                items.append(f"{Fore.BLUE}{item}{Style.RESET_ALL}")
            
            # If item is an executable file, print in green
            elif os.access(full_path, os.X_OK):
                items.append(f"{Fore.GREEN}{item}{Style.RESET_ALL}")
                
            # Otherwise, print normally
            else:
                items.append(item)
                
    # Sort the items alphabetically before returning
    items.sort()
    return items


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
    
    # List to hold directory contents
    items = []
    
    # Using -h alone prints the same as no args
    if args[0] == "-h":       
        return (ls())
            
    # Using -a alone or with -h prints all files including hidden
    elif args[0] == "-a" or args[0] == "ah" or args[0] == "ha":
        
        for item in ['.', '..'] + os.listdir():
            
            # Getting the full path of the item
            full_path = os.path.join(os.getcwd(), item)
            
            # If item is a directory, print in blue
            if os.path.isdir(full_path):
                items.append(f"{Fore.BLUE}{item}{Style.RESET_ALL}")
            
            # If item is an executable file, print in green
            elif os.access(full_path, os.X_OK):
                items.append(f"{Fore.GREEN}{item}{Style.RESET_ALL}")
                
            # Otherwise, print normally
            else:
                items.append(item)
                
        items.sort() 
        return(items) 
        
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
                full_path = os.path.join(os.getcwd(), item)
                file_info = os.stat(full_path)

                # Extract and format details
                permissions = stat.filemode(file_info.st_mode)
                links = file_info.st_nlink
                owner = pwd.getpwuid(file_info.st_uid).pw_name
                group = grp.getgrgid(file_info.st_gid).gr_name
                size = file_info.st_size
                mod_time = time.strftime("%b %d %H:%M", time.localtime(file_info.st_mtime))

                # Color the name
                if os.path.isdir(full_path):
                    name = Fore.BLUE + item + Style.RESET_ALL
                elif os.access(full_path, os.X_OK):
                    name = Fore.GREEN + item + Style.RESET_ALL
                else:
                    name = item

                # Append as a list (one per file)
                items.append([permissions, links, owner, group, size, mod_time, name])
                
        # Sort items by filename
        items = sorted(items, key=lambda x: x[-1].lower())
        return items
         
    # Using -al or -la prints all files in long format
    elif args[0] == "-al" or args[0] == "-la":
                
        total_size = 0
        
        # Calculate total size of all files in directory
        for item in ['.', '..'] + os.listdir():
            file_info = os.stat(item)
            total_size += file_info.st_blocks
        
        print("total", total_size)
        
        # Print details for each file
        for item in ['.', '..'] + os.listdir():
                
            # Get file info
            full_path = os.path.join(os.getcwd(), item)
            file_info = os.stat(full_path)
            
            # Extract and format details
            permissions = stat.filemode(file_info.st_mode)
            links = file_info.st_nlink
            owner = pwd.getpwuid(file_info.st_uid).pw_name
            group = grp.getgrgid(file_info.st_gid).gr_name
            size = file_info.st_size
            mod_time = time.strftime("%b %d %H:%M", time.localtime(file_info.st_mtime))

            # Color the name
            if os.path.isdir(full_path):
                name = Fore.BLUE + item + Style.RESET_ALL
            elif os.access(full_path, os.X_OK):
                name = Fore.GREEN + item + Style.RESET_ALL
            else:
                name = item

            # Append as a list (one per file)
            items.append([permissions, links, owner, group, size, mod_time, name])
                
        # Sort items by filename
        items = sorted(items, key=lambda x: x[-1].lower())
        return items
        
    # Using -lh or -hl prints files in long format with human readable sizes
    elif args[0] == "-lh" or args[0] == "-hl":
        
        total_size = 0
        
        # Calculate total size of all non-hidden files in directory
        for item in os.listdir():
            if not item.startswith('.'):
                file_info = os.stat(item)
                total_size += file_info.st_size
        
        print("total", human_readable(total_size))
        
        # Print details for each file
        for item in os.listdir():
            if not item.startswith('.'):
                
                # Get file info
                full_path = os.path.join(os.getcwd(), item)
                file_info = os.stat(full_path)

                # Extract and format details
                permissions = stat.filemode(file_info.st_mode)
                links = file_info.st_nlink
                owner = pwd.getpwuid(file_info.st_uid).pw_name
                group = grp.getgrgid(file_info.st_gid).gr_name
                size = human_readable(file_info.st_size)
                mod_time = time.strftime("%b %d %H:%M", time.localtime(file_info.st_mtime))

                # Color the name
                if os.path.isdir(full_path):
                    name = Fore.BLUE + item + Style.RESET_ALL
                elif os.access(full_path, os.X_OK):
                    name = Fore.GREEN + item + Style.RESET_ALL
                else:
                    name = item

                # Append as a list (one per file)
                items.append([permissions, links, owner, group, size, mod_time, name])
                
        # Sort items by filename
        items = sorted(items, key=lambda x: x[-1].lower())
        return items
        
    # Using -alh or any combo of those three prints all files in long format with human readable sizes
    elif args[0] == "-alh" or args[0] == "-ahl" or args[0] == "-lah" or args[0] == "-lha" or args[0] == "-hal" or args[0] == "-hla":
        
        total_size = 0
        
        # Calculate total size of all files in directory
        for item in ['.', '..'] + os.listdir():
            file_info = os.stat(item)
            total_size += file_info.st_size
        
        print("total", human_readable(total_size))
        
        # Print details for each file
        for item in ['.', '..'] + os.listdir():
                
            # Get file info
            full_path = os.path.join(os.getcwd(), item)
            file_info = os.stat(full_path)

            # Extract and format details
            permissions = stat.filemode(file_info.st_mode)
            links = file_info.st_nlink
            owner = pwd.getpwuid(file_info.st_uid).pw_name
            group = grp.getgrgid(file_info.st_gid).gr_name
            size = human_readable(file_info.st_size)
            mod_time = time.strftime("%b %d %H:%M", time.localtime(file_info.st_mtime))

            # Color the name depending on type
            if os.path.isdir(full_path):
                name = Fore.BLUE + item + Style.RESET_ALL
            elif os.access(full_path, os.X_OK):
                name = Fore.GREEN + item + Style.RESET_ALL
            else:
                name = item

            # Append as a list (one per file)
            items.append([permissions, links, owner, group, size, mod_time, name])
                
        # Sort items by filename
        items = sorted(items, key=lambda x: x[-1].lower())
        return items
        
    # Invalid option
    else:
        print("ls: invalid option.")
        print("Try 'ls --help' for more information.")
    
    
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
    
    
def exit_shell():
    """
    Exits the shell program.

    This function prints a goodbye message and exits the program.

    Parameters:
        None
    Returns:
        None
    """
    
    raise SystemExit(f"{Fore.GREEN}Exiting Shell. Goodbye!")


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

    if os.path.isabs(args[0]):
        
        # Getting the absolute path from argumen
        path = args[0]

    # if relative path, join with current working directory
    elif not os.path.isabs(args[0]):
        
        # Getting new directory name, current working directory
        # and joining them to create full path
        new_dir = args[0]
        cwd     = os.getcwd()
        path    = os.path.join(cwd, new_dir)
        
    # Creating the directory and handling errors
    try:
        os.mkdir(path)
    except OSError as e:
        print("Error:", e)
        
        
def human_readable(size):
    """
    Convert a file size in bytes to a human-readable format.

    This function takes a file size in bytes and converts it to a more
    human-friendly format (e.g., K, M, G) with two decimal places.

    Parameters:
        size (int): The file size in bytes.

    Returns:
        str: The file size in a human-readable format.
    """
    
    # Convert size to float for division
    size = float(size)
    
    # Define units for conversion
    units = ["K", "M", "G"]
    i = 0

    # Loop to convert size to appropriate unit
    while size >= 1024 and i < len(units):
        size /= 1024
        i += 1

    # If size is less than 1K, show in bytes without decimal
    if i == 0:
        return f"{int(size)}"
    
    # Otherwise, show with one decimal place and appropriate unit
    else:
        return f"{size:.1f}{units[i-1]}"
    

def print_cmd(cmd, cursor_pos=0):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    
    width = shutil.get_terminal_size((80, 20)).columns  

    # Clear line with spaces equal to width
    padding = " " * width
    sys.stdout.write("\r" + padding + "\r")
    
    # Update prompt with current working directory
    prompt = f"{Fore.CYAN}{os.getcwd()}{Style.RESET_ALL}$ "

    # Print prompt
    sys.stdout.write(f"{prompt}{cmd}")
    
    # clean_cmd = cmd.replace("\r", "")
    #sys.stdout.write(f"{prompt}{clean_cmd}")
    
    # Move cursor to correct position
    sys.stdout.write("\r" + prompt + cmd[:cursor_pos])
    sys.stdout.flush()



# MAIN PROGRAM
if __name__ == "__main__":
    
    # Allows for colored text in terminal and resets color after each print
    init(autoreset=True)

    # Print welcome message
    WelcomeMessage()
    
    cmd = ""  # empty cmd variable
    
    # For handling left/right arrow keys
    cursor_pos = 0

    print_cmd(cmd)  # print to terminal

    while True:  # loop forever

        # read a single character, don't print
        char = getch()

        # Exit shell on ctrl-c or 'exit' command
        if char == "\x03" or cmd == "exit":
            exit_shell()

        # If back space pressed, remove the character to the left of the cursor
        elif char == "\x7f":
            if cursor_pos > 0:
                cmd = cmd[:cursor_pos-1] + cmd[cursor_pos:]
                cursor_pos -= 1
            print_cmd(cmd, cursor_pos)

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
                if cursor_pos < len(cmd):
                    cursor_pos += 1
                print_cmd(cmd, cursor_pos)

            if direction in "D":  # left arrow pressed
                # moves the cursor to the left on your command prompt line
                if cursor_pos > 0:
                    cursor_pos -= 1
                print_cmd(cmd, cursor_pos)
              
                
        # return pressed
        elif char in "\r":
            print()

            #sleep(1)

            ## YOUR CODE HERE
            ## Parse the command
            token = cmd.split()
            if token:
                cmd_ = token[0]
                #flag = token[1] if len(token) > 1 else None
                args = token[1:]
                
            # Searching for valid commands with no arguments
            if cmd_ and len(args) == 0:
            
                # Printing current working directory
                if cmd_ == "pwd":
                    cwd_ = pwd_()
                    print(cwd_)
                   
                # Changing to home directory 
                elif cmd_ == "cd":
                    cd()
                    
                # Listing non-hidden files and directories
                elif cmd_ == "ls":
                    items = ls()
                    for item in items:
                        print(item, end=" ")
                    print()
                    
                # Clearing the terminal
                elif cmd_ == "clear":
                    clear()
                
            # Searching for valid commands with arguments
            elif cmd_ and len(args) == 1:
                
                # Changing directory with arguments
                if cmd_ == "cd":
                    cd_with_args(args)
                    
                # Making directory with arguments
                elif cmd_ == "mkdir":
                    mkdir_with_args(args)
                    
                # Listing files and directories with arguments
                elif cmd_ == "ls":
                    items = ls_with_args(args)
                    
                    # If using -l , -la, or -lah options, print in formatted columns
                    if args[0] in ["-l", "-al", "-la", "-lh", "-hl", "-alh", "-ahl", "-lah", "-lha", "-hal", "-hla"]:
                        for item in items:
                            print(f"{item[0]:<10} {item[1]:<3}{item[2]:<8}{item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}")
                    
                    # Otherwise, just print the items
                    else:
                        for item in items:
                            print(item, end=" ")
                        print()
                        
                        
            # Figure out what your executing like finding pipes and redirects
            if "|" in cmd:
                print("Pipes not implemented yet.")

            if ">" in cmd:
                print("Redirects not implemented yet.")

            if "<" in cmd:
                print("Redirects not implemented yet.")

            
            # write out the command to the history file
            # so you can access it later with the up/down arrows
            
            # Get the absolute path of the folder where the script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Build the full path to history.txt in the same folder
            history_file = os.path.join(script_dir, "history.txt")
            
            with open(history_file, "a") as file:
                file.write(cmd + "\n")
            

            cmd = ""  # reset command to nothing (since we just executed it)
            
            
            print_cmd(cmd)  # now print empty cmd prompt
            
        # Any other character that is not handled above
        else:
            # Concatenate the typed character at the cursor position
            cmd = cmd[:cursor_pos] + char + cmd[cursor_pos:]
            
            # move cursor position to the right
            cursor_pos += 1
            
            # add typed character to our "cmd"
            print_cmd(cmd, cursor_pos)
            
            
            #