#!/usr/bin/env python
"""
This py file is the development environment for the shell program.
I do all my dev and testing on this script then push it to 
production script when testing is sucessful

"""
import os 
import sys 
import pwd
import grp
import stat
import socket
import getpass
from getch import Getch
from colorama import init, Fore, Style
import time
import subprocess
from time import sleep
import re
import shutil

# Global variable to track current shell color
#CURRENT_COLOR = Style.RESET_ALL

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
    
    output = {"output" : None, "error" : None}
    
    # Storing cwd
    cwd = os.getcwd()
    
    # Storing it into output dictionary and returning
    output["output"] = cwd 
    return output

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
    if str_params == "" or str_params == "~":
        homedir = os.path.expanduser("~")
        os.chdir(homedir)
        return output
        
        # User wants to go to parent directory
    if str_params == "..":
        os.chdir("..")
            
    # User wants to go to differnt directory
    elif os.path.isdir(str_params):
        os.chdir(str_params)
            
    # If path doesn't exist and params isn't empty
    elif not os.path.isdir(str_params) and str_params != "":
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
        output["error"] = f"{Fore.RED}Error. Ls command should not have input.{Style.RESET_ALL}\nTry 'ls --help for more info."
        return output
        
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
            output["error"] = f"{Fore.RED}Error. {str_params} is not a directory.{Style.RESET_ALL}\nTry 'ls --help for more info."
            return output
        
        
    # return error if there are more than 1 parameters
    elif len(params) > 1:
        output["error"] = f"{Fore.RED}ls has too many parameters{Style.RESET_ALL}. \nTry 'ls --help for more info."
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
        if option == "-h": 
            
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
        elif option in ("-a","-ah", "-ha"):
            
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
        elif option == "-l":
            
            items = []
            total_size = 0
            
            # Getting block size
            for item in directory_list:
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                file_info = os.stat(full_path)
                total_size += file_info.st_blocks
            
            # Get size of directory 
            total_size = total_size // 2
            
            # Print details for each file
            for item in directory_list:
                    
                # Getting info about the item and adding it to list
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                items.append(format_long_listing(full_path))
                    
            # Return items sorted by filename
            items = sorted(items, key=lambda x: x[-1].lower())
            
            format_list = []
            for item in items:
                line = f"{item[0]:<10} {item[1]:<3}{item[2]:<8} {item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}"
                format_list.append(line)
                
            # Convert to string and return
            result = f"Total size: {total_size}\n" + "\n".join(format_list)
            output["output"] = result
            return output
        
        # Using -al or -la prints all files in long format
        elif option in ("-al", "-la"):
                
            total_size = 0
            items = []
            
            # Calculate total size of all files in directory
            for item in all_directory_list:
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                file_info = os.stat(full_path)
                total_size += file_info.st_blocks
            
            total_size = total_size // 2
            
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
                line = f"{item[0]:<10} {item[1]:<3}{item[2]:<8} {item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}"
                format_list.append(line)
            
            # Converting to string and returning
            result = f"Total size: {total_size}\n" + "\n".join(format_list)
            output["output"] = result
            return output
            
        # Using -lh or -hl prints files in long format with human readable sizes
        elif option in ("-lh", "-hl"):
            
            total_size = 0
            items = []
            
            # Calculate total size of all non-hidden files in directory
            for item in directory_list:
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                file_info = os.stat(full_path)
                total_size += file_info.st_blocks
            
            # st_blocks * 512 = byte
            total_size = human_readable(total_size * 512)
            
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
                line = f"{item[0]:<10} {item[1]:<3}{item[2]:<8} {item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}"
                format_list.append(line)
            
            # Convert to string and return
            result = f"Total size: {total_size}\n" + "\n".join(format_list)
            output["output"] = result
            return output
            
        # Using -alh or any combo of those three prints all files in long format with human readable sizes
        elif option in ( "-lah", "-alh", "-ahl", "-lha", "-hal", "-hla"):
            
            total_size = 0
            items = []
            
            # Calculate total size of all files in directory
            for item in all_directory_list:
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                file_info = os.stat(full_path)
                total_size += file_info.st_blocks
            
            # st_blocks * 512 = byte
            total_size = human_readable(total_size * 512)
            
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
                line = f"{item[0]:<10} {item[1]:<3}{item[2]:<8} {item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}"
                format_list.append(line)
            
            # Convert to string and return
            result = f"Total size: {total_size}\n" + "\n".join(format_list)
            output["output"] = result
            return output
           
        # Using -merica prints files in red white and blue 
        elif option == "-merica":

            total_size = 0
            items = []
            
            # Calculate total size of all files in directory
            for item in all_directory_list:
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                file_info = os.stat(full_path)
                total_size += file_info.st_blocks
            
            # st_blocks * 512 = byte
            total_size = human_readable(total_size * 512)
            
            # Print details for each file
            for item in all_directory_list:
                    
                # Getting item info and adding to list
                full_path = os.path.join(ls_directory or os.getcwd(), item)
                items.append(format_long_listing(full_path, human = True))
                    
            # Returning items sorted by filename
            items = sorted(items, key=lambda x: x[-1].lower())
            
            # Color the lines red white and blue | Got this code from Claude
            colors = [Fore.RED, Fore.WHITE, Fore.BLUE]
            format_list = []
            for i, item in enumerate(items):
                line = f"{item[0]:<10} {item[1]:<3}{item[2]:<8} {item[3]:<8}{item[4]:>8} {item[5]:<12} {item[6]}"
        
                # Apply color cycling through red, white, blue for each line
                color = colors[i % 3]
                colored_line = color + line + Style.RESET_ALL
                format_list.append(colored_line)
            
            # Convert to string and return
            result = f"Total size: {total_size}\n" + "\n".join(format_list)
            output["output"] = result
            return output
                    
        # Invalid option
        else:
            output["error"] = f"{Fore.RED}ls: invalid flag: {flags}.{Style.RESET_ALL} \nTry 'ls --help for more info."
            return output
        
    output["error"] = "Error"
    return output

