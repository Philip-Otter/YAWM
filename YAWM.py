import argparse
import random
import re
from datetime import datetime

class application():
    def __init__(self, inFile, outfile, verbose, rawOutput):
        self.wordlistPath = inFile
        self.outFile = outfile
        self.wordlistLines = []
        self.verbose = verbose
        self.rawOutput = rawOutput

        self.wordlistEncoding = 'utf8'
        self.minLength = None
        self.linePolicy = None
        self.lineAppender = None
        self.linePreAppender = None
        self.wordlistB_Path = None
    

    def linePolicyCheck(self,line):
        if(self.verbose):
            print(f"Line Policy Check Started: {datetime.now().strftime('%H:%M:%S')}")
            print(f"Checking Policies Against line:  {line}")
        
        if(self.linePolicy == None):
            if(self.verbose):
                print(f"Line Policy Check Ended: {datetime.now().strftime('%H:%M:%S')}")
            return True
    
        if("s" in self.linePolicy):  # Special Character Check
            reMatcher = re.compile('[^A-Z0-9a-z\s]|[ ]')
            if(reMatcher.search(line)):
                if(self.verbose):
                    print(f"Line Passed Special Character Policy Check")
            else:
                if(self.verbose):
                    print(f"Line Policy Check Ended: {datetime.now().strftime('%H:%M:%S')}")
                return False
        if("u" in self.linePolicy):  # Uppercase Character Check
            reMatcher = re.compile('[A-Z]')
            if(reMatcher.search(line)):
                if(self.verbose):
                    print(f"Line Passed Upper Character Policy Check")
            else:
                if(self.verbose):
                    print(f"Line Policy Check Ended: {datetime.now().strftime('%H:%M:%S')}")
                return False 
        if("l" in self.linePolicy):  # Lowercase Character Check
            reMatcher = re.compile('[a-z]')
            if(reMatcher.search(line)):
                if(self.verbose):
                    print(f"Line Passed Lower Character Policy Check")
            else:
                if(self.verbose):
                    print(f"Line Policy Check Ended: {datetime.now().strftime('%H:%M:%S')}")
                return False 
        if("n" in self.linePolicy):  # Numeric Character Check
            reMatcher = re.compile('[0-9]')
            if(reMatcher.search(line)):
                if(self.verbose):
                    print(f"Line Passed Numeric Character Policy Check")
            else:
                if(self.verbose):
                    print(f"Line Policy Check Ended: {datetime.now().strftime('%H:%M:%S')}")
                return False 
            

        if(self.verbose):
            print(f"Line Policy Check Ended: {datetime.now().strftime('%H:%M:%S')}")
        return True
            

    def lineLengthCheck(self,line):
        if(self.verbose):
            print(f"Line Length Check Started: {datetime.now().strftime('%H:%M:%S')}")

        if(self.minLength == None):
            if(self.verbose):
                print(f"Line Length Check Ended: {datetime.now().strftime('%H:%M:%S')}")
            return True
        else:
            if(len(line) >= self.minLength):
                if(self.verbose):
                    print(f"Line Length Check Ended: {datetime.now().strftime('%H:%M:%S')}")
                return True

        if(self.verbose):
            print(f"Line Length Check Ended: {datetime.now().strftime('%H:%M:%S')}")
        return False 


    def appendLine(self, line):
        if(self.verbose):
            print(f"Line Appending Started: {datetime.now().strftime('%H:%M:%S')}")

        line = line.strip("\n")
        line = line + self.lineAppender + "\n"

        if(self.verbose):
            print(f"Line Appending Ended: {datetime.now().strftime('%H:%M:%S')}")
        return line


    def preAppendLine(self, line):
        if(self.verbose):
            print(f"Line Pre-Appending Started: {datetime.now().strftime('%H:%M:%S')}")

        line = self.linePreAppender + line

        if(self.verbose):
            print(f"Line Pre-Appending Ended: {datetime.now().strftime('%H:%M:%S')}")
        return line

    
    def readWordlist(self, wordlistPath):
        if(self.verbose):
            print(f"Wordlist File Read Started: {datetime.now().strftime('%H:%M:%S')}")

        with open(wordlistPath, 'r', encoding=self.wordlistEncoding) as file:
            for line in file:
                # Pre-Policy Check Modifiers
                if(self.lineAppender != None):
                    line = self.appendLine(line)
                if(self.linePreAppender != None):
                    line = self.preAppendLine(line)

                # Length & Policy Check
                if(self.lineLengthCheck(line)):
                    if(self.linePolicyCheck(line)):
                        if(self.verbose):
                            print(f"Storing Line:  {line}", end="")

                        self.wordlistLines.append(line)
        file.close()

        if(self.verbose):
            print(f"Wordlist File Read Ended: {datetime.now().strftime('%H:%M:%S')}")
    

    def writeOutputFile(self, outputLines):
        if(self.verbose):
            print(f"Outfile Write Started: {datetime.now().strftime('%H:%M:%S')}")

        with open(self.outFile, 'w') as file:
            for line in outputLines:
                if(self.verbose):
                    print(f"Writing Line:  {line}", end="")
                file.write(line)
        file.close()
        
        if(self.verbose):
            print(f"Outfile Write Ended: {datetime.now().strftime('%H:%M:%S')}")
    

    def outputRaw(self, outputLines):
        for line in outputLines:
            print(f"{line}",end="")
    

    def shuffle(self):
        if(self.verbose):
            print(f"Shuffle Started: {datetime.now().strftime('%H:%M:%S')}")
        
        self.readWordlist(self.wordlistPath)
        random.shuffle(self.wordlistLines)
        if(self.rawOutput):
            self.outputRaw(self.wordlistLines)    
        
        if(self.outFile != None):
            self.writeOutputFile(self.wordlistLines)
    
        if(self.verbose):
            print(f"Shuffle Ended: {datetime.now().strftime('%H:%M:%S')}")
    

    def merge(self):
        if(self.verbose):
            print(f"Merge Started: {datetime.now().strftime('%H:%M:%S')}")
        
        if(self.wordlistB_Path == None):
            print("No Merging Wordlist Defiened!\nExiting!")
            exit()
        
        wordlistLinesA = []
        
        self.readWordlist(self.wordlistPath)
        wordlistLinesA = self.wordlistLines.copy()
        self.wordlistLines.clear()
        self.readWordlist(self.wordlistB_Path)

        newLineList = list(set(self.wordlistLines+wordlistLinesA))

        if(self.rawOutput):
            self.outputRaw(newLineList)
        
        if(self.outFile != None):
            self.writeOutputFile(newLineList)
        
        if(self.verbose):
            print(f"Merge Ended: {datetime.now().strftime('%H:%M:%S')}")


