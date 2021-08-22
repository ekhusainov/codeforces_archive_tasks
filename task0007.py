import sys


def get_d(a, b, c):
    diff = abs(a - b)
    if c > diff * 2:
        return -1
    
    if diff < a and diff < b:
        return -1
    if c <= diff:
        return diff + c
    if c - diff == a or c - diff == b:
        return -1
    return c - diff

def read_data():
    data = sys.stdin.read().split("\n")
    return data[1:-1]


def main():
    data = read_data()
    answer = ""
    for i in data:
        a, b, c = map(int, i.split())
        d = str(get_d(a, b, c)) + "\n"
        answer += d 

    answer = answer[:-1]
    sys.stdout.write(answer)

if __name__ == "__main__":
    main()