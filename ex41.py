import random
from urllib.request import urlopen
import sys

WORD_URL = "https://learncodethehardway.org/words.txt"
WORDS = []

# Snippets to be used as flash cards
# The keys are snippets, values are phrases
PHRASES = {
    "class %%%(%%%):" :
        "Make a class named %%% that is a %%%.",
    "class %%%(object):\n\tdef __init__(self, ***)" :
        "class %%% has-a __init__ that takes self and *** parameters.",
    "class %%%(object):\n\tdef ***(self, @@@)" :
        "class %%% has-a function *** that takes self and @@@ parameters.",
    "*** = %%%():" :
        "Set *** to be an instance of class %%%.",
    "***.***(@@@)":
        "From *** get the *** function, call it with params self, J.",
    "***.*** = '***'":
        "From *** get the *** attribute and set it to ***."
}

# if "english" is the second argument, then given sentence, answer in Python Syntax
if len(sys.argv) == 2 and sys.argv[1] == "english":
    PHRASE_FIRST = True
else:
    PHRASE_FIRST = False

# load the words from the website
# and some minor processing of the words
for word in urlopen(WORD_URL).readlines(): # returns a list of bytes with \n
    WORDS.append(str(word.strip(), encoding = "utf-8"))

# convert the %%%, @@@ in a snippet to random words loaded previously
def convert(snippet, phrase):
    # Note that by design, "%%%" is a placeholder for class name
    # Note that capitalize() only capitalizes the first letter, instead of the entire word
    class_names = [w.capitalize() for w in random.sample(WORDS, snippet.count("%%%"))]
    other_names = random.sample(WORDS, snippet.count("***"))
    results = []
    param_names = []

    for i in range(0, snippet.count("@@@")):
        param_count = random.randint(1, 3) # a random integer between 1 and 3, not including 3
        param_names.append(', '.join(
            random.sample(WORDS, param_count)))

    # The first loop goes through the snippet,
    # the second loop goes through the phrase
    for sentence in snippet, phrase:
        result = sentence[:]

        # fake class names
        for word in class_names:
            result = result.replace("%%%", word, 1) # replace only the first occurence of %%%

        # fake other names
        for word in other_names:
            result = result.replace("***", word, 1)

        # fake parameter
        for word in param_names:
            result = result.replace("@@@", word, 1)

        results.append(result)

    return results

# keep going until hit CTRL-D
try:
    while True:
        # all the keys in the PHRASES dict -> list
        snippets = list(PHRASES.keys())

        # shuffle the list of snippets in place
        random.shuffle(snippets)

        for snippet in snippets:
            phrase = PHRASES[snippet]
            question, answer = convert(snippet, phrase)

            if PHRASE_FIRST: # i.e. we want given sentence, answer with Python syntax
                question, answer = answer, question

            print(question)

            input("> ")
            print("ANSWER: {} \n\n".format(answer))
except EOFError:
    print("\nBye")


