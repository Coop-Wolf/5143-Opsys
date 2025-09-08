
04 Sep 2025
5143 Shell Project
Group Members:
- Tim Haxton
- Harika Vemulapalli
- Cooper Wolf

## Overview:
This project implements a basic shell in Python that supports a variety of commands.

## Instructions:
Clone the repository.
install requests is haven't already
    - pip install requests
Run the `shell.py` file and use the following commands...

## Commands:
| Command               | Description                                         | Author   |
|-----------------------|-----------------------------------------------------|----------|
| `ls`                  | List files and directories                          | Cooper   |
| `pwd`                 | Print working directory                             | Cooper   |
| `ls -a`               | List all files, including hidden ones.              | Cooper   |
| `ls -l`               | Long listing format.                                | Cooper   |
| `ls -h`               | Human-readable file sizes.                          | Cooper   |
| `mkdir`               | Create a directory.                                 | Cooper   |
| `cd directory`        | Change to a named directory.                        | Cooper   |
| `cd`                  | Change to the home directory if no argument given.  | Cooper   |
| `cp file1 file2`      | Copy file1 to file2.                                |          |
| `mv file1 file2`      | Move or rename file1 to file2.                      |          |
| `rm -r`               | Recursively delete a directory.                     |          |
| `cat file`            | Display contents of a file.                         |          |
| `head -n`             | Display the first n lines of a file.                |          |
| `tail -n`             | Display the last n lines of a file.                 |          |
| `grep 'pattern' file` | Search for a pattern in a file.                     |          |
| `wc -l`               | Count lines in a file.                              |          |
| `wc -w`               | Count words in a file.                              |          |
| `chmod xxx`           | Change file permissions.                            |          |
| `history`             | Show previously used commands.                      | Cooper   |
| `!x`                  | Re-run command number *x* from history.             | Cooper   |
| `exit`                | Exits the shell.                                    | Cooper   |
| `up & down arrows`    | Navigate previous command                           | Cooper   |
| `left & right arrows` | Move cursor                                         | Cooper   |
| `more`                |                                                     |          |
| `less`                |                                                     |          |
| `[program] > file`    |                                                     |          |
| `[program] < file`    |                                                     |          |
| `hfind`               |                                                     |          |
| `piping`              |                                                     |          |

## Non-Working Components:
cp
mv
rm
cat
head
tail
grep
wc
chmod
more
less
"<"
">"
hfind
commands with piping


## References:
- [geeksforgeeks](https://www.geeksforgeeks.org/python/executing-shell-commands-with-python/)
- [ChatGPT](https://chatgpt.com/)
- [Python Docs](https://docs.python.org/3/library/os.html)