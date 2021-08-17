"""
https://codeforces.com/problemset/problem/4/A
"""


def main():
    kilogram = int(input())
    if kilogram % 2 or kilogram == 2:
        print("NO")
    else:
        print("YES")


if __name__ == "__main__":
    main()