parser = argparse.ArgumentParser(prog='YAWM.py',
                                 description='Yet Another Wordlist Manager')

parser.add_argument('Mode', help="Set Modifier Mode:  Shuffle, Merge")
parser.add_argument('-f', '--wordlist', help='Set Input WordList')
parser.add_argument('-o', '--outFile', help="Set Output File")
parser.add_argument('-v', '--verbose', action='store_true', help='Enable Verbose Output')
parser.add_argument('-E', '--encoding', help='Overide Default Wordlist Encoding of "utf8"')
parser.add_argument('--raw', action='store_true', help='(Output New Wordlist To Terminal)')
parser.add_argument('--min', help='Set Minimum Number of Characters')
parser.add_argument('--policy', help='Output Only Lines That Match A Policy:  s[special Chars], u[Upper], l[Lower], n[Number]')
parser.add_argument('-a', '--append', help='Set String to Append to Lines')
parser.add_argument('-p', '--preappend', help='Set String to Pre-Append to Lines')
parser.add_argument('--merge', help='Set File Path of Wordlist B During A Merge')

args = parser.parse_args()

if(args.outFile == None):
    args.raw = True

newApplication = application(args.wordlist, args.outFile, args.verbose, args.raw)

if(args.min != None):
    newApplication.minLength = int(args.min)
if(args.policy != None):
    newApplication.linePolicy = str(args.policy).lower()
if(args.append != None):
    newApplication.lineAppender = str(args.append)
if(args.preappend != None):
    newApplication.linePreAppender = str(args.preappend)
if(args.merge != None):
    newApplication.wordlistB_Path = str(args.merge)

match str(args.Mode).lower():
    case "shuffle":
        newApplication.shuffle()
    case "merge":
        newApplication.merge()
    case _:
        print(f"No Mode Option Matches:  {args.Mode}\nExiting!")