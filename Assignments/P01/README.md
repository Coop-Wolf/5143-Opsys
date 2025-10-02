## Overview

In this project, we will implement a basic "shell". A shell is a command-line interface we often interact with, and provides an powerful interface with your system. Below is an overview of the actions our shell will perform:

1. Print a prompt(`$: `) to the user.
2. Read a command line from stdin.
3. Tokenize (lexically analyze) the command a create an array of command parts (tokens).
4. Parse the token array to identify the command and its arguments.

## Requirements

- **Language**: Python

- **Command Features**:
    - Each command returns a string.
    - Commands can accept input from other commands.

Our shell will support the following command types:

### 1. **Exit Command**

- **Command**: `exit`
- **Description**: Terminates the shell.
- **Concepts**: Exiting the shell with system calls like exit().

### 2. **Command without Arguments**

- **Example**: `ls`
- **Description**: Executes a command without arguments and waits for it to complete.
- **Concepts**: Synchronous execution, process forking.

### 3. **Command with Arguments**

- **Example**: `ls -l`
- **Description**: Parses command-line arguments and executes the command.
- **Concepts**: Command-line paramaters.

### 4. **Output Redirection**

- **Example**: `ls > output.txt`
- **Description**: Redirects the command output to a specified file.
- **Concepts**: File operations, output redirection.

### 5. **Input Redirection**

- **Example**: `sort < inputfile.txt`
- **Description**: Takes input from a file instead of the user’s input.
- **Concepts**: File operations, input redirection.

### 6. **Piping Commands**

- **Example**: `ls -l | more`
- **Description**: Passes the output of one command as input to another command.
- **Concepts**: Pipes, synchronous operations.

## Timeline:
01 Sept 2025 - 30 Sept 2025

## Group Members:
- Tim Haxton
- Harika Vemulapalli
- Cooper Wolf

## Files:
| Files                 | Description                                         |
|-----------------------|-----------------------------------------------------|
| practice_shell.py     | Secondary script used for development purposes.     |
| shell2.py             | Working shell script.                               |
| getch.py              | Class that reads in each character.                 |
| history.txt           | Text file that contains past shell commands.        |
| test.txt              | Text file used to test various commands.            |
| numtext               | Text file of numeric values used to test commands.  |
| bacon                 | Text file used for testing commands.                |
| valuable_notes.txt    | Contains notes and reminders for the project.       |

## Instructions:
- Clone the repository or connect through GitHub CodeSpaces in VS Code
- Locate the directory where the program exists
- Run `shell2.py` in the terminal using command: `python3 shell2.py` or `python shell2.py`
- A welcome message will be displayed as well as a prompt where you may begin execute the commands below

## Commands:
| Command               | Description                                         | Author   |
|-----------------------|-----------------------------------------------------|----------|
| `ls`                  | List files and directories                          | Cooper   |
| `pwd`                 | Print working directory                             | Cooper   |
| `mkdir`               | Create a directory.                                 | Cooper   |
| `cd directory`        | Change to a named directory.                        | Cooper   |
| `cp file1 file2`      | Copy file1 to file2.                                | Tim      |
| `mv file1 file2`      | Move or rename file1 to file2.                      | Tim      |
| `rm -r`               | Recursively delete a directory.                     | Tim      |
| `cat file`            | Display contents of a file.                         | Harika   |
| `head -n`             | Display the first n lines of a file.                | Harika   |
| `tail -n`             | Display the last n lines of a file.                 | Harika   |
| `grep 'pattern' file` | Search for a pattern in a file.                     | Cooper   |
| `wc`                  | Count lines, words in a file.                       | Cooper   |
| `history`             | Show previously used commands.                      | Cooper   |
| `!x`                  | Re-run command number *x* from history.             | Cooper   |
| `exit`                | Exits the shell.                                    | Cooper   |
| `up & down arrows`    | Navigate previous command                           | Cooper   |
| `left & right arrows` | Move cursor                                         | Cooper   |
| `chmod xxx`           | Change file permissions.                            | Cooper   |
| `more`                | View contents of a file                             | Tim      |
| `less`                | View contents of a file                             | Tim      |
| `[program] > file`    | Redirects output of a command into a file           | Tim      |
| `[program] < file`    | Redirects a file as input into a command            | Harika   |
| `sort `               | Sorts contents of a file.                           | Cooper   |


## Commands that malfunctioned:
|Command               |      Error             |     Solution |
|----------------------|------------------------|---------------------------------------|
| _cd ~_               |   broke the shell      | If statement containing piping syntax was misaligned in code |                            
| ll                   |   broke the shell      | "                                                           " |
| cat bacon.txt | sort |   error with piping    | "                                                           " |
| less h q / ?   |   breaks the shell     | added help buffer/created display buffer copy earlier to allow display  buffer reference swap | 
| grep as as file.txt  |   grep was trying to process mul patterns |   only allow for a single patterns without flag |

## Highs and Lows:
- Highs
  - Cooper
    - The first time piping worked
    - Finally figuring out the 'grep' command
    - When our second presentation went well
    - Adding the extra features and having them work
- Lows
  - Cooper
    - Grep command kept failing
    - Figuring out the arrow keys
    - When the first presentation didn't go as expected

## Extras:
- Color ls contents if they are directory or executable
- 'ls -merica' colors list contents red white and blue
- date command that displays date and time
- clear command that clears the screen
- ip command that displays ip address
- run command runs an application
- 'commands' command that prints list of working commands


## References:
- [Geeksforgeeks](https://www.geeksforgeeks.org/python/executing-shell-commands-with-python/)
- [ChatGPT](https://chatgpt.com/)
- [Python Docs](https://docs.python.org/3/library/os.html)
- [Terminal Width](https://www.google.com/search?q=get+terminal+width+python&rlz=1C1VDKB_enUS1178US1178&oq=get+terminal+w&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBggBEEUYOTINCAIQABjwBRieBhjIBjIHCAMQABiABDIHCAQQABiABDIICAUQABgWGB4yCAgGEAAYFhgeMggIBxAAGBYYHjIICAgQABgWGB4yCAgJEAAYFhgeqAIHsAIB8QVQ2yUT5i1rPPEFUNslE-Ytazw&sourceid=chrome&ie=UTF-8&safe=active&ssui=on)
- [Terminal Username](https://www.google.com/search?q=get+terminal+username+python&sca_esv=e7bf22627bcd1c5c&rlz=1C1VDKB_enUS1178US1178&ei=REvAaIzVNv21qtsPwYnX4Q0&ved=0ahUKEwiMh5DkgsyPAxX9mmoFHcHENdwQ4dUDCBI&uact=5&oq=get+terminal+username+python&gs_lp=Egxnd3Mtd2l6LXNlcnAiHGdldCB0ZXJtaW5hbCB1c2VybmFtZSBweXRob24yBRAhGKABMgUQIRigATIFECEYoAEyBRAhGKABMgUQIRigATIFECEYnwUyBRAhGJ8FMgUQIRifBTIFECEYnwUyBRAhGJ8FSMwLUCNY9AlwAXgBkAEAmAFroAH6BKoBAzYuMbgBA8gBAPgBAZgCCKACkQXCAgoQABiwAxjWBBhHwgIGEAAYFhgewgIIEAAYgAQYogTCAgUQIRirApgDAIgGAZAGCJIHAzcuMaAH0SyyBwM2LjG4B40FwgcFMC43LjHIBw8&sclient=gws-wiz-serp&safe=active&ssui=on)
