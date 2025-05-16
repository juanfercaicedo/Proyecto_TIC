def fibonacci_series(length):
    if length <= 0:
        return []
    elif length == 1:
        return [0]
    elif length == 2:
        return [0, 1]

    series = [0, 1]
    for _ in range(2, length):
        series.append(series[-1] + series[-2])
    return series

def main():
    try:
        n = int(input("Ingrese la longitud de la serie de Fibonacci: "))
        series = fibonacci_series(n)
        print("Serie de Fibonacci:", series)
    except ValueError:
        print("Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    main()
