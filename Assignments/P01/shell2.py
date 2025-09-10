#!/usr/bin/env python
"""
This file is about using getch to capture input and handle certain keys 
when the are pushed. The 'command_helper.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.

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
#from rich import print

##################################################################################
##################################################################################

getch = Getch()  # create instance of our getch class

prompt = "$"  # set default prompt


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
    
    output = {"output" : None, "error" : None}
    
    # Storing cwd
    cwd = os.getcwd()
    
    # Storing it into output dictionary and returning
    output["output"] = cwd 
    return os.getcwd()


def cd(parts):
    """
    Change to the home directory.
    This function changes the current working directory to the user's home directory.
    Parameters:
        None
    Returns:
        None
    """
    
    '''
    input: dict({"input" : None, "cmd" : None, "params" : [], "flags" : None, "error" : None})
    output dict: {"output" : string, "error" : string}
    '''
    
    # These are lists
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    # Dictionary to return
    output = {"output" : None, "error" : None}
    
    
    if input:
        output["error"] = "Error. Command should not have an input."
        return output
    
    if flags:
        output["error"] = "Error. Command doesn't take flags."
        return output
        
        
    # Changing output dictionary so it can be checked
        
    # Convert params list to string
    str_params = " ".join(params)
    
    # Remove single quotes if they exist
    str_params = str_params.strip("'")
    
        
    # User wants to go to home directory
    if str_params == "":
        homedir = os.path.expanduser("~")
        os.chdir(homedir)
        
        # User wants to go to parent directory
    if str_params == "..":
        os.chdir("..")
            
    # User wants to go to differnt directory
    elif os.path.isdir(str_params):
        os.chdir(str_params)
            
    # Directory is invalid
    elif not os.path.isdir(str_params):
        output["error"] = f"Error. {str_params} is not a directory."
        
    # Returning output dictionary
    return output
            
    
def ls(parts):
    """
    List non-hidden files and directories in the current directory.
    This function lists all files and directories in the current working directory,
    excluding hidden files (those starting with a dot).
    Parameters:
        None
    Returns:
        None
    """
    
    
    '''
    input: dict({"input" : None, "cmd" : None, "params" : [], "flags" : None, "error" : None})
    output dict: {"output" : string, "error" : string}
    '''
    
    # directory to store output information
    output = {"output" : None, "error" : None}
    
    
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)    
    
    # Used to store directory from params
    ls_directory = ""
    
    if input:
        pass
        
    # If user wants to ls a certain directory, grab the directory name if it's a directory
    if len(params) == 1:
        
        # Getting directory info from param given
        
        # Convert params list to string
        str_params = " ".join(params)
    
        # Remove single quotes if they exist
        str_params = str_params.strip("'")
        
        # Determining which directory to display info from
        if params == "..":
            ls_directory = params
            
        elif os.path.isdir(str_params):
            ls_directory = str_params
            
        elif not os.path.isdir(str_params):
            output["error"] = f"Error. {str_params} is not a directory."
            return output
        
        
    # return error if there are more than 1 parameters
    elif len(params) > 1:
        output["error"] = "ls has too many parameters"
        return output
        
    # User wants to print list from current directory
    if not flags:
        # list to store items
        items = []
            
        for item in get_directory_items(ls_directory):
            # Get full path to apply correct coloring
            full_path = os.path.join(ls_directory or os.getcwd(), item)
            items.append(color_filename(item, full_path))
            
        # Returning sorted list of items
        items.sort()
            
        # Convert to string
        result = " ".join(items)
        output["output"] = result
        return output
    
    # Executing ls that has flags
    if flags:
        # Storing the argument
        option = flags
    
        # List that stores directory contents
        directory_list     = get_directory_items(ls_directory)
        all_directory_list = get_directory_items(ls_directory, include_hidden = True)
        
        # Using -h alone prints the same as no args
        if option == "h": 
            
            # list to store items
            items = []
            
            for item in directory_list:
                # Get full path to apply correct coloring
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                items.append(color_filename(item, full_path))
            
            # Returning sorted list of items
            items.sort()
            
            # Convert to string
            result = " ".join(items)
            output["output"] = result
            return output
                
                
        # Using -a alone or with -h prints all files including hidden
        elif option in ("a","ah", "ha"):
            
            # list to store directory items
            items = []
            
            # Getting items in directory including hidden and coloring
            # depending on item type
            for item in all_directory_list:
                
                # Get full path to apply correct coloring
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                items.append(color_filename(item, full_path))
            
            # Returning sorted list of items
            items.sort()
            
            # Convert to string
            result = " ".join(items)
            output["output"] = result
            return output
            
        # Using -l alone
        elif option == "l":
            
            items = []
            total_size = 0
            
            # Getting block size
            for item in directory_list:
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                file_info = os.stat(full_path)
                total_size += file_info.st_blocks
            
            # Printing size of directory
            print("total", total_size // 2)
            
            # Print details for each file
            for item in directory_list:
                    
                # Getting info about the item and adding it to list
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                items.append(format_long_listing(full_path))
                    
            # Return items sorted by filename
            items = sorted(items, key=lambda x: x[-1].lower())
            
            format_list = []
            for item in items:
                line = f"{item[0]:<10} {item[1]:<3}{item[2]:<8}{item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}"
                format_list.append(line)
                
            # Convert to string and return
            result = "\n".join(format_list)
            output["output"] = result
            return output
        
            
        # Using -al or -la prints all files in long format
        elif option in ("al", "la"):
                
            total_size = 0
            items = []
            
            # Calculate total size of all files in directory
            for item in all_directory_list:
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                file_info = os.stat(full_path)
                total_size += file_info.st_blocks
            
            print("total", total_size // 2)
            
            # Print details for each file
            for item in all_directory_list:
                    
                # Getting info about the item and adding it to list
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                items.append(format_long_listing(full_path))
                    
            # Sort items by filename
            items = sorted(items, key=lambda x: x[-1].lower())
            
            # formatting list before converting to string
            format_list = []
            for item in items:
                line = f"{item[0]:<10} {item[1]:<3}{item[2]:<8}{item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}"
                format_list.append(line)
            
            # Converting to string and returning
            result = "\n".join(format_list)
            output["output"] = result
            return output
            
        # Using -lh or -hl prints files in long format with human readable sizes
        elif option in ("lh", "hl"):
            
            total_size = 0
            items = []
            
            # Calculate total size of all non-hidden files in directory
            for item in directory_list:
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                file_info = os.stat(full_path)
                total_size += file_info.st_blocks
            
            # st_blocks * 512 = byte
            print("total", human_readable(total_size * 512))
            
            # Print details for each file
            for item in directory_list:
                    
                # Getting item info and adding to list
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                items.append(format_long_listing(full_path, human = True))
                    
            # Returning items sorted by filename
            items = sorted(items, key=lambda x: x[-1].lower())
            
            # formatting list before converting to string
            format_list = []
            for item in items:
                line = f"{item[0]:<10} {item[1]:<3}{item[2]:<8}{item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}"
                format_list.append(line)
            
            # Converting to string and returning
            result = "\n".join(format_list)
            output["output"] = result
            return output
            
        # Using -alh or any combo of those three prints all files in long format with human readable sizes
        elif option in ("alh", "ahl", "lah", "lha", "hal", "hla"):
            
            total_size = 0
            items = []
            
            # Calculate total size of all files in directory
            for item in all_directory_list:
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                file_info = os.stat(full_path)
                total_size += file_info.st_blocks
            
            # st_blocks * 512 = byte
            print("total", human_readable(total_size * 512))
            
            # Print details for each file
            for item in all_directory_list:
                    
                # Getting item info and adding to list
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                items.append(format_long_listing(full_path, human = True))
                    
            # Returning items sorted by filename
            items = sorted(items, key=lambda x: x[-1].lower())
            
            # formatting list before converting to string
            format_list = []
            for item in items:
                line = f"{item[0]:<10} {item[1]:<3}{item[2]:<8}{item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}"
                format_list.append(line)
            
            # Converting to string and returning
            result = "\n".join(format_list)
            output["output"] = result
            return output
            
        # Invalid option
        else:
            output["error"] = "ls: invalid option. Try 'ls --help for more info."
            return output
        
    output["error"] = "Error"
    return output


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
def format_long_listing(full_path, human = False):
    '''
    Returns detailed metadata for a file in "long listing" format.
    
    Parameters:
        item (str): The filename.
        human (bool): If True, convert file size to human-readable format.
    
    Returns:
        list: [permissions, links, owner, group, size, mod_time, colored_name]
    '''
    
    # Getting full path of the item and info about the item
    file_info = os.stat(full_path)

    # Retreiving info about item
    permissions = stat.filemode(file_info.st_mode)
    links       = file_info.st_nlink
    owner       = pwd.getpwuid(file_info.st_uid).pw_name
    group       = grp.getgrgid(file_info.st_gid).gr_name
    size        = human_readable(file_info.st_size) if human else file_info.st_size
    mod_time    = time.strftime("%b %d %H:%M", time.localtime(file_info.st_mtime))
    
    # coloring item name depending on type
    name        = color_filename(os.path.basename(full_path), full_path)

    # Returning all item information
    return [permissions, links, owner, group, size, mod_time, name]
    #return f"{permissions} {links} {owner} {group} {size} {mod_time} {name}"


# Helper function for ls_with_args
def get_directory_items(directory = None, include_hidden = False):
    '''
    Returns a list of items in the current directory.
    
    Parameters:
        include_hidden (bool): If True, include hidden files along with "." and "..".
    
    Returns:
        list: Filenames in the directory.
    '''
    
    # Storing items from directory into items list
    if directory:
        items = os.listdir(directory)
    
    if not directory:
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
       
       
def write_to_history(cmd):
    '''
    # write out the command to the history file
    # so you can access it later with the up/down arrows
    '''
          
    # Get the absolute path of the folder where the script is located
    # Since this script and the history file are in the same directory:
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path to history.txt inside your repo
    history_file = os.path.join(script_dir, "history.txt")

    # Append command to the file
    with open(history_file, "a") as file:
        file.write(cmd + "\n")
       
    
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


def mkdir(parts):
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



# Test function
def ls_(parts):
    '''
    input: dict({"input" : None, "cmd" : None, "params" : [], "flags" : None, "error" : None})
    output dict: {"output" : string, "error" : string}
    '''
    
    
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    if input:
        pass
        
    if len(params) > 0:
        
        return {"output": None, "error" : "Directionary doesn't exist"}
        
    if flags:
        if '-a' in flags:
            pass
        if '-h' in flags:
            pass
        if '-l' in flags:
            pass
        
    if params:
        
        
        output = "something"
        
    return {"output" : output}


def parse_cmd(cmd_input):
    
    command_list = []
    
    cmds = cmd_input.split("|")
    
    for cmd in cmds:
        
        # Need to have a check while procession that if error has error in it, stop processing.
        
        d = {"input" : None, "cmd" : None, "params" : [], "flags" : None, "error" : None}
        subparts = cmd.strip().split()
        d["cmd"] = subparts[0]
        
        
        
        for item in subparts[1:]:
            
            if "-" in item:
                d["flags"] = item[1:]
            else:
                d["params"].append(item)
                
        print("parameters list:", d["params"])
        
        command_list.append(d)
        
    return command_list
                
        


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
            
            # Printing blank line to info isn't overwritten
            print()

            # Writing command to history file
            write_to_history(cmd)
                
            # If there is a command to execute
            if(cmd):
                
                # Part command and returning list of dictionaries
                command_list = parse_cmd(cmd)
                result = {"output" : None, "error" : None}
                
                
                # Here we need to save the command to the history file.
            
                while len(command_list) != 0:
            
                    # Pop first command off of the command list
                    command = command_list.pop(0)
                    
                    # Kill execution if error
                    if result["error"]:
                        break

                        
                    if command.get("cmd") == "cd":
                        result = cd(command)
                    elif command.get("cmd") == "ls":
                        result = ls(command)

                            
                            
                            
                # Printing result to screen
                if result["error"]:
                    print(result["error"])
                elif result["output"]:
                    print(result["output"])



            cmd = ""
            cursor_pos = 0
            
            print_cmd(cmd)  # now print empty cmd prompt on next line
        else:
            # Concatenate the typed character at the cursor position
            cmd = cmd[:cursor_pos] + char + cmd[cursor_pos:]
            
            # move cursor position to the right
            cursor_pos += 1
            
            # add typed character to our "cmd"
            print_cmd(cmd, cursor_pos)