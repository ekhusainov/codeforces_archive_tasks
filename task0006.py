MAX_V = 1000

def read_data():
    n = int(input())
    values = []
    for _ in range(n):
        values.append(int(input()))
    return n, values


def main():
    n, values = read_data()
    polycarp_values = []
    current_value = 0
    for _ in range(MAX_V):
        while 1:
            current_value += 1
            if current_value % 3 == 0 or str(current_value)[-1] == "3":
                continue
            else:
                polycarp_values.append(current_value)
                break
    for v in values:
        print(polycarp_values[v - 1])

    
if __name__ == "__main__":
    main()