def wc(parts):
    '''
    input: dict({"input" : None, "cmd" : None, "params" : [], "flags" : None, "error" : None})
    output dict: {"output" : string, "error" : string}
    '''
    
    # Parsing parts dictionary
    input  = parts.get("input", None)
    flags  = parts.get("flags", None)
    params = parts.get("params", None)
    
    # Dictionary to store output
    output = {"output" : None, "error" : None}
    
    # If multiple parameters
    if len(params) > 1:
        output["error"] = f"{Fore.RED}Error: 'wc' can only take one parameter.{Style.RESET_ALL} \nRun 'wc --help' for more info."
        return output
    
    # Variables to store count
    line_count = 0
    word_count = 0
    char_count = 0
    
    # Convert params to string
    if params:
        params = "".join(params)
        params = params.strip("'")
        
    # Convert input to string
    if input:
        input = "".join(input)
        input = input.strip("'")
        
    # Filtering out bad commands
    if not params and not input:
        output["error"] = f"{Fore.RED}Error: 'wc' needs either an input file or parameter file to process.{Style.RESET_ALL} \nRun 'wc --help' for more info."
        return output
    if params and input:
        output["error"] = f"{Fore.RED}Error: 'wc' needs either an input file or parameter file to process.{Style.RESET_ALL} \nRun 'wc --help' for more info."
        return output
    if flags and flags not in ["-w", "-l", "-wl", "-lw"]:
        output["error"] = f"{Fore.RED}Error: {flags} is not a viable flag.{Style.RESET_ALL} Run 'wc --help' for flag options"
        return output
    
    # Checking if input or params in a file.
    item = input or params
    
    # Determine if item is a file
    if os.path.isfile(item):
        
        # Seeing if file is an absolute path
        if os.path.isabs(item):
            
            # Getting the absolute path from argument
            path = item

        # if relative path, join with current working directory
        elif not os.path.isabs(item):
            
            # Building absolute path
            new_dir = item
            cwd     = os.getcwd()
            path    = os.path.join(cwd, new_dir)
            
        # If user ran a pipe and wc section only contains wc
        # Example: ls | wc -w or wc -l fruit.txt
        if flags and path:
            
            # Get countswhat
            with open(path, 'r') as file:
                for line in file:
                    if "l" in flags:
                        line_count += 1
                    if "w" in flags:
                        words = line.split()
                        word_count += len(words)
            
            # Getting correct data to output | Code from ChatGPT           
            output_values = []
            output_values.append(str(line_count) if "l" in flags else None)
            output_values.append(str(word_count) if "w" in flags else None)
                            
            # Store results to output and return | Code from ChatGPT
            output["output"] = " ".join(filter(None, output_values))
            return output
            
        # If user ran wc with flags
        # Example wc fruit.txt or ls | wc
        if not flags and path:
            
            # Get counts
            with open(path, 'r') as file:
                for line in file:
                    line_count += 1
                    words = line.split()
                    word_count += len(words)
                    char_count += len(line)
                            
            # Store results to output and return
            output["output"] = f"{line_count} {word_count} {char_count} {input or params}"
            return output            
            
    # Determine if item is a string
    elif isinstance(item, str) and input and not params:
        
        
        # Split string in lines first 
        lines = item.splitlines()
        
        # Removes characters used to color text
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        item = ansi_escape.sub('', item)
        
        # Split string in lines first
        lines = item.splitlines()
    
        # If user ran a pipe and wc section only contains wc
        # Example: ls | wc -w or wc -l fruit.txt
        if flags and item:
            
            # Getting line count
            if "l" in flags:
                
                # If item has multiple lines get length
                if len(lines) > 1:
                    line_count = len(lines)
                    
                # Else its just one line
                else:
                    line_count = 1
                    
            # Getting word count
            if "w" in flags:
                
                # Count words in each line
                if len(lines) > 1:
                    for line in lines:
                        for words in line.split():
                            word_count += len(words)
                            
                # Only one line      
                else:
                    word_count = len(lines)
                            
            # Getting correct data to output | Code from ChatGPT           
            output_values = []
            output_values.append(str(line_count) if "l" in flags else None)
            output_values.append(str(word_count) if "w" in flags else None)
                            
            # Store results to output and return | Code from ChatGPT
            output["output"] = " ".join(filter(None, output_values))
            return output
            
        # If user ran wc with flags
        # Example wc fruit.txt or ls | wc
        if not flags and item:
            
            # If item has multiple lines cound them
            if len(lines) > 1:
                line_count = len(lines)
                
            # If item has one line only add one
            else:
                line_count = 1
                
            # Count words in each line
            if len(lines) > 1:
                for line in lines:
                    for words in line.split():
                        word_count += len(words)
                        
            else:
                word_count = len(lines)
            
            # Count all characters in string
            char_count = len(item)
                            
            # Store results to output and return
            output["output"] = f"{line_count} {word_count} {char_count}"
            return output
    
    # item was not a string or file
    else:
        output["error"] = f"{Fore.RED}Error: {item}: No such file or directory.{Style.RESET_ALL}\nRun 'wc --help' for more info."
        return output

