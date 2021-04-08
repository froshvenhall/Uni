# Assessment 1.2 -- SPELLCHECKER2 -- created by Frederick Hall -- due Friday 8 Nov 6pm
# Open englishwords.txt into a file

import string # For removing punctuation
import re # For removing the £ sign as is not in string.puncuation string

f = open("englishwords.txt", "r")
# Splitting of the file englishwords.txt into a list to make it easier to pass through
lines = []
for line in f:              
    line = line.rstrip()    
    lines.append(line)


    
print("---------------------FREDERICK'S SPELLCHECKER PROGRAM------------------------------------------")

# Loop to continue until user inputs q when prompted
cont = True
while cont == True:
    sentence = input("\nPlease enter a sentence to be spell checked: \n")
    
    # Remove UPPER case letters and convert to lowercase
    sentence = sentence.lower()

    # Remove PUNCUATION
    translation = str.maketrans("", "", string.punctuation)
    sentence = sentence.translate(translation)

    sentence = re.sub('£', '', sentence)

    # Remove numbers
    translation2 = str.maketrans("", "", string.digits)
    sentence = sentence.translate(translation2)

    print("Here is your entry: \n\n" + sentence  + "\n")

    words = sentence.split()

    # Loop to go through file to check for correctly spelt words
    i = 0
    wordsfalse = 0
    wordstrue = 0
    j = 0
    while i < len(words):
        j = 0
        while j < len(lines):
            if words[i] == lines[j]:
                print(words[i] + " is spelt correctly.")
                i += 1
                wordstrue += 1
                break
            elif j == (len(lines) - 1):
                print(words[i] + " not found in dictionary")
                i += 1
                wordsfalse +=1
                break
            else:
                j += 1

    # Output facts about inputted sentence
    print("Number of words: " + str(len(words)))
    print("Number of correctly spelt words: " + str(wordstrue) + "/" + str(len(words)))
    print("Number of incorrectly spelt words: " + str(wordsfalse) + "/" + str(len(words)))

    # User decision to input another sentence or quit
    carryon = input("Press q [enter] to quit or any other key [enter] to go again: ")
    if carryon == "q":
        cont = False
    else:
        cont = True

# Don't forget to close the file!!!!
f.close()
