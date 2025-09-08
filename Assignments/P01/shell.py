#!/usr/bin/env python




"""
Imports used in this project:

OS and system interaction:
    - os       : Functions for interacting with the operating system (paths, directory listing, permissions, etc.)
    - sys      : System-specific parameters and functions (e.g., arguments, exit)

User and group information:
    - pwd      : Retrieve user account information (file owner in long listings)
    - grp      : Retrieve group account information (file group in long listings)

File status and permissions:
    - stat     : Interpret file status results (file mode, permissions, file type)

Input handling:
    - getch.Getch : Capture single keypresses without needing Enter (used for shell input handling)

Terminal output formatting:
    - colorama (init, Fore, Style) : Cross-platform colored terminal output (e.g., directories in blue, executables in green)

Time-related functionality:
    - time     : Time functions (formatting file modification times)
    - sleep    : Pause execution for a given number of seconds (optional delays)

Other utilities:
    - re       : Regular expression matching operations (parsing and validating input/commands)
"""
import os 
import sys 
import pwd
import grp
import stat
from getch import Getch
from colorama import init, Fore, Style
import time
from time import sleep
import re



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
    print(f"{Fore.GREEN}Designed and implemented by Tim Haxton, Harika Vemulapalli, and Cooper Wolf.")
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


# Helper function for ls_with_args
def color_filename(item, full_path):
    '''
    Returns a colored string for a filename based on its type.
    
    - Directories → Blue
    - Executable files → Green
    - Other files → Default color
    '''
    
    # Coloring the directories blue
    if os.path.isdir(full_path):
        return Fore.BLUE + item + Style.RESET_ALL
    
    # Coloring the executables green
    elif os.access(full_path, os.X_OK):
        return Fore.GREEN + item + Style.RESET_ALL
    
    # Leaving all other itms default color
    return item
    

# Helper functin for ls_with_args
def format_long_listing(item, human = False):
    '''
    Returns detailed metadata for a file in "long listing" format.
    
    Parameters:
        item (str): The filename.
        human (bool): If True, convert file size to human-readable format.
    
    Returns:
        list: [permissions, links, owner, group, size, mod_time, colored_name]
    '''
    
    # Getting full path of the item and info about the item
    full_path = os.path.join(os.getcwd(), item)
    file_info = os.stat(full_path)

    # Retreiving info about item
    permissions = stat.filemode(file_info.st_mode)
    links       = file_info.st_nlink
    owner       = pwd.getpwuid(file_info.st_uid).pw_name
    group       = grp.getgrgid(file_info.st_gid).gr_name
    size        = human_readable(file_info.st_size) if human else file_info.st_size
    mod_time    = time.strftime("%b %d %H:%M", time.localtime(file_info.st_mtime))
    
    # coloring item name depending on type
    name        = color_filename(item, full_path)

    # Returning all item information
    return [permissions, links, owner, group, size, mod_time, name]


