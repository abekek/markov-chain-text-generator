'''
@author: Alibek Kaliyev
'''

import random
from collections import Counter

# reading the file
filename = input("Please, enter the name of a file: ")
file = open(filename, "r", encoding="utf-8")


# preprocessing the corpus
def text_preprocessing():

    # extracting tokens
    tokens = []
    for line in file:
        line_tokens = line.split()
        for token in line_tokens:
            tokens.append(token)

    # creating trigrams
    trigrams = []
    for i in range(len(tokens) - 2):
        trigrams.append([tokens[i], tokens[i + 1], tokens[i + 2]])

    # dictionary of trigrams with head and tail
    dict = {}
    for trigram in trigrams:
        dict.setdefault(trigram[0] + ' ' + trigram[1], []).append(trigram[2])

    # sorted dictionary by frequency
    freq_dict = {}
    for key in dict:
        freq_counter = Counter(dict[key])
        freq_dict[key] = freq_counter.most_common()

    return freq_dict, trigrams


# finction to generate a text
def sentence_generator(word_, freq_dict, trigram):
    sent_ = [word_]
    word_ = trigram[1] + ' ' + trigram[2]
    text_length = 2
    while True:
        curr_word = word_.split(' ')[-1]
        next_word = freq_dict[word_][0][0]
        if curr_word.endswith(('.', '!', '?')) and text_length >= 4:
            sent_.append(curr_word)
            return sent_
        if next_word.endswith(('.', '!', '?')) and text_length >= 3:
            sent_.append(curr_word + ' ' + next_word)
            return sent_
        sent_.append(curr_word + ' ' + next_word)
        text_length += 2
        next_next_word = freq_dict[curr_word + ' ' + next_word][0][0]
        if next_next_word.endswith(('.', '!', '?')) and text_length >= 4:
            sent_.append(next_next_word)
            return sent_
        word_ = next_word + ' ' + next_next_word
    return sent_


# function to get first two words (randomly)
def get_first_head(trigram, trigrams):
    first_head = trigram[0] + ' ' + trigram[1]
    while trigram[0].islower() or trigram[0].endswith(('.', '!', '?')):
        trigram = random.choice(trigrams)
        first_head = trigram[0] + ' ' + trigram[1]
    return first_head, trigram


# results
print('Generated text')
freq_dict, trigrams = text_preprocessing()
for i in range(10):
    trigram = random.choice(trigrams)
    start_head, trigram = get_first_head(trigram, trigrams)
    sentence = sentence_generator(start_head, freq_dict, trigram)
    print(' '.join(sentence))
