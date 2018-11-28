from handle_args import ArgParse
import re
import sys

blankLine = re.compile(r"^\s*$")

def cat(options, file):
    countAll = 'n' in options
    countNonBlank = 'b' in options
    if file != "-":
        with open(file, 'r') as f:
            line_no = 0
            for line in f:
                line = line[:-1]
                if countAll:
                    line_no += 1
                    print("%5d  %s" % (line_no, line))
                elif countNonBlank:
                    if not blankLine.match(line):
                        line_no += 1
                        print("%5d  %s" % (line_no, line))
                    else:
                        print(line)
                else:
                    print(line)

def catall(options, files):
    for file in files:
        cat(options, file)

if __name__ == '__main__':
    from sys import argv
    parsed = ArgParse(set(['b', 'n']), set(), argv)
    if 'b' in parsed.argsSet and 'n' in parsed.argsSet:
        print('Both b and n options cannot be specified')
        sys.exit(1)
    catall(parsed.argsSet, parsed.argsPositional)
