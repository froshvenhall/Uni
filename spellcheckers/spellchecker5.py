# Assessment 1.5 -- SPELLCHECKER5-- created by Frederick Hall -- due Friday 8 Nov 6pm

import string # For removing punctuation
import re # For removing the £ sign as is not in string.puncuation string
import time # For outputting time taken and appending the datetime to the file
from difflib import SequenceMatcher

# Open englishwords.txt into a file
f = open("englishwords.txt", "r")

# Splitting of the file englishwords.txt into a list to make it easier to pass through
lines = []
for line in f:              
    line = line.rstrip()    
    lines.append(line)

# Remove non alpha characters module
def removepuncandig(terms):
    
    terms = terms.lower() # capitals
    translation = str.maketrans("", "", string.punctuation) # Puncuation removal
    terms = terms.translate(translation)

    terms = re.sub('£', '', terms) # £ sign as not in punctuation

    translation2 = str.maketrans("", "", string.digits) # Digits removal
    terms = terms.translate(translation2)
    return(terms)
    
# Spellchecker module
def spellchecker(words):
    # Counters for opportunities
    ignored = 0
    marked = 0
    newdicword = 0

    words = words.split() # Break up the inputted text into a list to parse through easier
    i = 0
    wordsfalse = 0
    wordstrue = 0
    j = 0
    while i < len(words):
        j = 0
        score1 = SequenceMatcher(None, lines[j], words[i]).ratio() # set score 1
        wordrec = lines[j]
        
        while j < len(lines):
            score2 = SequenceMatcher(None, lines[j], words[i]).ratio() # set score of next word
            if score2 > score1: # If second word has higher score than first, replace
                score1 = score2 # other wise leave as is
                wordrec = lines[j] # Word to recommend
                continue
            
            if words[i] == lines[j]:
                if sent == True:
                    print("\n" + words[i] + " is spelt correctly.")
                else:
                    None
                i += 1
                wordstrue += 1
                break
            elif j == (len(lines) - 1): # If parser reaches end of dictionary, word is false
                if sent == True:
                    print("\n" + words[i] + " not found in dictionary")
                else:
                    None

                # Provide bordering for menu choices and output
                print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
                print(u"\u007C" + (17*u"\u0020") + "WORD NOT FOUND" + (15*u"\u0020") + u"\u007C")
                print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                print(u"\u007C" + "  " + words[i] + ((44 - len(words[i]))*u"\u0020") + "|")
                print(u"\u007C" + "  Did you mean:" + 31*u"\u0020" + "|")
                print(u"\u007C" + "  " + wordrec + ((44 - len(wordrec))*u"\u0020") +"|")
                print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
                change = input("Enter [y] or [n]: ")
                if change == "y":
                    words[i] = wordrec
                elif change == "n":
                    # Border using unicode for menu
                    print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
                    print(u"\u007C" + (17*u"\u0020") + "WORD NOT FOUND" + (15*u"\u0020") + u"\u007C")
                    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                    print(u"\u007C" + "  1. Ignore the word" + 26*u"\u0020" + "|")
                    print(u"\u007C" + "  2. Mark the word as incorrect" + 15*u"\u0020" + "|")
                    print(u"\u007C" + "  3. Add word to dictionary" + 19*u"\u0020" + "|")
                    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
                    print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
                    
                    opportunity = input("Enter choice: ")
                    if opportunity == "1":
                        words[i] = "!" + words[i] + "!" # Ignore word
                        ignored += 1
                    elif opportunity == "2":
                        words[i] = "?" + words[i] + "?" # Mark word
                        marked += 1
                    elif opportunity == "3":
                        print(words[i] + " added to dictionary.\n")
                        addtodic = open("englishwords.txt", "a") # Add word to dictionary
                        addtodic.write("\n" + words[i])
                        addtodic.close()
                        words[i] = "*" + words[i] + "*"
                        newdicword += 1
                    else:
                        print("Please enter a valid input\n") # Error handling
                        continue
                else:
                    print("Please enter a valid input\n") # Error handling
                    continue
                i += 1
                wordsfalse +=1
                break
            else:
                j += 1

    # Output facts about inputted sentence
    print("Number of words: " + str(len(words)))
    print("Number of correctly spelt words: " + str(wordstrue) + "/" + str(len(words)))
    print("Number of incorrectly spelt words: " + str(wordsfalse) + "/" + str(len(words)))

    print("--Number ignored: " + str(ignored))
    print("--Number marked: " + str(marked))
    print("--Number added to dictionary: " + str(newdicword))

    print("Time elapsed: " + str(time.time() - start_time) + "s")

    if sent == False:
        # Write information to incorrect words file
        incorrectfile = open("incorrectwords.txt", "w+")
        incorrectfile.write(str(time.ctime()) + "\n\n")
        incorrectfile.write("\nNumber of words: " + str(len(words)))
        incorrectfile.write("\nNumber of correctly spelt words: " + str(wordstrue) + "/" + str(len(words)))
        incorrectfile.write("\nNumber of incorrectly spelt words: " + str(wordsfalse) + "/" + str(len(words)))
        incorrectfile.write("\n--Number ignored: " + str(ignored))
        incorrectfile.write("\n--Number marked: " + str(marked))
        incorrectfile.write("\n--Number added to dictionary: " + str(newdicword) + "\n")
        words = " ".join(words)
        incorrectfile.write("\n" + words)

        incorrectfile.close()
    else:
        None

