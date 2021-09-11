"""
Facebook Hacker Cup
Problem A1: Consistency - Chapter 1
"""

VOWELS = "AEIOU"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXYZ"
FULL_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def main():
    t = int(input())
    answer = []
    for _ in range(t):
        current_string = input()
        best_change = 1_000_000_000
        for etalon_char in FULL_ALPHABET:
            changes = 0
            for current_char in current_string:
                if current_char == etalon_char:
                    continue
                if current_char in VOWELS and etalon_char in VOWELS:
                    changes += 2
                elif current_char in CONSONANTS and etalon_char in CONSONANTS:
                    changes += 2
                else:
                    changes += 1
            best_change = min(best_change, changes)
        answer.append(best_change)
    with open("somefile_0029.txt", "a") as the_file:
        for idx, value in enumerate(answer):
            output_part = "Case #" + str(idx + 1) + ": " + str(value) + "\n"
            the_file.write(output_part)


if __name__ == "__main__":
    main()
