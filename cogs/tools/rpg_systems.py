import random


class Cellbit:
    def __init__(self) -> None:
        pass

    def OPC(self, dano: str, x):
        valores = ''
        rolagem = dano
        val = {}
        sinais = {}
        cont = maior = menor = 0
        adi = []
        dano = dano.lower().replace(' ', '')

        for c, item in enumerate(dano):
            if not item.isalnum():
                cont += 1
                dano = dano.replace(item, ' ')
                # Salvando o sinal com seu index como chave
                sinais[cont] = item
        
        #Transformando o texto em uma lista.
        dano = dano.split()

        for c, item in enumerate(dano):
            if 'd' in item:
                print(item)
                dado = item.split('d')
                for cont in range(0, int(dado[0])):
                    gerado = random.randint(1, int(dado[1]))
                    valores += f'{cont + 1}° d{dado[1]}: {gerado}\n'
                    if cont == 0:
                        val[c] = [str(gerado)]
                        if c == 0:
                            maior = gerado
                            menor = gerado
                        else:
                            if gerado > maior:
                                maior = gerado
                            elif gerado < menor:
                                menor = gerado
                    else:
                        val[c].append(str(gerado))
                        if gerado > maior:
                            maior = gerado
                        elif gerado < menor:
                            menor = gerado
            else:
                dano[c] = 'remove'
                adi.append(str(sinais[c] if c in sinais else '') + str(item))
        
        while 'remove' in dano:
            dano.remove('remove')

        for c, item in enumerate(val.keys()):
            dano.pop(item - c)
        
        cont = 0
        for key, value in val.items():
            dano.insert(key, str(sinais[cont] if cont in sinais else '') + str(eval('+'.join((value)))))
            cont += 1
    
        for item in adi:
            dano.append(item)

        maior = str(maior)
        menor = str(menor)
        inicio = f"{rolagem.replace('*', 'x')}\n\n" + valores

        if x == 0:
            fim = "".join(dano).replace('*', 'x') + f' = {eval("".join(dano))}'
        else:
            fim = f"Maior:{maior + ''.join(adi)} = {eval(maior + ''.join(adi))} \nMenor:{menor + ''.join(adi)} = {eval(menor + ''.join(adi))} "

        return inicio + "\n" + fim
        
    def OPD(self, v, p, d=20):
        normal = d+1 - p
        bom = d+1 - p//2
        extremo = d+1 - p // 5

        if v >= normal:
            response = 'Normal'
        elif v > 1 < normal:
            response = 'Falha'
        else:
            response = 'Desastre'
        if v >= bom:
            response = 'Bom'
        if v >= extremo:
            response = 'Extremo'

        return response
