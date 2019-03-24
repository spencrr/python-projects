import random
with open('words_alpha.txt') as word_file:
    words = word_file.read().split()
    while True:
        times = int(input())
        length = int(input())
        count = 0
        for _ in range(len(words)):
            word = words[random.randint(0, len(words) - 1)]
            if len(word) == length:
                print(word)
                count += 1
            if count == times:
                break
        