def cat(file):
    '''
    Usage: cat [FILE]...

    Example:
        cat f - g   Output f's contents, then standard input, then g's contents.
        cat         Copy standard input to standard output.
    '''
    output = {"output": None, "error": None}

     #if no file provided, read from stdin once
    if not file:
        output["output"] = sys.stdin.read()
        return output
    for f in file:
        if f == '-':
            #read from standard input here
            output["output"] = sys.stdin.read()
        else:
            try:
                with open(f,'r') as file_handle:
                    output["output"] = file_handle.read()
            except FileNotFoundError:
                output["error"] = f"cat: {f}: No such file or directory\n"
            except Exception as e:
                output["error"] = f"cat: {f}: {str(e)}\n"
    return output              

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
    
    # These are lists
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    # Dictionary to return
    output = {"output" : None, "error" : None}
    
    # Make sure user only ran mkdir [directory]
    if not input and not flags:
        # Convert params list to string
        str_params = " ".join(params)
        
        # Remove single quotes if they exist
        str_params = str_params.strip("'")

        if os.path.isabs(str_params):
            
            # Getting the absolute path from argumen
            path = str_params

        # if relative path, join with current working directory
        elif not os.path.isabs(str_params):
            
            # Getting new directory name, current working directory
            # and joining them to create full path
            new_dir = str_params
            cwd     = os.getcwd()
            path    = os.path.join(cwd, new_dir)
            
        # Creating the directory and handling errors
        try:
            os.mkdir(path)
        except OSError as e:
            output["error"] = f"Error: {e}"
            
            
    # User entered incorrect command format
    else:
        output["error"] = "Error. Mkdir command only takes a directory."
        
        
    return output

def grep(parts):
    '''
    Grep command searches for a given pattern within the given file.
    If no file is given, it will match with what has been received as
    input from previous command (only if piping). You can only have 
    one patter. This command takes no flags 
    '''
    
    # These are lists
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    # Dictionary to return
    output = {"output" : None, "error" : None}
    
    # list to contain matches
    match = []
    
    # Catching bad commands
    if flags:
        output["error"] = f"{Fore.RED}Error: 'grep' doesn't take flags.{Style.RESET_ALL} \nRun 'grep --help' for more info."
        return output

    if not params:
        output["error"] = f"{Fore.RED}Error: 'grep' must have a pattern to match.{Style.RESET_ALL} \nRun 'grep --help' for more info."
        return output
    
    if not input and len(params) < 2:
        output["error"] = f"{Fore.RED}Error: 'grep' is missing a pattern or file.{Style.RESET_ALL} \nRun 'grep --help' for more info."
        return output
    
    if input and len(params) > 2:
        output["error"] = f"{Fore.RED}Error: 'grep' cannot process input and a parameter(s).{Style.RESET_ALL} \nRun 'grep --help' for more info."
        return output
    
    if input and len(params) < 1:
        output["error"] = f"{Fore.RED}Error: 'grep' has input, but was also given a file to process. Must be one or the other.{Style.RESET_ALL} \nRun 'grep --help' for more info."
        return output
    
    if len(params) > 50:
        output["error"] = f"{Fore.RED}Error: Params list too long.{Style.RESET_ALL} \nRun 'grep --help' for more info."
    
    # list to store split params
    files = []
    pattern_parts = []
    
    # Loop through params to clean and append to correct list
    for param in params:
        clean = param.strip("'\"")
        
        # If param is file append to files list | logic From ChatGPT
        if os.path.isfile(param) or os.path.exists(clean):
            files.append(param)
            
        # Else param is part of the pattern
        else:
            pattern_parts.append(param)
            
    pattern = " ".join(pattern_parts)  
        
    # Convert input to string
    if input:
        input = "".join(input)
        input = input.strip("'")
    
    # Store the input or files to process on
    source = input or files
    
    if not source:
        output["error"] = f"{Fore.RED}Error: Could not get the file or string to process.{Style.RESET_ALL} \nRun 'grep --help' for more info."
    
    # if source is a string
    if isinstance(source, str):
        
        # Split the lines of the source and process
        for line in source.splitlines():
            if pattern in line:
                
                # Highlight all matches of the pattern in yellow
                highlighted = re.sub(re.escape(pattern), f"{Fore.YELLOW}{pattern}{Style.RESET_ALL}", line)
                match.append(highlighted)
        
        # Converting to string and returning
        result = "\n".join(match)
        output["output"] = result
        return output
        
    # Determine if item is a file
    for file in source:
        if os.path.isfile(file):
            # Seeing if file is an absolute path
            if os.path.isabs(file):
            
                # Getting the absolute path from argument
                path = file

            # if relative path, join with current working directory
            elif not os.path.isabs(file):
            
                # Building absolute path
                new_dir = file
                cwd     = os.getcwd()
                path    = os.path.join(cwd, new_dir)
                
            # Match patter with contents in file
            if path:
                with open(path, 'r') as file_:
                    for line in file_:
                        if pattern in line:
                            
                            # Highlight the pattern in green (Got from GPT)
                            highlighted = re.sub(re.escape(pattern),f"{Fore.YELLOW}{pattern}{Style.RESET_ALL}", line)
                            
                            # Output info differently depending on if processing one or many files
                            if len(files) > 1:
                                match.append(f"{file}: {highlighted}")
                            else:
                                match.append(f"{highlighted}")                                
                            
            # Error is could not get path
            else:
                output["error"] = f"{Fore.RED}Error: {file} could not be found.{Style.RESET_ALL} \nRun 'grep --help' for more info."
                return output
            
        # Error if one of the files does not exist
        else:
            output["error"] = f"{Fore.RED}Error: {file} is not a file.{Style.RESET_ALL} \nRun 'grep --help' for more info."
            return output
        
    # Converting to string and returning
    result = "".join(match)
    output["output"] = result
    return output
           
