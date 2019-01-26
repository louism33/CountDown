import time

import enchant
import random

'''
from the game countdown: pick 9 vowels / consonants, make longest word possible
'''
d = enchant.Dict("en_UK")
total_letters = 9
default_consonants = 6
game_time_limit = 30

def find_longest_word(array):
    longest_words = ["", "", ""]
    longest_words_lengths = [0, 0, 0]
    remaining_letters = array[1:]

    def iterative_deepening_search(current_word, remaining_letters):
        if d.check(current_word):
            length = len(current_word)
            if length > min(longest_words_lengths) and not current_word in longest_words:
                index = longest_words_lengths.index(min(longest_words_lengths))
                longest_words[index] = current_word
                longest_words_lengths[index] = length

                # print(longest_words)
                # print(longest_words_lengths)

        for l in range(len(remaining_letters)):
            rem = remaining_letters[:l]
            rem += (remaining_letters[l + 1:])
            iterative_deepening_search(current_word + remaining_letters[l], rem)

    for l in range(len(array)):
        rem = remaining_letters[:l]
        rem += (remaining_letters[l + 1:])
        iterative_deepening_search(array[l], remaining_letters=rem)

    return longest_words, longest_words_lengths


def random_consonant():
    return "bcdfghjklmnpqrstvwxyz"[random.randint(0, 20)]


def random_vowel():
    return "aeiou"[random.randint(0, 4)]


def get_random_numbers(c):
    global total_numbers
    v = total_letters - c

    vowels = []
    for i in range(v):
        vowels.append(random_vowel())

    consonants = []
    for i in range(c):
        consonants.append(random_consonant())

    all_letters = []
    all_letters.extend(consonants)
    all_letters.extend(vowels)
    return all_letters

def main():
    global total_letters, default_consonants
    n = input("Out of %d, how many consonants do you want (default is %d)?\n" % (total_letters, default_consonants)) or default_consonants
    try:
        number_of_consonants = int(n)
        if number_of_consonants < 0 or number_of_consonants > total_letters:
            print("illegal number, defaulting to %d consonants" % default_consonants)
    except ValueError:
        print("could not read your input, defaulting to %d consonants" % default_consonants)
        number_of_consonants = default_consonants

    print("generating %d consonant(s) and %d vowel(s)" % (number_of_consonants, (total_letters - number_of_consonants)))
    time.sleep(2)
    arr = get_random_numbers(number_of_consonants)
    s = "".join(x for x in arr)
    print("your letters are: " + " ".join(random.sample(s, len(s))).upper())

    time.sleep(6)
    print("ready?")
    time.sleep(2)

    print("you have %d seconds, go!" % game_time_limit)

    for i in range(game_time_limit, 0, -1):
        print("%d seconds left" % i)
        time.sleep(1)

    print("time's up!")
    time.sleep(2)
    print("how did you do?")
    time.sleep(2)

    print("let me see if what I can find...")
    best_words, best_words_length = find_longest_word(arr)

    print("The three best words I found had lengths:\n" + str(best_words_length))
    time.sleep(3)
    print("these words are:\n" + str(", ".join(x for x in best_words)))
    time.sleep(2)

    a = input("Do you want to play again (with different numbers)? [Y/n]\n") or "y"

    if a == 'y' or a == 'y':
        main()
    else:
        print("bye bye!")
        exit(0)


main()

