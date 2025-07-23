import random

def lanzar_dados(debug=False, input_func=None):
    if debug:
        while True:
            try:
                if input_func:
                    d1_str = input_func("(Debug) valor dado 1 (1-6): ")
                    d2_str = input_func("(Debug) valor dado 2 (1-6): ")
                else:
                    d1_str = input("(Debug) valor dado 1 (1-6): ")
                    d2_str = input("(Debug) valor dado 2 (1-6): ")
                
                d1 = int(d1_str)
                d2 = int(d2_str)
                
                if 1 <= d1 <= 6 and 1 <= d2 <= 6:
                    return d1, d2
                else:
                    if input_func:
                        pass
                    else:
                        print("⚠️ Valores inválidos. Usando aleatorio.")
                    return random.randint(1, 6), random.randint(1, 6)
            except ValueError:
                if input_func:
                    pass
                else:
                    print("⚠️ Valores inválidos. Usando aleatorio.")
                return random.randint(1, 6), random.randint(1, 6)
    return random.randint(1, 6), random.randint(1, 6)

def es_par(dado1, dado2):
    return dado1 == dado2