def sort(parts):
    '''
    
    '''        
            
    # Getting parsed parts
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    # Dictionary to return
    output = {"output" : None, "error" : None}
    
    # List to store sorted data
    sorted_list = []

    # Filter out bad commands
    if (input and params) or (not input and not params):
        output["error"] = f"{Fore.RED}Error: 'sort' needs either input or params.{Style.RESET_ALL} \nRun 'sort --help' for more info."
        return output
        
    if flags not in ["-r", "-n", None]:
        output["error"] = f"{Fore.RED}Error: Invalid flag: '{flags}'.{Style.RESET_ALL} \nRun 'sort --help' for more info."
        return output
        
    # Storing the input or param into data
    data = input or params
    
    # Converting data from list to string
    data = "".join(data)
    data = data.strip("'")
    
    # Process if data is file
    if os.path.isfile(data):
        
        # Seeing if file is an absolute path
        if os.path.isabs(data):
            
            # Getting the absolute path from argument
            path = data

        # if relative path, join with current working directory
        elif not os.path.isabs(data):
            
            # Building absolute path
            new_dir = data
            cwd     = os.getcwd()
            path    = os.path.join(cwd, new_dir)
                
        # Match patter with contents in file
        if path:
            
            # From Chat
            with open(path, 'r') as file_:
                for line in file_:
                    if line.endswith("\n"):
                        sorted_list.append(line)
                    else:
                        line = line + "\n"
                        sorted_list.append()
                    
            # Sort alphebetically
            if flags in ["-a", None]:
                sorted_list.sort()
            
            # Reverse list
            elif flags == "-r":
                sorted_list.sort(reverse=True)
                
            # Sort numerically
            elif flags == "-n":
                sorted_list.sort(key=int)
                
        # Error if path not found
        else:
            output["error"] = f"{Fore.RED}Error: {data} is not a file.{Style.RESET_ALL} \nRun 'sort --help' for more info."
            return output
                
        # Converting to string and returning
        result = "".join(sorted_list)
        output["output"] = result
        return output
    
    # if source exists and is a string
    elif isinstance(data, str):
        
        # Removes characters used to color text in order to properly sort
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        data = ansi_escape.sub('', data)       
        
        # Split the lines of the string and append to list
        if "\n" in data and len(data) > 1:
            for line in data.splitlines():
                
                # Avoid empty lines
                if line.strip():
                    sorted_list.append(line)
                
        # If data is one line, split by word
        elif "\n" not in data and len(data) > 1:
            for line in data.splitlines():
                for word in line.split():
                    sorted_list.append(word)
                    
        # If data is one character
        else:
            output["error"] = f"{Fore.RED}Error: 'sort' was given nothing to sort.{Style.RESET_ALL} \nRun 'sort --help' for more info."
            return output
                
        # Sort alphebetically or numerically
        if flags in ["-a", None]:
            sorted_list.sort()
            
        # Reverse list
        if flags == "-r":
            sorted_list.sort(reverse=True) 
            
        # Sort numerically
        if flags == "-n":
            sorted_list.sort(key=int)              
        
        # Converting to string and returning
        result = "\n".join(sorted_list)
        output["output"] = result
        return output
    
    else:
        output["error"] = f"{Fore.RED}Error: {data} could not be properly handled.{Style.RESET_ALL} \nRun 'sort --help' for more info."
        return output   

