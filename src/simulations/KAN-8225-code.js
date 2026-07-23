def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

if __name__ == "__main__":
    try:
        input_n = int(input("Digite um número inteiro para calcular o fatorial: "))
        fact = factorial(input_n)
        print(f"O fatorial de {input_n} é: {fact}")
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")