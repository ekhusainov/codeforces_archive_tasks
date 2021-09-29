LEFT = "("
RIGHT = ")"
current_string = input()
brackets = []
answer = []
for idx, elem in enumerate(current_string):
    if elem != LEFT and elem != RIGHT:
        continue
    if elem == LEFT:
        brackets.append(idx)
    if elem == RIGHT:
        last_left = brackets.pop()
        answer.append((last_left, idx))
for position in answer:
    print(f"{position[0]}, {position [1]}")
