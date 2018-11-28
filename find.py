import argparse
import os
from os import listdir
from os.path import isfile, join, isdir
import re
import subprocess

def create_regex_pattern(glob_pattern):
    if not glob_pattern:
        return "^.*$"
    nChars = ['^']
    for c in glob_pattern:
        if c == '*':
            nChars.append('.')
        nChars.append(c)
    nChars.append('$')
    return re.compile(''.join(nChars))

def listFiles(dirName, pattern):
    fileList = []
    if isdir(dirName) and pattern.match(dirName):
        fileList.append(dirName)
    files = listdir(dirName)
    for f in files:
        filePath = join(dirName, f)
        if isdir(filePath):
            fileList += listFiles(filePath, pattern)
        else:
            if pattern.match(f):
                fileList.append(filePath)

    return fileList

def printAll(fileList):
    for f in fileList:
        print(f)

def run_exec(fileName, cmdList):
    cmds = []
    for cmdPart in cmdList:
        cmdPart = cmdPart.replace("{}", fileName)
        cmds.append(cmdPart)
    # print(' '.join(cmds))
    run_cmd(cmds)

def run_exec_all(fileList, parsed):
    if not fileList:
        return
    for fileName in fileList:
        run_exec(fileName, parsed.exec)

def run_cmd(cmds):
    result = subprocess.run(cmds, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.stdout:
        for line in result.stdout.decode('utf-8').split('\n'):
            print(line)

def process(parsed):
    print(parsed)
    if not parsed:
        return
    pattern = create_regex_pattern(parsed.name)
    fileList = listFiles(parsed.root_directory, pattern)
    if parsed.print:
        printAll(fileList)
    if parsed.exec:
        run_exec_all(fileList, parsed)

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("root_directory",
                        help="Start searching from this directory as root")
    parser.add_argument("-name", 
                        help="File name pattern")
    parser.add_argument("-print", action="store_true",
                        help="Print the file names found")
    parser.add_argument("-type",
                        help="Type of file: f or d")
    parser.add_argument("-exec", nargs='+',
                        help="Execute the command for all files found")
    parsed = parser.parse_args()
    process(parsed)

if __name__ == '__main__':
    from sys import argv
    main(argv)
