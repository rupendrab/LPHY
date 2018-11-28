## Parse command line arguments

class ArgParse:

    def __init__(self, setOptions, mapOptions, args):
        self.valid = True
        self.programName = args[0]
        self.args = args[1:]
        self.setOptions = setOptions
        self.mapOptions = mapOptions
        self.parse()

    def parse(self):
        self.argsSet = set()
        self.argsMap = {}
        self.argsPositional = []
        if not self.args:
            return
        # This variable indicates if there is a -p, -s or -e encountered, so the next param will be the
        # corresponding value
        mapKey = None
        for arg in self.args:
            if arg.startswith("-h") or arg.startswith("-help"):
                print(self.help())
                self.valid = False
                return
            if arg.startswith("-"):
                if self.argsPositional:
                    print("Options must be specified before positional parameters")
                    self.valid = False
                    return
                opt = arg[1:]
                if opt in self.setOptions:
                    self.argsSet.add(opt)
                elif opt in self.mapOptions:
                    mapKey = opt
                else:
                    print("Invalid option %s" % arg)
                    self.valid = False
                    return
            elif mapKey:
                self.argsMap[mapKey] = arg
                mapKey = None
            else:
                self.argsPositional.append(arg)

    def help(self):
        return """
        Usage: %s -h 
        or     %s -m -n -t -p fileType -s startLine -e endLine fileName1 fileName2 ... fileNamen
        """ % (self.programName, self.programName)

def main(args):
    parsed = ArgParse(set(['m', 'n', 't']), set(['p', 's', 'e']), args)
    if parsed.valid:
        print(parsed.argsSet)
        print(parsed.argsMap)
        print(parsed.argsPositional)

if __name__ == '__main__':
    from sys import argv
    main(argv)
