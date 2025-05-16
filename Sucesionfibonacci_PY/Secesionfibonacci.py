def fibonacci(n):
    sequence = []

    if n <= 0:
        return sequence
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    sequence = [0, 1]
    for i in range(2, n):
        next_value = sequence[i - 1] + sequence[i - 2]
        sequence.append(next_value)

    return sequence

# Solicita el número de términos al usuario
try:
    n = int(input("Ingrese la cantidad de términos de la sucesión de Fibonacci: "))

    print("\nSucesión de Fibonacci:")
    print(fibonacci(n))
except ValueError:
    print("Por favor, ingrese un número entero válido.")
