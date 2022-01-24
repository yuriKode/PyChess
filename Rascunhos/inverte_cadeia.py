def inverte(cadeia):
    nova_cadeia = str()
    for i in reversed(range(0, len(cadeia))):
        nova_cadeia += cadeia[i]
    return nova_cadeia

inverte("Mamãe é maluca");

def isPalidromo(cadeia):
    cadeia_invertida = inverte(cadeia)
    if(cadeia == cadeia_invertida):
        return True
    return False

print(isPalidromo("relógio"))
print(isPalidromo("radar"))
print(isPalidromo("carro"))

def superposicion(cadeia1, cadeia2):
    for i in range(len(cadeia1)):
        for j in range(len(cadeia2)):
            if(cadeia1[i] == cadeia2[j]):
                return True
    return False

print(superposicion("teste", "amtdor"))

def generar_n_caracteres(n = int(), caractere = str()):
    nova_cadeia = str()
    for i in range(n):
        nova_cadeia += caractere
    print(nova_cadeia)

generar_n_caracteres(7, "x")


def histogram(array = []):
    for i in range(len(array)):
        for j in range(array[i]):
            print(".", end = "")
        print()

histogram([2,3,4,7])

    