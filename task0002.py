"""
https://codeforces.com/problemset/problem/71/A
"""

MAX_LEN_WORD = 10

def k8s_like(word):
    first_char = word[0]
    last_char = word[-1]
    middle_number = str(len(word) - 2)
    return first_char + middle_number + last_char

def main():
    number_input = int(input())
    words = []
    for _ in range(number_input):
        words.append(input())

    answer_words = []
    for current_word in words:
        if len(current_word) <= MAX_LEN_WORD:
            answer_words.append(current_word)
        else:
            answer_words.append(k8s_like(current_word))
    
    for i in answer_words:
        print(i)


if __name__ == "__main__":
    main()
