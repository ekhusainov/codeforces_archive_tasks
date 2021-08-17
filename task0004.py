"""
https://codeforces.com/problemset/problem/703/A
"""

MISHKA = "Mishka"
CHRIS = "Chris"
FRIENDSHIP = "Friendship is magic!^^"


def main():
    number_games = int(input())
    total_misha = 0
    total_chris = 0
    for _ in range(number_games):
        misha_v, chris_v = map(int, input().split())
        if misha_v > chris_v:
            total_misha += 1
        elif misha_v < chris_v:
            total_chris += 1

    if total_misha > total_chris:
        print(MISHKA)
    elif total_misha < total_chris:
        print(CHRIS)
    else:
        print(FRIENDSHIP)


if __name__ == "__main__":
    main()
