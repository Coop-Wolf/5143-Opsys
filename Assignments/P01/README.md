
04 Sep 2025
5143 Shell Project
Group Members:
- Tim Haxton
- Harika Vemulapalli
- Cooper Wolf

## Overview:
This project implements a basic shell in Python that supports a variety of commands.

## Files
| Files                 | Description                                         | Author   |
|-----------------------|-----------------------------------------------------|----------|
| Dev_shell.py          | Python script used for development.                 | Cooper   |
| Practice_shell.py     | Secondary script used for development purposes.     | Cooper   |
| shell2.py             | Working shell script.                               | Cooper   |
| getch.py              | python file that.                                   | Cooper   |
| history.txt           | txt file that contains past shell commands.         | Cooper   |
| test.txt              | txt file used to test various commands.             | Cooper   |
| numtext               | txt file of numeric values used to test commands.   | Cooper   |
| bacon                 | txt file used for testing commands.                 | Cooper   |
| valuable_notes        | Contains notes and reminders for the project.       | Cooper   |

## Instructions:
Clone the repository or connect through VS Code Spaces
Run the `shell2.py` file and use the following commands...

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
| `more`                |                                                     | Tim      |
| `less`                |                                                     | Tim      |
| `[program] > file`    |                                                     | Tim      |
| `[program] < file`    |                                                     | Harika   |
| `sort `               | Sorts contents of a file.                           | Cooper   |

## Non-Working Components:
- head
- tail
- more
- less
- "<"
- ">"

## Extras
- Color ls contents if they are directory or executable
- 'ls -merica' colors list contents red white and blue
- date command that displays date and time
- clear command that clears the screen
- ip command that displays ip address
- run command runs an application


## References:
- [geeksforgeeks](https://www.geeksforgeeks.org/python/executing-shell-commands-with-python/)
- [ChatGPT](https://chatgpt.com/)
- [Python Docs](https://docs.python.org/3/library/os.html)
