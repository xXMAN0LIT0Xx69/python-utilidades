pregunta = str(input("¿Quieres codificar o decodificar? (c/d): "))
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
if pregunta.lower() == 'c':
    texto=str(input("Introduce tu texto caraculo: "))
    binario= '' .join(format(ord(c), '08b') for c in texto)

    while len(binario) % 6 != 0:
        binario += "0"
    lisalisa= []

    for a in range(0, len(binario), 6):
        lisalisa.append(binario[a:a+6])

    manolo= []

    for c in lisalisa:
        manolo.append(int(c, 2))

    base64= ''.join(alfabeto[i] for i in manolo)

    padding = (3 - len(texto) % 3) % 3
    base64 += "=" * padding

    print(base64)
else:
    trabajo = input(str("Introduce tu texto merluzo: "))
    padding = trabajo.count("=")
    trabajo = trabajo.rstrip("=")
    for c in trabajo:
        valor = alfabeto.index(c)
    
    binario = ''.join(format(alfabeto.index(c), '06b') for c in trabajo)
    if padding:
        binario = binario[:-(padding * 2)]
    texto = ''.join(chr(int(binario[i:i+8], 2)) for i in range(0, len(binario), 8))
    print(texto)
