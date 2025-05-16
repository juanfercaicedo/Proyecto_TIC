import sys

def fibonacci(userInput):
    sequence = []

    if userInput <= 0:
        return sequence
    elif userInput == 1:
        return [0]
    elif userInput == 2:
        return [0, 1]

    sequence = [0, 1]
    for i in range(2, userInput):
        next_value = sequence[i - 1] + sequence[i - 2]
        sequence.append(next_value)

    return sequence

# Lee el número desde los argumentos del sistema
try:
    if len(sys.argv) < 2:
        raise ValueError("Falta argumento")

    n = int(sys.argv[1])
    print("\nSucesión de Fibonacci:")
    print(fibonacci(n))
except ValueError:
    print("Por favor, ingrese un número entero válido.")
