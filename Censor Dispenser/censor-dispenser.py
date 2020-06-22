# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

import string

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithm", "her", "herself"]

negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressing", "concerning", "horrible", "horribly", "questionable"]

test_list = ['blorb', 'flork', 'chees']


# Generator function to find every occurrence of a given phrase:

def findall(text, phrase, check_end = False):                                                       # Last flag optional toggle to disregard whether the term makes a whole word
    phrase_length = len(phrase)
    i = text.find(phrase)                                                                             
    while i != -1:                                                                                  # If phrase found:
        if check_end == True:
            phrase_end = text[i+phrase_length] 
            if phrase_end in string.punctuation or phrase_end == ' ' or phrase_end == '\n':         # Check to make sure it's a whole word (i.e. with punctuation or whitespace after)
                yield i                                                                             # Add to the iterator
        else:
            yield i
        i = text.find(phrase, i+1)                                                                  # Next time, search after the found phrase

# Base censor function to replace all non-punctutation/whitespace characters with '#'

def censor(text):
    new_text = ''
    for c in text:
        if c == ' ':
            new_text += ' '
        elif c == '\n':
            new_text += '\n'
        elif c in string.punctuation:
            new_text += c
        else:
            new_text += '#'
    return new_text

# Function 1 - Censor a given phrase from text

def censor_phrase(text, phrase):
    text_casefold = text.casefold()                                                                 # Ignore case of text and phrase
    phrase_casefold = phrase.casefold()
    phrase_length = len(phrase)
    for start_index in findall(text_casefold, phrase_casefold):                                     # Locate each instance of phrase
        end_index = start_index + phrase_length                                                   
        if start_index >=0:
            text = text[:start_index] + censor(text[start_index:end_index]) + text[end_index:]      # Replace phrase using censor function
    return text

# Function 2 - Censor all phrases in given list from text

def censor_from_list(text, phrase_list):
    text_casefold = text.casefold()
    for phrase in phrase_list:
        phrase_casefold = phrase.casefold()
        phrase_length = len(phrase)
        for start_index in findall(text_casefold, phrase_casefold):
            end_index = start_index + phrase_length                                          
            if start_index >=0:
                text = text[:start_index] + censor(text[start_index:end_index]) + text[end_index:]
    return text

# Function 3 - Censor all phrases in given list from text, AFTER the first two occurrences of any phrase

def censor_after_two(text, phrase_list):
    text_casefold = text.casefold()
    index_list = []
    for phrase in phrase_list:                                                                      # First pass to find each phrase in the text
        phrase_casefold = phrase.casefold()
        phrase_length = len(phrase)
        for start_index in findall(text_casefold, phrase_casefold):
            if start_index >= 0:
                index_list.append(start_index+phrase_length)                                        # Append the end index of phrase if found
    index_list.sort()                                                                               # Sort all of the end indices
    if index_list:                                                                                  # If there are any phrases in the text:
        untouched_text = text[:index_list[1]]                                                       # Decide which text to leave behind
        censored_text = text[index_list[1]:]                                                        # And which to censor
        censored_text_casefold = censored_text.casefold()
        for phrase in phrase_list:
            phrase_casefold = phrase.casefold()
            phrase_length = len(phrase)
            for start_index in findall(censored_text_casefold, phrase_casefold):                    
                end_index = start_index + phrase_length                                    
                if start_index > 0:
                    censored_text = censored_text[:start_index] + censor(censored_text[start_index:end_index]) + censored_text[end_index:]
        text = untouched_text + censored_text
    return text

# Function 4 - Censor all phrases in fiven list from text, AND each word either side of the phrase

def censor_either_side(text, phrase_list):
    text_casefold = text.casefold()
    for phrase in phrase_list:
        phrase_casefold = phrase.casefold()
        phrase_length = len(phrase)
        if phrase_casefold in text_casefold:
            for start_index in findall(text_casefold, phrase_casefold, True):                       # Don't catch words within words
                end_index = start_index + phrase_length                                           
                start_space_count = 0                                                               # Initialise start and end space count
                end_space_count = 0
                while start_index > 0 and start_space_count < 2:                                    # From start_index, go backwards until two spaces are found (the space before our target word, and the space before the word before that...)
                    start_index -= 1
                    if text[start_index] == ' ':
                        start_space_count += 1
                while end_index < len(text) - 1 and end_space_count < 1:                            # From end_index, go forwards until two spaces are found (the space after our target word, and the space after the word after that...)
                    end_index += 1
                    if text[end_index] == ' ':
                        end_space_count += 1
                text = text[:start_index] + censor(text[start_index:end_index]) + text[end_index:]
    return text

# print(censor_phrase(email_one, 'learning algorithms'))
# print(censor_from_list(email_two, proprietary_terms))
# print(censor_after_two(email_three, negative_words))
# print(censor_either_side(email_four, proprietary_terms + negative_words))
def function_choice():
    user_choice = input('''
    Choose from the four test functions:
    1 Censor a given phrase from text
    2 Censor all phrases in given list from text
    3 Censor all phrases in given list from text, AFTER the first two occurrences of any phrase
    4 Censor all phrases in given list from text, AND each word either side of the phrase
    \n''')
    if user_choice == '1':
        print('\n', censor_phrase(choose_email(), 'learning algorithm'))
    elif user_choice == '2':
        print('\n', censor_from_list(choose_email(), proprietary_terms))
    elif user_choice == '3':
        print('\n', censor_after_two(choose_email(), negative_words))
    elif user_choice == '4':
        print('\n', censor_either_side(choose_email(), proprietary_terms + negative_words))

def choose_email():
    user_choice = input('''
    Select sample text to censor:
    1 Email one
    2 Email two
    3 Email three
    4 Email four
    \n''')
    if user_choice == '1':
        return email_one
    elif user_choice == '2':
        return email_two
    elif user_choice == '3':
        return email_three
    elif user_choice == '4':
        return email_four
    else:
        choose_email()

function_choice()