# Helper function for ls_with_args
def get_directory_items(include_hidden = False):
    '''
    Returns a list of items in the current directory.
    
    Parameters:
        include_hidden (bool): If True, include hidden files along with "." and "..".
    
    Returns:
        list: Filenames in the directory.
    '''
    
    # Storing items from directory into items list
    items = os.listdir()
    non_hidden_items = []
    
    # If wanting all items return items + . and ..
    if include_hidden:
        return ['.', '..'] + items
    
    # Return only non hidden items
    else:
        for item in items:
            if not item.startswith('.'):
                non_hidden_items.append(item)
                
        return non_hidden_items


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
    
    # Storing the argument
    option = args[0]
    
    # List that stores directory contents
    directory_list     = get_directory_items()
    all_directory_list = get_directory_items(include_hidden = True)
    
    # Using -h alone prints the same as no args
    if option == "-h":       
        return ls()
            
    # Using -a alone or with -h prints all files including hidden
    elif option in ("-a","-ah", "-ha"):
        
        # list to store directory items
        items = []
        
        # Getting items in directory including hidden and coloring
        # depending on item type
        for item in all_directory_list:
            
            # Get full path to apply correct coloring
            full_path = os.path.join(os.getcwd(), item)
            items.append(color_filename(item, full_path))
        
        # Returning sorted list of items
        items.sort()
        return items
        
    # Using -l alone
    elif option == "-l":
        
        items = []
        total_size = 0
        
        # Getting block size
        for item in directory_list:
            file_info = os.stat(item)
            total_size += file_info.st_blocks
        
        # Printing size of directory
        print("total", total_size // 2)
        
        # Print details for each file
        for item in directory_list:
                
            # Getting info about the item and adding it to list
            items.append(format_long_listing(item))
                
        # Return items sorted by filename
        items = sorted(items, key=lambda x: x[-1].lower())
        return items
         
    # Using -al or -la prints all files in long format
    elif option in ("-al", "-la"):
               
        total_size = 0
        items = []
        
        # Calculate total size of all files in directory
        for item in all_directory_list:
            file_info = os.stat(item)
            total_size += file_info.st_blocks
        
        print("total", total_size // 2)
        
        # Print details for each file
        for item in all_directory_list:
                
            # Getting info about the item and adding it to list
            items.append(format_long_listing(item))
                
        # Sort items by filename
        items = sorted(items, key=lambda x: x[-1].lower())
        return items
        
    # Using -lh or -hl prints files in long format with human readable sizes
    elif option in ("-lh", "-hl"):
        
        total_size = 0
        items = []
        
        # Calculate total size of all non-hidden files in directory
        for item in directory_list:
            file_info = os.stat(item)
            total_size += file_info.st_blocks
        
        # st_blocks * 512 = byte
        print("total", human_readable(total_size * 512))
        
        # Print details for each file
        for item in directory_list:
                
            # Getting item info and adding to list
            items.append(format_long_listing(item, human = True))
                
        # Returning items sorted by filename
        items = sorted(items, key=lambda x: x[-1].lower())
        return items
        
    # Using -alh or any combo of those three prints all files in long format with human readable sizes
    elif option in ("-alh", "-ahl", "-lah", "-lha", "-hal", "-hla"):
        
        total_size = 0
        items = []
        
        # Calculate total size of all files in directory
        for item in all_directory_list:
            file_info = os.stat(item)
            total_size += file_info.st_blocks
        
        # st_blocks * 512 = byte
        print("total", human_readable(total_size * 512))
        
        # Print details for each file
        for item in all_directory_list:
                
            # Getting item info and adding to list
            items.append(format_long_listing(item, human = True))
                
        # Returning items sorted by filename
        items = sorted(items, key=lambda x: x[-1].lower())
        return items
        
    # Invalid option
    else:
        print("ls: invalid option.")
        print("Try 'ls --help' for more information.")
    
        
def history():
    """
    Display the command history from the history.txt file.

    This function reads the history.txt file and prints each command
    stored in it. If the file does not exist, it informs the user.

    Parameters:
        None
    Returns:
        None
    """
    
    # Get the absolute path of the folder where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path to history.txt inside your repo
    history_file = os.path.join(script_dir, "history.txt")

    history_list = []
    command_number = 1

    # Check if history file exists
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            commands = file.readlines()
            for command in commands:
                history_list.append(f"{command_number} {command.strip()}")
                command_number += 1
        
        # Appending the history command that was just executed
        history_list.append(f"{command_number} history")
        
        # Returning list
        return history_list       
        
    # If history_file does not exist, return None
    else:
        return None
    
    
def get_history_rev():
    """
    Opens history text file and returns the contents.

    This function retrieves the previous command from the history file
    and returns it. If there is no previous command, it returns None.

    Parameters:
        None
    Returns:
        List of all commands in history file.
    """
    
    # Get the absolute path of the folder where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path to history.txt inside your repo
    history_file = os.path.join(script_dir, "history.txt")

    # Check if history file exists
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            h_cmds = file.readlines()
            
            # Remove the last value if its empty
            if h_cmds and h_cmds[-1].strip() == "":
                h_cmds.pop()
            
            # Removing '\n' at the end of each command
            h_cmds = [item.strip() for item in h_cmds]
            
            # Reversing list
            h_cmds.reverse()
            
            # Return list of all commands in history in reverse order
            return h_cmds
            
    else:
        # History file doesn't exist
        return None
    
    
# This functions works as the !x command
def cmd_from_history(index):
    '''
    Functions handles the !x command by getting the index value from the command
    and retrieves the history commands then return the at index given
    '''
    
    index = int(index)
    index -= 1
    h_cmds = get_history_rev() or []
    
    # Reverse list so
    if h_cmds:
        h_cmds.reverse()
    
    # Geting history commands
    if 0 <= index < len(h_cmds):
    
        # Returning cmd at given index
        return h_cmds[index].strip()
    else:
        return None
       
    
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


def visible_length(s):
    '''Helper function for print_cmd. This is needed to bring the terminal cursor to the correct
    position. Previously. it was offset by the length of ({Fore.CYAN}{Style.RESET_ALL}). So this
    funciton removes that from the prompt so the cursor can be in the correct position.
    '''
    
    # Step by step:
    # \x1b         -> The escape character signaling the start of an ANSI sequence
    # \[           -> Matches the literal '[' that follows the escape character
    # [0-9;]*      -> Matches any digits or semicolons (e.g., 36, 1;32) zero or more times
    # m            -> Matches the literal 'm' at the end of the ANSI code
    # Together: \x1b\[[0-9;]*m matches things like:
    #    \x1b[36m    -> set cyan text
    #    \x1b[0m     -> reset text style/color
    #    \x1b[1;32m  -> bold green text

    # re.compile() -> Compiles this regex pattern for reuse
    # ansi_escape.sub('', s) -> Removes all ANSI sequences from the string
    # len(...) -> Counts only the visible characters, ignoring color codes
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return len(ansi_escape.sub('', s))


def print_cmd(cmd, cursor_pos=0):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
#    
#    
#    # Setting width to terminal size
#    width = shutil.get_terminal_size((80, 20)).columns  
#
#    # Clear line with spaces equal to width
#    padding = " " * width
#    sys.stdout.write("\r" + padding + "\r")
#    
#    # Update prompt with current working directory
#    prompt = f"{Fore.CYAN}{os.getcwd()}{Style.RESET_ALL}$ "
#
#    # Print prompt
#    sys.stdout.write(f"{prompt}{cmd}")
#    
#    # Move cursor to correct position
#    sys.stdout.write("\r" + prompt + cmd[:cursor_pos])
#    sys.stdout.flush()
#
#

    # Update prompt with current working directory
    prompt = f"{Fore.CYAN}{os.getcwd()}{Style.RESET_ALL}$ "
    
    
    # Print fix from ChatGPT
    ###################################################################################
    
    # Move cursor to start, print prompt + command
    sys.stdout.write("\r")           # go to start of line
    sys.stdout.write(f"{prompt}{cmd}")
    sys.stdout.write("\033[K")       # clear from cursor to end of line

    # Move cursor to correct position
    sys.stdout.write("\r")                               # go to start
    sys.stdout.write(f"\033[{visible_length(prompt) + cursor_pos}C")  # move cursor to position
    
    ##################################################################################
    

    sys.stdout.flush()



####### BEGINNING OF MAIN PROGRAM ##############
if __name__ == "__main__":
    
    # Allows for colored text in terminal and resets color after each print
    init(autoreset=True)

    # Print welcome message
    WelcomeMessage()
    
    cmd = ""  # empty cmd variable
    
    # For handling left/right arrow keys
    cursor_pos = 0

    # For handling up/down arrow keys
    history_index = -1

    print_cmd(cmd)  # print to terminal

    while True:  # loop forever

        # read a single character, don't print
        char = getch()
        
        # Exit shell on ctrl-c command
        if char == "\x03":
            exit_shell()

        # If back space pressed, remove the character to the left of the cursor
        if char == "\x7f":
            if cursor_pos > 0:
                cmd = cmd[:cursor_pos-1] + cmd[cursor_pos:]
                cursor_pos -= 1
            print_cmd(cmd, cursor_pos)

        elif char in "\x1b":  # arrow key pressed
            null = getch()  # waste a character
            direction = getch()  # grab the direction
            
            # Get updated history if avaible
            h_cmd = get_history_rev() or []

            if direction in "A":  # up arrow pressed
                
                # Get list of history commands
                if h_cmd and history_index < len(h_cmd) - 1:
                    
                    # Get the previous command from history depending on
                    # history_index and increment index
                    history_index += 1
                    cmd = h_cmd[history_index]
                    
                    
                # If at the end of history, stay there
                else:
                    # already at the oldest command
                    # so set cmd to end of h_cmd list
                    cmd = h_cmd[-1]
                    
                cursor_pos = len(cmd)
                print_cmd(cmd, cursor_pos)

            if direction in "B":  # down arrow pressed
                
                # get the NEXT command from history (if there is one)
                if h_cmd and history_index > 0:
                    
                    # Get the previous command from history depending on
                    # history_index and decrement index
                    history_index -= 1
                    cmd = h_cmd[history_index]

                    
                # At the newest, go to blank like
                else:
                    
                    # Getting a blank line
                    history_index = -1
                    cmd = ""
                    
                cursor_pos = len(cmd)
                print_cmd(cmd, cursor_pos)

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
            
            # Exit shell on 'exit' command
            if cmd == "exit":
                exit_shell()

            # Executing !x command
            if len(cmd.split()) == 1 and cmd.startswith("!") and cmd[1:].isnumeric() and (".") not in cmd:
                    
                # Getting the given command from history file
                h_cmd = cmd_from_history(cmd[1:])
                    
                # If found, print and set cmd to command
                if h_cmd:
                        
                    # Set command from history to command
                    cmd = h_cmd
                    
                    # set cursor_pos to zero
                    cursor_pos = 0
                    print(cmd)
                    
                # Command wasn't found    
                else:
                    print(f"Line {cmd[1:]} does not exist.")
            
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
                    
                elif cmd_ == "history":
                    history_list = history()
                    
                    if history_list:
                        for item in history_list:
                            print(item)
                            
                    else:
                        print("ERROR: History File could not be found.")
    
            
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
            # Since this script and the history file are in the same directory:
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Build the full path to history.txt inside your repo
            history_file = os.path.join(script_dir, "history.txt")

            # Append command to the file
            with open(history_file, "a") as file:
                file.write(cmd + "\n")
            

            cmd = ""  # reset command to nothing (since we just executed it)
            cursor_pos = 0
            
            print_cmd(cmd)  # now print empty cmd prompt
            
        # Any other character that is not handled above
        else:
            # Concatenate the typed character at the cursor position
            cmd = cmd[:cursor_pos] + char + cmd[cursor_pos:]
            
            # move cursor position to the right
            cursor_pos += 1
            
            # add typed character to our "cmd"
            print_cmd(cmd, cursor_pos)
            
