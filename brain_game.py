import random
import time


def memory_challenge(level: int) -> bool:
    """Show a sequence of digits for a short time and ask user to recall."""
    length = level + 2
    seq = ''.join(str(random.randint(0, 9)) for _ in range(length))
    print(f"Remember this sequence: {seq}")
    time.sleep(0.8 + level * 0.2)
    print("\033c", end="")  # Clear screen (works in most terminals)
    guess = input("Enter the sequence: ")
    return guess.strip() == seq


def math_challenge(level: int) -> bool:
    """Simple arithmetic question."""
    a = random.randint(1, 10 + level * 2)
    b = random.randint(1, 10 + level * 2)
    op = random.choice(['+', '-', '*'])
    if op == '+':
        answer = a + b
    elif op == '-':
        answer = a - b
    else:
        answer = a * b
    guess = input(f"Solve: {a} {op} {b} = ")
    try:
        return int(guess) == answer
    except ValueError:
        return False


def pattern_challenge(level: int) -> bool:
    """Ask for next number in an arithmetic progression."""
    start = random.randint(1, 5)
    step = random.randint(1, 5)
    length = 4 + level
    seq = [start + i * step for i in range(length)]
    print("Sequence:", ' '.join(str(n) for n in seq[:-1]))
    guess = input("Next number: ")
    try:
        return int(guess) == seq[-1]
    except ValueError:
        return False


CHALLENGES = [memory_challenge, math_challenge, pattern_challenge]

def run_game(rounds: int = 5) -> None:
    score = 0
    for i in range(rounds):
        level = i // 2  # increase difficulty every two rounds
        challenge = random.choice(CHALLENGES)
        print(f"\nRound {i+1} - {challenge.__name__.replace('_', ' ').title()}")
        if challenge(level):
            print("Correct!\n")
            score += 1
        else:
            print("Incorrect.\n")
    print(f"Game over! Your score: {score}/{rounds}")


if __name__ == "__main__":
    try:
        rounds = int(input("How many rounds would you like to play? "))
    except ValueError:
        rounds = 5
    run_game(rounds)