def help(parts):
    '''
    input: dict({"input" : None, "cmd" : None, "params" : [], "flags" : None, "error" : None})
    output dict: {"output" : string, "error" : string}
    '''
    
    input  = parts.get("input", None)
    flags  = parts.get("flags", None)
    params = parts.get("params", None)
    cmd    = parts.get("cmd", None)
    
    output = {"output" : None, "error" : None}
    
    output["output"] = "    ------------------------------"
    
    if not input and not params and flags == "--help":
        if cmd == "cd":
            output["output"] += cd.__doc__
            
        elif cmd == "ls":
            output["output"] += ls.__doc__

        elif cmd == "pwd":
            output["output"] += pwd_.__doc__

        elif cmd == "mkdir":
            output["output"] += mkdir.__doc__
            
        elif cmd == "wc":
            output["output"] += wc.__doc__
            
        elif cmd == "history":
            output["output"] += history.__doc__
            
        elif cmd == "grep":
            output["output"] += grep.__doc__
            
        elif cmd == "sort":
            output["output"] += sort.__doc__
            
        elif cmd == "chmod":
            output["output"] += chmod.__doc__
        
        elif cmd == "help":
            output["output"] += help.__doc__
            
        elif cmd == "date":
            output["output"] += date.__doc__
        
        elif cmd == "clear":
            output["output"] += clear.__doc__
            
        elif cmd == "exit":
            output["output"] += exit_shell.__doc__
            
        elif cmd == "run":
            output["output"] += run.__doc__
        '''
        if cmd == "cp":
            output["output"] += cp.__doc__

        if cmd == "mv":
            output["output"] += mv.__doc__

        if cmd == "rm":
            output["output"] += rm.__doc__

        if cmd == "cat":
            output["output"] += cat.__doc__

        if cmd == "head":
            output["output"] += head.__doc__

        if cmd == "tail":
            output["output"] += tail.__doc__

        if cmd == "more":
            output["output"] += more.__doc__

        if cmd == "less":
            output["output"] += less.__doc__

        '''
        
        output["output"] += "------------------------------"
        return output
    else:
        output["error"] = f"Error, help for command {cmd} could not be found."
        return output

def history(parts):
    """
    Display the command history from the history.txt file.

    This function reads the history.txt file and prints each command
    stored in it. If the file does not exist, it informs the user.

    Parameters:
        None
    Returns:
        None
    """
    
    # These are lists
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    # Dictionary to return
    output = {"output" : None, "error" : None}
    
    # If there exist any input flags and params in the dict, dont execute
    if not input and not flags and not params:
        
        # Get the absolute path of the folder where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the full path to history.txt inside your repo
        history_file = os.path.join(script_dir, "history.txt")

        history_list = []
        command_number = 1

        # Check if history file exists
        if os.path.exists(history_file):
            
            # Opening history file
            with open(history_file, "r") as file:
                
                # Storing contents into commands
                commands = file.readlines()
                
                # Getting each line
                for command in commands:
                    
                    # Appending the command alone with its command number to list
                    history_list.append(f"{command_number} {command.strip()}")
                    command_number += 1
            
            # Appending the history command that was just executed
            history_list.append(f"{command_number} history")
            
            # Convert to string and return
            result = "\n".join(history_list)
            output["output"] = result
            return output
      
        
        # If history_file does not exist, return None
        else:
            output["error"] = "Error, History file doesn't exist in the directory that this pythons script is in."
            return output
        
    # If user added on top of history command
    else:
        output["error"] = "Error, history command must not have any params, input, or flags."

def cmd_from_history(index):
    '''
    Functions handles the !x command by getting the index value from the command
    and retrieves the history commands then return the at index given
    '''
    
    # directory to store output information
    output = {"output" : None, "error" : None}
    
    # setting index to only value, removing '!'
    index = index[1:]
    
    index = int(index)
    index -= 1
    h_cmds = get_history_rev() or []
        
    # Reverse list so commands are in chronological
    if h_cmds:
        h_cmds.reverse()
        
    # Geting history commands
    if 0 <= index < len(h_cmds):
        
        # Returning cmd at given index
        output["output"] = h_cmds[index].strip()
        return output
    
    # if index is out of range of history
    else:
        output["error"] = f"Error. There are only {len(h_cmds)} commands in history."
        return output

def cp(parts):
    '''
    Copy SOURCE to DEST.

          --help        display this help and exit
    '''

    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    output = {"output" : None, "error" : None}

    if input:
        output["error"] = "Error. Command should not have an input."
        return output
    
    if flags:
        output["error"] = "Error. Command doesn't take flags."
        return output

    try:
        shutil.copy(params[0], params[1])
    except FileNotFoundError:
        output["error"] = f"Error: File {params[0]} not found."
    except PermissionError:
        output["error"] = f"Error: Permission denied when copying {params[0]} to {params[1]}."
    except shutil.SameFileError:
        output["error"] = f"Error: Source and destination {params[0]} are the same file."
    except IsADirectoryError:
        output["error"] = f"Error: One of the paths provided is a directory, not a file."
    except Exception as e:
        output["error"] = f"An unexpected error occurred: {e}"

    return output

