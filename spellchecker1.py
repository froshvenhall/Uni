# Assessment 1.1 -- SPELLCHECKER1-- created by Frederick Hall -- due Friday 8 Nov 6pm
# Open englishwords.txt into a file
f = open("englishwords.txt", "r")

print("---------------------FREDERICK'S SPELLCHECKER PROGRAM------------------------------------------")

sentence = input(str("\nPlease enter a sentence to be spell checked: \n"))

words = sentence.split()
lines = []

# Splitting of the file englishwords.txt into a list to make it easier to pass through
for line in f:              
    line = line.rstrip()    
    lines.append(line)

# Loop to go through file to check for correctly spelt words
i = 0
while i < len(words):
    j = 0
    while j < len(lines):
        if words[i] == lines[j]:
            print(words[i] + " is spelt correctly.")
            i += 1
            break
        elif j == (len(lines) - 1):
            print(words[i] + " not found in dictionary")
            i += 1
            break
        else:
            j += 1
    
# Don't forget to close the file!!!!
f.close()
