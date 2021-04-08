# Assessment 1.3 -- SPELLCHECKER3 -- created by Frederick Hall -- due Friday 8 Nov 6pm

import string # For removing punctuation
import re # For removing the £ sign as is not in string.puncuation string
#import datetime #  For appending date and time to file
import time

# Open englishwords.txt into a file
f = open("englishwords.txt", "r")

# Splitting of the file englishwords.txt into a list to make it easier to pass through
lines = []
for line in f:              
    line = line.rstrip()    
    lines.append(line)

# Remove non alpha characters module
def removepuncandig(terms):
    
    terms = terms.lower()
    translation = str.maketrans("", "", string.punctuation)
    terms = terms.translate(translation)

    terms = re.sub('£', '', terms)

    translation2 = str.maketrans("", "", string.digits)
    terms = terms.translate(translation2)
    return(terms)

# Spellchecker module
def spellchecker(words):
    words = words.split()
    i = 0
    wordsfalse = 0
    wordstrue = 0
    j = 0
    while i < len(words):
        j = 0
        while j < len(lines):
            if words[i] == lines[j]:
                if sent == True:
                    print(words[i] + " is spelt correctly.")
                else:
                    None
                i += 1
                wordstrue += 1
                break
            elif j == (len(lines) - 1):
                if sent == True:
                    print(words[i] + " not found in dictionary")
                else:
                    None
                words[i] = "?" + words[i] + "?"
                i += 1
                wordsfalse +=1
                break
            else:
                j += 1

    # Output facts about inputted sentence
    print("Number of words: " + str(len(words)))
    print("Number of correctly spelt words: " + str(wordstrue) + "/" + str(len(words)))
    print("Number of incorrectly spelt words: " + str(wordsfalse) + "/" + str(len(words)))

    print("Time elapsed: " + str(time.time() - start_time) + "s")

    if sent == False:
        incorrectfile = open("incorrectwords.txt", "w")
        incorrectfile.write(str(time.ctime()) + "\n\n")
        incorrectfile.write("\nNumber of words: " + str(len(words)))
        incorrectfile.write("\nNumber of correctly spelt words: " + str(wordstrue) + "/" + str(len(words)))
        incorrectfile.write("\nNumber of incorrectly spelt words: " + str(wordsfalse) + "/" + str(len(words)))
        words = " ".join(words)
        incorrectfile.write("\n" + words)

        incorrectfile.close()
    else:
        None
print("---------------------FREDERICK'S SPELLCHECKER PROGRAM------------------------------------------")


cont = True
while cont == True:
    sent = False
    decision = input("- Press 1 if you would like to spellcheck a file \n- Press 2 if you would like to spellcheck a sentence\n- Press 0 if you would like to quit. \n\n>>> ")
    print("\n--------------------------------------------------------------------------------")

    # Loop to spellcheck file
    if decision == "1":
        file = input("Please type the full name of the file to check (Eg 'englishwords.txt'): \n>>> ")

        start_time = time.time()

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
        sentence = input("\nPlease enter a sentence to be spell checked: \n>>> ")

        start_time = time.time()
        
        sentence = removepuncandig(sentence)

        print("Here is your entry: \n\n" + sentence  + "\n")

        # Spellcheck sentence
        spellchecker(sentence)
        

    # Error handling
    elif decision != "1" or "2" or "0":
        print("Please input a valid choice")
        continue
    # User decision to input another sentence or quit
    carryon = input("Press q [enter] to quit or any other key [enter] to go again:\n>>> ")
    if carryon == "q":
        cont = False
    else:
        cont = True

# Don't forget to close the file!!!!
f.close()