def chmod(parts):
    '''
    Change the mode of each FILE to MODE.
    
            The MODE is a three-digit octal number representing the permissions
            for the user, group, and others, respectively. Each digit is a sum of:
            4 (read), 2 (write), and 1 (execute).
            
            For example, to set read, write, and execute permissions for the user,
            and read and execute permissions for the group and others, use 755:
            chmod 755 filename
    
            The following table shows the permission values:
            0    ---    
            1    --x
            2    -w-
            3    -wx
            4    r--
            5    r-x
            6    rw-
            7    rwx

    '''

    # Getting parsed parts
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    # Dictionary to return
    output = {"output" : None, "error" : None}

    # Filter out bad commands
    if input:
        output["error"] = f"{Fore.RED}Error. Command should not have an input.{Style.RESET_ALL}\nRun 'chmod --help' for more info."
        return output
    
    if flags:
        output["error"] = f"{Fore.RED}Error. Command doesn't take flags.{Style.RESET_ALL}\nRun 'chmod --help' for more info."
        return output
    
    if len(params) != 2:
        output["error"] = f"{Fore.RED}Error. Command requires exactly two parameters: MODE and FILE.{Style.RESET_ALL}\nRun 'chmod --help' for more info."
        return output
    
    permission = params[0]
    file = params[1]
    
    # Validating permission string
    if len(permission) != 3 or not permission.isdigit():
        output["error"] = f"{Fore.RED}Error: Invalid permission '{permission}'. Mode should be a three-digit octal number (e.g., 755).{Style.RESET_ALL}\nRun 'chmod --help' for more info."
        return output
    
    for digit in permission:
        if digit < '0' or digit > '7':
            output["error"] = f"{Fore.RED}Error: Invalid permission '{permission}'. Each digit should be between 0 and 7.{Style.RESET_ALL}\nRun 'chmod --help' for more info."
            return output
    
    
    # Seeing if file is an absolute path
    if os.path.isabs(file):
        file_path = file
        
    # If relative path, join with cwd
    else:
        file_path = os.path.join(os.getcwd(), file) 
        
    # File not found
    if not os.path.exists(file_path):
        output["error"] = f"{Fore.RED}Error: {file} could not be found.{Style.RESET_ALL}\nRun 'chmod --help' for more info."
        return output
    
    # Change file permissions
    try:
        # Convert parameters to int
        mode = int(params[0], 8)
        os.chmod(file_path, mode)

    # Catching errors
    except PermissionError:
        output["error"] = f"Error: Permission denied when changing mode of {file}."
    except Exception as e:
        output["error"] = f"An unexpected error occurred: {e}"

    # Return success case
    return output

def ip(parts):
    '''
    Display the IP address of the machine.
    '''
    
    # Getting parsed parts
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)    
    
    # Dictionary to return
    output = {"output" : None, "error" : None}
    
    # Filter out bad commands
    if input or flags or params:
        output["error"] = f"{Fore.RED}Error. Command should not have any input, flags, or params.{Style.RESET_ALL}\nRun 'ip --help' for more info."
        return output
    
    # Getting hostname and IP address
    try:
        hostname = socket.gethostname()
        ip_addr  = socket.gethostbyname(hostname)
        output["output"] = f"IP Address: {ip_addr}"
    except Exception as e:
        output["error"] = f"{Fore.RED}An error occurred while retrieving the IP address: {e}.{Style.RESET_ALL}"
    
    # Return final output
    return output

def date(parts):
    '''
    Display the current date and time.
    '''
    
    # Getting parsed parts
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)    
    
    # Dictionary to return
    output = {"output" : None, "error" : None}
    
    # Filter out bad commands
    if input or flags or params:
        output["error"] = f"{Fore.RED}Error. Command should not have any input, flags, or params.{Style.RESET_ALL}\nRun 'date --help' for more info."
        return output
    
    # Getting current date and time
    # Got time functions from chatGPT
    try:
        current_time = time.strftime("%m-%d-%y %H:%M:%S", time.localtime())
        output["output"] = f"{current_time}"
    except Exception as e:
        output["error"] = f"{Fore.RED}An error occurred while retrieving the date and time: {e}.{Style.RESET_ALL}"
    
    # Return final output
    return output

def clear_screen(parts):
    '''
    Clear the terminal screen.
    '''
    
    # Getting parsed parts
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)    
    
    # Dictionary to return
    output = {"output" : None, "error" : None}
    
    # Filter out bad commands
    if input or flags or params:
        output["error"] = f"{Fore.RED}Error. Command should not have any input, flags, or params.{Style.RESET_ALL}\nRun 'clear --help' for more info."
        return output
    
    # Clear the screen
    clear()
    
    # Return final output
    return output

