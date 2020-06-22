# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

import string

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithm", "her", "herself"]

negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressing", "concerning", "horrible", "horribly", "questionable"]

test_list = ['blorb', 'flork', 'chees']

def findall(text, phrase):
    i = text.find(phrase)
    while i != -1:
        yield i
        i = text.find(phrase, i+1)

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

def censor_phrase(text, phrase):
    text_casefold = text.casefold()
    phrase_casefold = phrase.casefold()
    phrase_length = len(phrase)
    start_index = text_casefold.find(phrase_casefold)        
    end_index = start_index + phrase_length
    if start_index >=0:
        text = text[:start_index] + censor(text[start_index:end_index]) + text[end_index:]
    return text

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

def censor_after_two(text, phrase_list):
    text_casefold = text.casefold()
    index_list = []
    for phrase in phrase_list:
        phrase_casefold = phrase.casefold()
        phrase_length = len(phrase)
        for start_index in findall(text_casefold, phrase_casefold):
            if start_index >= 0:
                index_list.append(start_index+phrase_length)                                    #append the end index of word if found
    index_list.sort()                                                                       #sort all of the end indices
    if index_list:
        untouched_text = text[:index_list[1]]
        censored_text = text[index_list[1]:]                                                #if elements in list, choose text to censor and leave
        censored_text_casefold = censored_text.casefold()
        for phrase in phrase_list:
            phrase_casefold = phrase.casefold()
            phrase_length = len(phrase)
            for start_index in findall(text_casefold, phrase_casefold):
                end_index = start_index + phrase_length
                if start_index > 0:
                    censored_text = censored_text[:start_index] + censor(censored_text[start_index:end_index]) + censored_text[end_index:]
        text = untouched_text + censored_text
    return text



def censor_either_side(text, phrase_list):
    text_casefold = text.casefold()
    for phrase in phrase_list:
        phrase_casefold = phrase.casefold()
        phrase_length = len(phrase)
        if phrase_casefold in text_casefold:
            for start_index in findall(text_casefold, phrase_casefold):
                end_index = start_index + phrase_length
                start_space_count = 0
                end_space_count = 0
                while start_index > 0 and start_space_count < 2:             # from start_index go backwards until previous space
                    start_index -= 1
                    if text[start_index] == ' ':
                        start_space_count += 1
                while end_index < len(text) - 1 and end_space_count < 1:     # from end_index go forwards until next space
                    end_index += 1
                    if text[end_index] == ' ':
                        end_space_count += 1
                text = text[:start_index] + censor(text[start_index:end_index]) + text[end_index:]
    return text

print(censor_phrase(email_one, 'learning algorithms'))
print(censor_from_list(email_two, proprietary_terms))
print(censor_after_two(email_three, negative_words))
print(censor_either_side(email_four, proprietary_terms + negative_words))