cont = True
while cont == True:
    sent = False
    print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
    print(u"\u007C" + (17*u"\u0020") + "SPELL CHECKER" + (16*u"\u0020") + u"\u007C")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\u007C" + "  1. Check a file" + 29*u"\u0020" + "|")
    print(u"\u007C" + "  2. Check a sentence" + 25*u"\u0020" + "|")
    print(u"\u007C" + "  0. Quit" + 37*u"\u0020" +"|")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
    decision = input("Enter Choice: ")
    print("\n\n")

    # Loop to spellcheck file
    if decision == "1":
        # Bordering for file name entry
        print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
        print(u"\u007C" + (19*u"\u0020") + "LOAD FILE" + (18*u"\u0020") + u"\u007C")
        print(u"\u007C" + (46*u"\u0020") + u"\u007C")
        print(u"\u007C" + "  Enter the file name" + 25*u"\u0020" + "|")
        print(u"\u007C" + "  then press enter" + 28*u"\u0020" + "|")
        print(u"\u007C" + (46*u"\u0020") + u"\u007C")
        print(u"\u007C" + (46*u"\u0020") + u"\u007C")
        print(u"\u007C" + (46*u"\u0020") + u"\u007C")
        print(u"\u007C" + (46*u"\u0020") + u"\u007C")
        print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")    
    

        file = input("Enter file name: ")
        
        start_time = time.time() # Start timer
        try:
            filetocheck = open(file, "r")
        except FileNotFoundError:  # Error handling if file to open doesnt exist
            print("\n!!!!!!!!!!!!!!!!!402_FILE_NOT_FOUND_ERROR!!!!!!!!!!!!!!!!!\n")
            continue
        filetocheck = open(file, "r")
        para = ""
        for line in filetocheck:
            line = line.strip()
            para = para + line

        para = removepuncandig(para)
        para = spellchecker(para)
        
        filetocheck.close()
        
    # Loop to check a sentence until q decided
    elif decision == "2":
        sent = True
        print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
        print(u"\u007C" + (17*u"\u0020") + "SENTENCE CHECKER" + (13*u"\u0020") + u"\u007C")
        print(u"\u007C" + (46*u"\u0020") + u"\u007C")
        print(u"\u007C" + (46*u"\u0020") + u"\u007C")
        print(u"\u007C" + (46*u"\u0020") + u"\u007C")
        print(u"\u007C" + (46*u"\u0020") + u"\u007C")
        print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
            
        sentence = input("Enter sentence here: ")

        start_time = time.time()
        
        sentence = removepuncandig(sentence)

        print("\nHere is your entry: \n\n" + sentence  + "\n")

        # Spellcheck sentence
        spellchecker(sentence)
    elif decision == "0":
        cont = False
        break

    # Error handling
    elif decision != "1" or "2" or "0":
        print("Please input a valid choice")
        continue
    # User decision to input another sentence or quit
    print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\u007C" + "  Enter q to quit or" + 26*u"\u0020" + "|")
    print(u"\u007C" + "  anything else to continue" + 19*u"\u0020" + "|")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\u007C" + (46*u"\u0020") + u"\u007C")
    print(u"\uFF0B" + 45*u"\u2212" + u"\uFF0B")    

    carryon = input("Enter choice: ")
    if carryon == "q":
        cont = False
    else:
        cont = True

print("\n\nCLOSING PROGRAM . . .\n\n") # Goodbye python

# Don't forget to close the file!!!!
f.close()