def run(parts):
    '''
    Launch the Firefox web browser or Nautilus fire manager.
    
    Possible commands: run firefox, run nautilus
    
    Note: 
    
    This command does not take any input or flags.
    Make sure Firefox and Nautilus is installed on your system.
    
    Run only works in a GUI environment.
    Vs Code terminal is not a GUI environment.
    If running in a non-GUI environment, this command will return an error.
    
    To install Firefox and Nautilus:
    1. sudo apt update
    2. sudo apt install firefox -y 
    3. sudo apt install nautilus -y
    '''
    
    # Getting parsed parts
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)    
    
    # Dictionary to return
    output = {"output" : None, "error" : None}
    
    # Throw error if user added input, flags
    if input and flags:
        output["error"] = f"{Fore.RED}Error. Command should not have any input or flags .{Style.RESET_ALL}\nRun 'run_app --help' for more info."
        return output
    
    # Throw error if user didn't provide correct parameter
    if params not in ["firefox", "nautilus"] or len(params) != 1:
        output["error"] = f"{Fore.RED}Error. Command only takes 'firefox' or 'nautilus' as a parameter.{Style.RESET_ALL}\nRun 'run_app --help' for more info."
        return output
    
    # Storing program to run
    program = params.strip().lower()
    
    # Check if DISPLAY exists for GUI
    # firefix needs a display to run
    if "DISPLAY" not in os.environ:
        output["error"] = "Cannot run GUI apps: no display found."
        return output

    # Check if program exists
    # shutil.which searchs for executables in system path
    if shutil.which(program):
        try:
            # Running firefox on its own process so firefox can run independently
            # Suppress output by redirecting to DEVNULL
            # Python script can continue runnning without waiting for firefox to close
            subprocess.Popen([program], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Return nothing on success
            return output
            
        # Catch any exceptions during launch
        except Exception as e:
            output["error"] = f"Error launching {program}: {e}"
            return output
            
    # Program not found in PATH
    else:
        output["error"] = f"Program '{program}' not found in PATH."
        output["error"] = f"Is {program} installed?{Style.RESET_ALL}\nIf it isn't, exit the shell and install."
        output["error"] += f"\nTo install {program}:\n  1. sudo apt update\n  2. sudo apt install {program} -y"
        return output

##### Helper functions for above commands #####

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

def parse_cmd(cmd_input):
    
    '''
    Defining input as values that can only be inputted by the program
    User cannot provide input. That is considered a parameter. For the case
    of wc command. If the user types: wc fruits.txt. fruits.txt is considered
    a parameter. But in the user types: ls | wc. The output of ls is the input in 
    wc.
    '''
    
    
    command_list = []
    
    cmds = cmd_input.split("|")
    
    for cmd in cmds:
        
        # Need to have a check while procession that if error has error in it, stop processing.
        
        d = {"input" : None, "cmd" : None, "params" : [], "flags" : None, "error" : None}
        subparts = cmd.strip().split()
        d["cmd"] = subparts[0]
        
        # Going thorugh the rest of the subparts to classify and store correctly
        for item in subparts[1:]:
            
            if item.startswith("-"):
                d["flags"] = item
            else:
                d["params"].append(item)
                
        # Appending the correct dictionary to command list
        command_list.append(d)
        
    return command_list
                
def color(parts):
    '''
    input: dict({"input" : None, "cmd" : None, "params" : [], "flags" : None, "error" : None})
    output dict: {"output" : string, "error" : string}
    '''
    #global CURRENT_COLOR
    
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    output = {"output" : None, "error" : None}
    
    # Making sure nothing was passed besides the command 'color'
    if not input and not flags and not params:
        #CURRENT_COLOR = Fore.GREEN
        output["output"] = f"Color has been changed to green.\nTo return to default color type command 'stop_color'."
        return output
    # User passed something besides 'color' command
    else:
        output["error"] = "Error. Color could not be changes. 'color' command takes not arguments."
        return output
    
def stop_color(parts):
    '''
    input: dict({"input" : None, "cmd" : None, "params" : [], "flags" : None, "error" : None})
    output dict: {"output" : string, "error" : string}
    '''
    #global CURRENT_COLOR
    
    input = parts.get("input", None)
    flags = parts.get("flags", None)
    params = parts.get("params", None)
    
    output = {"output" : None, "error" : None}
    
    # Making sure nothing was passed besides the command 'color'
    if not input and not flags and not params:
        #CURRENT_COLOR = Style.RESET_ALL
        output["output"] = f"Color has been changed to default."
    
    # User passed something besides 'color' command
    else:
        output["error"] = "Error. Color could not be changes. 'color' command takes not arguments."
        return output

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

    # Update prompt with current working directory
    username      = getpass.getuser()
    computer_name = socket.gethostname()
    cwd           = os.getcwd()
    
    # store built prompt to prompt variable
    prompt = f"{Fore.CYAN}{username}@{computer_name}:{cwd}{Style.RESET_ALL}$ "
    
    
    # Print fix from ChatGPT
    
    # Move cursor to start, print prompt + command
    sys.stdout.write("\r")
    sys.stdout.write(f"{prompt}{cmd}")
    
    # clear everything to the right of the cursor
    sys.stdout.write("\033[K")

    # Move cursor to start
    sys.stdout.write("\r")
    
    # Move cursor to the right the length of the prompt plus cursor_pos
    sys.stdout.write(f"\033[{visible_length(prompt) + cursor_pos}C")
    
    # Flush
    sys.stdout.flush()


# Beginning of main
if __name__ == "__main__":
    
    
    # Allows for colored text in terminal and resets color after each print
    init(autoreset=True)

    # Print welcome message
    WelcomeMessage()
    
    # List of commands user may request to execute
    available_commands = ["ls", "pwd", "mkdir", "cd", "cp", "mv", "rm", "cat",
                          "head", "tail", "grep", "wc", "chmod", "history",
                          "exit", "more", "less", "sort", "help", "ip", "date",
                          "clear", "run"]

    
    # Empty cmd variable
    cmd = ""
    
    # For handling left/right arrow keys
    cursor_pos = 0

    # For handling up/down arrow keys
    history_index = -1
    
    # Print to terminal
    print_cmd(cmd)

    # Loop forever
    while True:

        char = getch()  # read a character (but don't print)

        # Exit shell on ctrl-c command
        if char == "\x03":
            print()
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
                    
                # Moving cursor to length of new cmd and print cmd
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
                    
                # Moving cursor to length of new cmd and print cmd
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

        elif char in "\r":  # return pressed
            
            # Printing blank line to info isn't overwritten
            print()
            
            if cmd == "exit":
                exit_shell()

            # If there is a command to execute
            if(cmd):
                
                # Part command and returning list of dictionaries
                command_list = parse_cmd(cmd)
                result = {"output" : None, "error" : None}
                
                # Handle if user wants to run !x command
                if len(command_list) == 1 and command_list[0].get("cmd").startswith("!"):
                    
                    # Get the cmd and send to function.
                    # It includes ! but we will remove in function
                        result = cmd_from_history(command_list[0].get("cmd"))
                        
                        #Setting cmd to 'x' command from !x
                        if result["error"]:
                            
                            # Set command list to zero
                            command_list = []
                            
                        # Setting command_list to result command from !x command
                        else:
                            command_list = parse_cmd(result["output"])
                            cmd = result["output"]
                            result["output"] = None
                            
                            # Printing to the user what is about to be executed
                            print()
                            print("Command(s) being executed.")
                            print("--------------------")
                            for command in command_list:
                                print("Command:", command.get("cmd"))
                                print("Flags:", command.get("flags"))
                                print("Params:", command.get("params"))
                                print("--------------------")
                            print()

                # Executing each command in the command list
                while len(command_list) != 0:
            
                    # Pop first command off of the command list
                    command = command_list.pop(0)
                    
                    # Making sure valid command
                    if command.get("cmd") not in available_commands:
                        result["error"] = f"Error. command '{command.get("cmd")}' is not in list of avaiable commands."
                        
                    # If there is output in the previous command and command has not input
                    # make the output to the previous command the input to the next
                    if result["output"] and not command["input"]:
                        command["input"] = result["output"] 
                    
                    # Kill execution if error
                    if result["error"]:
                        break

                    # Executing command depending on cmd input
                    if command.get("flags") == "--help" and not command.get("params") and not command.get("input"):
                        result = help(command)                        
                    elif command.get("cmd") == "cd":
                        result = cd(command)
                    elif command.get("cmd") == "ls":
                        result = ls(command)
                    elif command.get("cmd") == "pwd":
                        result = pwd_()
                    elif command.get("cmd") == "mkdir":
                        result = mkdir(command)
                    elif command.get("cmd") == "history":
                        result = history(command)
                    elif command.get("cmd") == "wc":
                        result = wc(command)
                    elif command.get("cmd") == "cp":
                        result = cp(command)
                    elif command.get("cmd") == "cat":
                        file = command.get("params")
                        result = cat(file)
                    elif command.get("cmd") == "grep":
                        result = grep(command)
                    elif command.get("cmd") == "sort":
                        result = sort(command)
                    elif command.get("cmd") == "chmod":
                        result = chmod(command)
                    elif command.get("cmd") == "ip":
                        result = ip(command)
                    elif command.get("cmd") == "date":
                        result = date(command)
                    elif command.get("cmd") == "clear":
                        result = clear_screen(command)
                    elif command.get("cmd") == "run":
                        result = run(command)
                    #elif command.get("cmd") == "color":
                    #    result = color(command)
                    #elif command.get("cmd") == "stop_color":
                    #    result = stop_color(command)


                            
                # Printing result to screen
                if result["error"]:
                    print(result["error"])
                elif result["output"]:
                    print(result["output"])


            # Writing command to history
            write_to_history(cmd)

            # Setting cmd back to blank and cursor back to 0
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