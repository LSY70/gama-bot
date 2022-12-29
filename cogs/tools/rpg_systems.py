class Cellbit:

    def OPC(self, dano: str, x):
        try:
            import random
            valores = ''
            rolagem = dano
            val = {}
            sinais = {}
            qtd = cont = maior = menor = 0
            adi = []
            dano = dano.replace(' ', '')

            #Troca de sinais por ","
            for c, item in enumerate(dano):
                if not item.isalnum():
                    if c != 0:
                        #o cont aqui é usado para definir o index do sinal
                        cont += 1
                        dano = dano.replace(item, ',')
                    else:
                        dano = dano[1:]
                    # Aqui salvei o sinal em seu index
                    sinais[cont] = item
            
            #Transformando o texto em uma lista.
            dano = dano.split(',')

            #Rolagem dos dados
            for c, item in enumerate(dano):
                if 'd' in item:
                    #qtd é usado para previnir um bug no caso de x=1 e existe mais de um dado na rolagem.
                    qtd += 1
                    #lista que separa o item de "3d10" para "3, 10", sendo o primeiro número quantidade e o segundo faces 
                    dado = item.split('d')
                    for cont in range(0, int(dado[0])):
                        gerado = random.randint(1, int(dado[1]))
                        valores += f'{cont + 1}° d{dado[1]}: {gerado}\n'
                        if cont == 0:
                            val[c] = [str(gerado)]
                            if qtd == 1:
                                maior = gerado
                                menor = gerado
                        else:
                            if qtd == 1:
                                if gerado > maior:
                                    maior = gerado
                                elif gerado < menor:
                                    menor = gerado
                            val[c].append(str(gerado))
                else:
                    #remove item do dano e adiciona á variavel adi
                    dano.remove(item)
                    adi.append(str(sinais[c] if c in sinais else '') + str(item))
            
            for c, item in enumerate(val.keys()):
                dano.pop(item - c)
            
            #este laço insere os dados dentro da variavel dano
            cont = 0
            for key, value in val.items():
                dano.insert(key, str(sinais[cont] if cont in sinais else '') + str(eval('+'.join((value)))))
                cont += 1

            for item in adi:
                dano.append(item)

            maior = str(maior)
            menor = str(menor)
            inicio = f"{rolagem.replace('*', 'x')}\n\n" + valores + "\n"
            fim = ["".join(dano).replace('*', 'x') + f' = {eval("".join(dano))}', f"Maior:{maior + ''.join(adi)} = {eval(maior + ''.join(adi))} \nMenor:{menor + ''.join(adi)} = {eval(menor + ''.join(adi))} "]
            return inicio + fim[x]
        except Exception as error:
            return f'Erro: {error}'
        
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
