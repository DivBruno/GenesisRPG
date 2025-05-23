from idlelib.iomenu import encoding
from random import randint
from time import sleep
from colorama import Fore, Style

ficha = False
ficha_1 = {"player": "", "name": "", "level": 1, "attributes point": 0,
           "attributes": {"strength": 1,
                          "agility": 1,
                          "dexterity": 1,
                          "endurance": 1,
                          "spirit": 1,
                          "perception": 1,
                          "intelligence": 1,
                          "charisma": 1},
           "skills": {
               "strength": {"athletics": 0,
                            "fighting": 0,
                            "weapons heavy": 0,
                            "weapons light": 0,
                            "throwing": 0},
               "agility": {"reflex": 0,
                           "stealth": 0,
                           "acrobatics": 0},
               "dexterity": {"mounting": 0,
                             "aiming": 0,
                             "lockpicking": 0,
                             "pickpocket": 0},
               "endurance": {"breath": 0,
                             "tolerance": 0,
                             "defending": 0, },
               "spirit": {"channeling": 0,
                          "summon": 0,
                          "transmutation": 0,
                          "magic senses": 0},
               "perception": {"insight": 0,
                              "investigation": 0},
               "intelligence": {"memory": 0,
                                "logic": 0,
                                "wisdom": 0,
                                "knowledge": 0},
               "charisma": {"domesticate": 0,
                            "manipulation": 0,
                            "intimidation": 0,
                            "diplomacy": 0,
                            "performance": 0,
                            "seduction": 0}
           },
           "race": "", "background": "", "situation": "Alive/Healthy"}
ficha_2 = {"HP": 0, "SP": 0, "speed": 0, "armor": 0, "resistance": 0, "slots": []}
ficha_3 = {"annotation": "", "magic": [], "ability": [], "weight": 0, "inventory": [], "lore": ""}
using_weight = 0
skill_points = 0
hp_atual = ficha_2["HP"]
sp_atual = ficha_2["SP"]
favorites = {}
# favorites order = "number": [sides / modifier / number of rolls]
# slots order = "name": [roll, effect/damage]
# magic order = "name": [roll, effect/damage]
# ability oroder = "name": [roll, effect/damage]
# inventory order = "name": [weight, value, extra info, quantity]
modificador = [{"imperito": -1}, {"aprendiz": 1}, {"adepto": 3}, {"mestre": 5}]
cores = [Fore.RED, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.LIGHTCYAN_EX, Fore.CYAN, Fore.LIGHTBLUE_EX]


# A way to test the type of success, a unique mechanic from our system
def success(dice, mod, cd):
    soma = dice + mod - abs(cd)
    result = ''
    if dice == 1:
        result = 'Fracasso Extremo'
    elif dice == 20:
        result = 'Sucesso Extremo'
    elif soma <= -10:
        result = 'Fracasso Crítico'
    elif -9 <= soma <= -1:
        result = 'Fracasso'
    elif 9 >= soma >= 0:
        result = 'Sucesso'
    elif soma >= 10:
        result = 'Sucesso Crítico'
    return result


# Some attributes have scaling, mostly of these have the same equation, and this function calculate it
def escalonamento(base, meio, maximo, aumento_i, aumento_f, nivel):
    if 11 > nivel:
        atributo = base + ((nivel - 1) // 2 * aumento_i)
    elif 20 > nivel >= 11:
        atributo = meio
        atributo += ((nivel - 11) // 3 + 1) * aumento_f
    else:
        atributo = maximo

    return atributo


# As the name says, validate if something is "integerable"
def validate_integer(user_input):
    try:
        int(user_input)
    except:
        pass
    else:
        return True


# calculates some status evolution
def evolve_status(status, level_pre_evo):
    if status == "HP":
        hp_antes = escalonamento(8, 32, 48, 6, 4, level_pre_evo)
        hp_agora = escalonamento(8, 32, 48, 6, 4, ficha_1["attributes"]["endurance"])
        aumento = hp_agora - hp_antes
        return aumento
    elif status == "SP":
        sp_antes = escalonamento(4, 20, 28, 4, 2, level_pre_evo)
        sp_agora = escalonamento(4, 20, 28, 4, 2, ficha_1["attributes"]["spirit"])
        aumento = sp_agora - sp_antes
        return aumento
    elif status == "speed":
        speed_antes = escalonamento(3, 11, 15, 2, 1, level_pre_evo)
        speed_agora = escalonamento(3, 11, 15, 2, 1, ficha_1["attributes"]["agility"])
        aumento = speed_agora - speed_antes
        return aumento
    elif status == "weight":
        weight_antes = escalonamento(10, 34, 50, 6, 4, level_pre_evo)
        weight_agora = escalonamento(10, 34, 50, 6, 4, ficha_1["attributes"]["strength"])
        aumento = weight_agora - weight_antes
        return aumento
    elif status == "HP2":
        hp_antes = escalonamento(0, 4, 8, 1, 1, level_pre_evo)
        hp_agora = escalonamento(0, 4, 8, 1, 1, ficha_1["level"])
        aumento = hp_agora - hp_antes
        return aumento


# calculates the hp gain per level
def hp_per_level(num_rolls, dice):
    aumento_total = 0
    for x in range(num_rolls):
        aumento = randint(1, dice)
        print("-" * 30)
        print(f"{x + 1}° dado:", end = " ")
        sleep(2)
        print(aumento)
        print("-" * 30)
        # a one chance re-roll
        while True:
            escolha = input("Deseja rejogar o dado?\n1 - SIM\n2 - NÃO\n")
            if escolha == "1":
                aumento = randint(1, dice)
                print("-" * 30)
                print(f"{x + 1}° dado rejogado:", end = " ")
                sleep(1)
                print(aumento)
                break
            elif escolha == "2":
                break
            else:
                print("Escolha inválida, tente novamente.")
        aumento_total += aumento
    return aumento_total


# save the variables
def salvar():
    # saving basics
    with open("dados/basics.txt", "w", encoding="utf-8") as f:
        salvante = []
        for item, valor in ficha_1.items():
            if item == "attributes" or item == "skills":
                pass
            else:
                if validate_integer(valor) == True:
                    valor = str(valor)
                salvante.append(valor)
        f.write("#".join(salvante))
    # saving attributes
    with open("dados/attributes.txt", "w", encoding="utf-8") as f:
        salvante = []
        # making attributes usable in write
        lista_atributo = []
        for x in ficha_1["attributes"].values():
            lista_atributo.append(str(x))
        f.write("#".join(lista_atributo))
    # saving skills
    with open("dados/skills.txt", "w", encoding="utf-8") as f:
        salvante = []
        # making skills usable in write
        lista_pericia = []
        for x in ficha_1["skills"].keys():
            for y, z in ficha_1["skills"][x].items():
                lista_pericia.append(str(z))
        f.write("#".join(lista_pericia))
    # saving status
    with open("dados/status.txt", "w", encoding="utf-8") as f:
        salvante = []
        for item, valor in ficha_2.items():
            if item == "slots":
                pass
            else:
                if validate_integer(valor) == True:
                    valor = str(valor)
                salvante.append(valor)
        f.write("#".join(salvante))
    # saving slots
    with open("dados/slots.txt", "w", encoding="utf-8") as f:
        # slots order = "name": [roll, effect/damage]
        lista_slots = []
        for slots in ficha_2["slots"]:
            for nome, detalhes in slots.items():
                lista_slots.append(nome)
                for x in detalhes:
                    lista_slots.append(x)
        f.write("#".join(lista_slots))
    # saving others
    with open("dados/others.txt", "w", encoding="utf-8") as f:
        salvante = []
        for item, valor in ficha_3.items():
            if item == "annotation" or item == "weight" or item == "lore":
                salvante.append(str(valor))
        f.write("#".join(salvante))
    # saving magic
    with open("dados/magic.txt", "w", encoding="utf-8") as f:
        # magic order = "name": [roll, effect/damage]
        lista_magias = []
        for magias in ficha_3["magic"]:
            for nome, detalhes in magias.items():
                lista_magias.append(nome)
                for x in detalhes:
                    lista_magias.append(x)
        f.write("#".join(lista_magias))
    # saving ability
    with open("dados/ability.txt", "w", encoding="utf-8") as f:
        # ability oroder = "name": [roll, effect/damage]
        lista_habilid = []
        for habilidades in ficha_3["ability"]:
            for nome, detalhes in habilidades.items():
                lista_habilid.append(nome)
                for x in detalhes:
                    lista_habilid.append(x)
        f.write("#".join(lista_habilid))
    # saving inventory
    with open("dados/inventory.txt", "w", encoding="utf-8") as f:
        # inventory order = "name": [weight, value, extra info, quantity]
        lista_itens = []
        for habilidades in ficha_3["inventory"]:
            for nome, detalhes in habilidades.items():
                lista_itens.append(nome)
                for x in detalhes:
                    lista_itens.append(str(x))
        f.write("#".join(lista_itens))
    # saving favorites rolls
    with open("dados/favorites.txt", "w", encoding="utf-8") as f:
        # favorites order = "number": [sides / modifier / number of rolls]
        lista_favorites = []
        for fav, detalhes in favorites.items():
            lista_favorites.append(str(fav))
            for x in detalhes:
                lista_favorites.append(str(x))
        f.write("#".join(lista_favorites))
    # saving some extra things
    with open("dados/extra.txt", "w", encoding="utf-8") as f:
        lista_extras = [str(hp_atual), str(sp_atual), str(skill_points), str(using_weight), str(ficha)]
        f.write("#".join(lista_extras))

# load the variables
def carregar():
    with open("dados/basics.txt", "r", encoding="utf-8") as f:
        for valor in f:
            cont = 0
            for x in ficha_1:
                if x == "attributes" or x == "skills":
                    continue
                else:
                    ficha_1[x] = valor.split("#")[cont]
                    ficha_1[x] = convert(ficha_1[x])
                    cont += 1
    with open("dados/attributes.txt", "r", encoding="utf-8") as f:
        cont = 0
        for valor in f:
            for x in ficha_1["attributes"]:
                ficha_1["attributes"][x] = valor.split("#")[cont]
                ficha_1["attributes"][x] = convert(ficha_1["attributes"][x])
                cont+=1
    with open("dados/skills.txt", "r", encoding="utf-8") as f:
        cont = 0
        for valor in f:
            for x in ficha_1["skills"]:
                for y,z in ficha_1["skills"][x].items():
                    ficha_1["skills"][x][y] = valor.split("#")[cont]
                    ficha_1["skills"][x][y] = convert(ficha_1["skills"][x][y])
                    cont+=1
    with open("dados/status.txt", "r", encoding="utf-8") as f:
        cont = 0
        for valor in f:
            for status in ficha_2:
                if status == "slots":
                    continue
                else:
                    ficha_2[status] = valor.split("#")[cont]
                    ficha_2[status] = convert(ficha_2[status])
                    cont+=1
    with open("dados/slots.txt", "r", encoding="utf-8") as f:
        cont = 0
        lista_favoritos = []
        ficha_2["slots"] = []
        for valor in f:
            lista_temporaria = valor.split("#")
            for x in range(len(lista_temporaria)):
                if cont % 3 == 0:
                    lista_favoritos.append(lista_temporaria[cont:cont + 3])
                cont += 1
        for x in range(len(lista_favoritos)):
            ficha_2["slots"].append({lista_favoritos[x][0]: [lista_favoritos[x][1], lista_favoritos[x][2]]})
    with open("dados/others.txt", "r", encoding="utf-8") as f:
        for valor in f:
            cont = 0
            for others in ficha_3:
                if others == "annotation" or others == "weight" or others == "lore":
                    ficha_3[others] = valor.split("#")[cont]
                    ficha_3[others] = convert( ficha_3[others])
                    cont+=1
    with open("dados/magic.txt", "r", encoding="utf-8") as f:
        cont = 0
        lista_favoritos = []
        ficha_3["magic"] = []
        for valor in f:
            lista_temporaria = valor.split("#")
            for x in range(len(lista_temporaria)):
                if cont % 3 == 0:
                    lista_favoritos.append(lista_temporaria[cont:cont + 3])
                cont += 1
        for x in range(len(lista_favoritos)):
            ficha_3["magic"].append({lista_favoritos[x][0]: [lista_favoritos[x][1], lista_favoritos[x][2]]})
    with open("dados/ability.txt", "r", encoding="utf-8") as f:
        cont = 0
        lista_habilidad = []
        ficha_3["ability"] = []
        for valor in f:
            lista_temporaria = valor.split("#")
            for x in range(len(lista_temporaria)):
                if cont % 3 == 0:
                    lista_habilidad.append(lista_temporaria[cont:cont + 3])
                cont += 1
        for x in range(len(lista_habilidad)):
            ficha_3["ability"].append({lista_habilidad[x][0]: [lista_habilidad[x][1], lista_habilidad[x][2]]})
    with open("dados/inventory.txt", "r", encoding="utf-8") as f:
        cont = 0
        lista_inventario = []
        ficha_3["inventory"] = []
        for valor in f:
            lista_temporaria = valor.split("#")
            for x in range(len(lista_temporaria)):
                if cont % 5 == 0:
                    lista_inventario.append(lista_temporaria[cont:cont + 5])
                cont += 1
        for x in range(len(lista_inventario)):
            ficha_3["inventory"].append({lista_inventario[x][0]: [lista_inventario[x][1], lista_inventario[x][2], lista_inventario[x][3],lista_inventario[x][4]]})
            for nome in ficha_3["inventory"][x]:
                cont = 0
                for detalhe in ficha_3["inventory"][x][nome]:
                    ficha_3["inventory"][x][nome][cont] = convert(detalhe)
                    cont += 1
    with open("dados/favorites.txt", "r", encoding="utf-8") as f:
        cont = 0
        lista_favoritos = []
        for valor in f:
            lista_temporaria = valor.split("#")
            for x in range(len(lista_temporaria)):
                if cont%4 == 0:
                    lista_favoritos.append(lista_temporaria[cont:cont+4])
                cont += 1
        for x in range(len(lista_favoritos)):
            lista_favoritos[x][0] = convert(lista_favoritos[x][0])
            favorites[lista_favoritos[x][0]] = [lista_favoritos[x][1], lista_favoritos[x][2], lista_favoritos[x][3]]
        for dado in favorites:
            cont = 0
            for detalhe in favorites[dado]:
                favorites[dado][cont] = convert(detalhe)
                cont += 1
    with open("dados/extra.txt", "r", encoding="utf-8") as f:
        global hp_atual, sp_atual, skill_points, using_weight, ficha
        for valor in f:
            hp_atual, sp_atual, skill_points, using_weight, ficha = valor.split("#")
            hp_atual = convert(hp_atual)
            sp_atual = convert(sp_atual)
            skill_points = convert(skill_points)
            using_weight = convert(using_weight)
            ficha = bool(ficha)


    """print("ficha 1:", ficha_1)
    print()
    print("ficha 2:", ficha_2)
    print()
    print("ficha 3:", ficha_3)
    print()
    print("favoritos:", favorites)
    print()
    print("extras:", [hp_atual, sp_atual, skill_points, using_weight, ficha])"""

# convert STR to INT, used in load variables
def convert(valor):
    if validate_integer(valor) == True:
        valor = int(valor)
    return valor

#validate the input
def teste_val(opt, min = 0, max = 0):
    while True:
        if validate_integer(opt) == True:
            opt = int(opt)
            if min == max == 0:
                return opt
            else:
                if opt < min or opt > max:
                    print("Opção inválida, tente novamente")
                    opt = input("Escolha sua opção: ")
                else:
                    return opt
        else:
            print("Opção inválida, tente novamente")
            opt = input("Escolha sua opção: ")

def dice_roll():
    while True:
        result = []
        total = 0
        print("=" * 30)
        print("Rolagem de dados - Genesis")
        print("-" * 30)
        print("1 - Rolagem rápida (dados pré-definidos)")
        print("2 - Rolagem customizada")
        print("3 - Rolagem de teste")
        print("4 - Favoritar")
        print("5 - sair")
        print("-" * 30)
        ans = input("Escolha sua opção: ")

        # validate the input
        ans = teste_val(ans, 1, 5)
        """while True:
            if validate_integer(ans) == True:
                ans = int(ans)
                if ans < 1 or ans > 5:
                    print("Opção inválida, tente novamente")
                    ans = input("Escolha sua opção: ")
                else:
                    break
            else:
                print("Opção inválida, tente novamente")
                ans = input("Escolha sua opção: ")"""

        # fast roll
        if ans == 1:
            # some predef dices
            basic_rolls = [2, 3, 4, 6, 8, 10, 12, 20, 100]
            cont = 0

            print("=" * 30)

            # printing predef dices
            print("Rolagens pré-definidas:")
            for x in basic_rolls:
                cont += 1
                print(f"{cont} - d{x}", end=" | ")
            print()  # just to correct "end"

            # printing favorite dices
            print("Rolagens favoritadas: ")
            for x, y in favorites.items():
                if y[2] <= 0:
                    print(f"{x} - d{y[0]}+{y[1]}", end=' | ')
                else:
                    print(f"{x} - {y[2]}d{y[0]} + {y[1]}", end=" | ")
            print()  # just to correct "end"

            print("=" * 30)

            # choose an option
            ans = input("Escolha sua opção: (0 para cancelar) ")

            # validate the input
            if favorites == {}:
                ans = teste_val(ans, 0, 9)
            else:
                ans = teste_val(ans, 0, max(favorites))
            """while True:
                if validate_integer(ans) == True:
                    ans = int(ans)
                    if favorites == {}:
                        if ans < 0 or ans > 9:
                            print("Opção inválida, tente novamente")
                            ans = input("Escolha sua opção: (0 para cancelar) ")
                        else:
                            break
                    else:
                        if ans < 0 or ans > max(favorites):
                            print("Opção inválida, tente novamente")
                            ans = input("Escolha sua opção: (0 para cancelar) ")
                        else:
                            break
                else:
                    print("Opção inválida, tente novamente")
                    ans = input("Escolha sua opção: (0 para cancelar) ")
            """
            # cancel, back to main menu
            if ans == 0:
                break

            # Using basic rolls
            if 9 >= ans >= 1:
                # choose the roll/modifier quantities
                quant = input("Digite a quantidade de rolagens: ")
                mod = input("Digite a quantidade do modificador: ")

                # validate the input
                quant = teste_val(quant)
                mod = teste_val(mod)
                """while True:
                    if validate_integer(quant) == True and validate_integer(mod) == True:
                        quant = int(quant)
                        mod = int(mod)
                        break
                    else:
                        print("Opção inválida, tente novamente")
                        quant = input("Digite a quantidade de rolagens: ")
                        mod = input("Digite a quantidade do modificador: ")"""

                # rolling dices and printing results
                for x in range(quant):
                    result.append(randint(1, basic_rolls[ans - 1]))
                    soma = result[x] + mod
                    print(f"{result[x]} + {mod} = {soma}", end='')
                    total += result[x] + mod
                    print()

                # printing some specified results
                print("-" * 30)
                print(f"Total = {total}")

            # Using favorite ones
            else:
                alterado = False
                # if favorite without roll quantity
                if favorites[ans][2] <= 0:
                    favorites[ans][2] = input("Digite a quantidade de rolagens: ")

                    # validate the input
                    teste_val(favorites[ans][2])
                    """while True:
                        if validate_integer(favorites[ans][2]) == True:
                            favorites[ans][2] = int(favorites[ans][2])
                            break
                        else:
                            print("Opção inválida, tente novamente")
                            favorites[ans][2] = input("Digite a quantidade de rolagens: ")"""
                    alterado = True

                # rolling dices and printing results
                for x in range(favorites[ans][2]):
                    result.append(randint(1, favorites[ans][0]))
                    soma = result[x] + favorites[ans][1]
                    print(f"{result[x]} + {favorites[ans][1]} = {soma}", end='')
                    total += result[x] + favorites[ans][1]
                    print()

                # printing some specified results
                print('-' * 30)
                print(f"Total = {total}")

                # just to change back the number to zero, if it was changed.
                if alterado == True:
                    favorites[ans][2] = 0

        # custom roll
        elif ans == 2:
            print("="*30)
            print("Rolagem customizada")
            # make your choices
            lado = input("Quantos lados tem o dado? ")
            quant = input("Quantos dados serão jogados? ")
            mod = input("Quanto de modificador será adicionado? ")

            # validate the input
            while True:
                if validate_integer(lado) == True and validate_integer(quant) == True and validate_integer(mod) == True:
                    lado = int(lado)
                    quant = int(quant)
                    mod = int(mod)
                    break
                else:
                    print("Opção inválida, tente novamente")
                    quant = input("Digite a quantidade de rolagens: ")
                    mod = input("Digite a quantidade do modificador: ")
                    lado = input("Quantos lados tem o dado? ")

            # rolling dices and printing results!
            for x in range(quant):
                result.append(randint(1, lado))
                soma = result[x] + mod
                print(f"{result[x]} + {mod} = {soma}", end='')
                total += result[x] + mod
                print()

            print('-' * 30)
            print(f"total = {total}")

        # rolls specifically to tests
        elif ans == 3:
            if ficha == False:
                print("Você não possui uma ficha, crie uma.")
            else:
                # making attributes numeric
                lista_atributo = list(ficha_1["attributes"])

                # making skills numeric
                lista_pericia = []
                for x in ficha_1["skills"].keys():
                    lista_pericia += list(ficha_1["skills"][x])

                soma = 0
                mod = []
                #print the attributes/skills
                pupu()
                print("-" * 30)
                print("Rolagem de testes: ")
                atri = input("Qual atributo será usado? (0 para cancelar) ")
                # validate the input
                while True:
                    if validate_integer(atri) == True:
                        atri = int(atri)
                        if atri < 0 or atri > 8:
                            print("Opção inválida, tente novamente")
                            atri = input("Qual atributo será usado? (0 para cancelar) ")
                        else:
                            break
                    else:
                        print("Opção inválida, tente novamente")
                        atri = input("Qual atributo será usado? (0 para cancelar) ")
                if atri == 0:
                    break
                mod_att = escalonamento(-4,0,4,1,1,ficha_1["attributes"][lista_atributo[atri-1]])
                mod.append(mod_att)

                print("-"*30)

                peri = input("Qual perícia será usada? (0 para cancelar) ")
                # validate input
                while True:
                    if validate_integer(peri) == True:
                        peri = int(peri)
                        if peri < 0 or peri > 31:
                            print("Opção inválida, tente novamente")
                            peri = input("Qual perícia será usada? (0 para cancelar) ")
                        else:
                            break
                    else:
                        print("Opção inválida, tente novamente")
                        peri = input("Qual perícia será usada? (0 para cancelar) ")
                if peri == 0:
                    break
                for x in ficha_1["skills"].items():
                    for y, z in ficha_1["skills"][x[0]].items():
                        if lista_pericia[peri - 1] == y:
                            if z == 0:
                                mod.append(-1)
                            elif z == 1:
                                mod.append(1)
                            elif z == 2:
                                mod.append(3)
                            elif z == 3:
                                mod.append(5)

                print("-" * 30)
                quant = input("Digite quantas rolagens serão feitas: ") #3
                # validate the input
                while True:
                    if validate_integer(quant) == True:
                        quant = int(quant)
                        break
                    else:
                        print("Opção inválida, tente novamente.")
                        quant = input("Digite quantas rolagens serão feitas: ")

                print("-" * 30)
                #to add multiples mods, 0 to stop
                print("Digite o modificado extra (Atributo e perícia já estão inclusos): ")
                while True:
                    #mod_quant = 1 DELETE LATER
                    mod_quant = input("Pode digitar individualmente, 0 para parar): ")

                    # validate the input
                    while True:
                        if validate_integer(mod_quant) == True:
                            mod_quant = int(mod_quant)
                            break
                        else:
                            print("Opção inválida, tente novamente")
                            mod_quant = input("Digite o modificador: ")
                    if mod_quant != 0:
                        mod.append(mod_quant)
                    else:
                        break

                print("-" * 30)
                #input to DC
                dc = input("Digite o nível de desafio: ")
                # validate the input
                while True:
                    if validate_integer(dc) == True:
                        dc = int(dc)
                        break
                    else:
                        print("Opção inválida, tente novamente.")
                        dc = input("Digite o nível de desafio: ")
                print("-" * 30)

                result = []
                total = []
                for y in range(len(mod)):
                    soma += mod[y]
                for x in range(quant):
                    result.append(randint(1,20))
                    total.append(result[x] + soma - abs(dc))
                    if soma < 0:
                        print(f"{result[x]} - {abs(soma)} - {abs(dc)} = {total[x]}; {success(result[x], soma, dc)}")
                    else:
                        print(f"{result[x]} + {soma} - {abs(dc)} = {total[x]}; {success(result[x], soma, dc)}")
                print("="*30)
                print(f"maior = {max(total)}; {success(max(result), soma, dc)}")
                print(f"menor = {min(total)}; {success(min(result), soma, dc)}")

        # creating, removing or changing a favorite roll
        elif ans == 4:
            # KEEP CREATING FAVORITES INDEFINITELY MUHAHAHA
            while True:
                print("=" * 30)
                print("Favoritar")
                print("-" * 30)
                print("1 - Adicionar uma rolada favorita")
                print("2 - Remover uma rolada favoritada")
                print("3 - Alterar uma rolada favoritada")
                print("4 - Sair")
                print("-" * 30)
                # chose your optiotn
                ans = input("Escolha uma opção: ")

                # validate the input
                while True:
                    if validate_integer(ans) == True:
                        ans = int(ans)
                        if ans < 0 or ans > 4:
                            print("Opção inválida, tente novamente")
                            ans = input("Escolha sua opção: ")
                        else:
                            break
                    else:
                        print("Opção inválida, tente novamente")
                        ans = input("Escolha sua opção: ")

                # add favorite
                if ans == 1:
                    print("-" * 30)
                    print("Adicionar favorito:")

                    # make your choices
                    lado = input("Quantos lados terá dado? ")
                    mod = input("Quanto de modificador será adicionado? ")
                    quant = input("Quantidade de rolagens [0 se não quiser definir, -1 para cancelar]: ")

                    # validate the input
                    while True:
                        if validate_integer(lado) == True and validate_integer(quant) == True and validate_integer(
                                mod) == True:
                            lado = int(lado)
                            quant = int(quant)
                            mod = int(mod)
                            break
                        else:
                            print("Opção inválida, tente novamente")
                            quant = input("Quantidade de rolagens [0 se não quiser definir, -1 para cancelar]: ")
                            mod = input("Digite a quantidade do modificador: ")
                            lado = input("Quantos lados tem o dado? ")

                    # if user wants to cancel
                    if quant == -1:
                        break

                    size = len(favorites) + 10
                    favorites[size] = []
                    favorites[size].append(lado)
                    favorites[size].append(mod)
                    favorites[size].append(quant)

                # remove favorite
                elif ans == 2:
                    print("-" * 30)
                    print("Remover favorito:")

                    # just printing the options
                    for x, y in favorites.items():
                        if y[2] <= 0:
                            print(f"{x} - d{y[0]}+{y[1]}", end=' | ')
                        else:
                            print(f"{x} - {y[2]}d{y[0]} + {y[1]}", end=" | ")
                    print()  # because of "end"

                    print("-" * 30)
                    # choose your option
                    ans = input("Escolha uma opção para remover: (0 para cancelar) ")

                    # validate the input
                    while True:
                        if validate_integer(ans) == True:
                            ans = int(ans)
                            if ans == 0:
                                break
                            elif ans < min(favorites) or ans > max(favorites):
                                print("Opção inválida, tente novamente")
                                ans = input("Escolha uma opção para remover: (0 para cancelar) ")
                            else:
                                break
                        else:
                            print("Opção inválida, tente novamente")
                            ans = input("Escolha uma opção para remover: (0 para cancelar) ")

                    # if user wants to cancel
                    if ans == 0:
                        break
                    # SUGGESTION - if "ans" in favorite.keys(), do the 242 - 246
                    if favorites[ans][2] <= 0:
                        print(f"d{favorites[ans][0]}+{favorites[ans][1]} será removido!")
                    else:
                        print(f"{favorites[ans][2]}d{favorites[ans][0]} + {favorites[ans][1]} será removido!")
                    favorites.pop(ans)

                    # testing the try to reorganize, at the moment this one is useless, DELETE LATER
                    """while size != max(favorites.keys()):
                        print(size)
                        print(max(favorites.keys()))
                        print("As posições não correspondem a quantidade de favoritos!")
                        try:
                            print(favorites[max(favorites.keys())-1])
                        except KeyError:
                            print("Casa vazia")
                            favorites[max(favorites.keys())-1] = favorites[max(favorites.keys())]
                            favorites.pop(max(favorites.keys()))
                        else:
                            print("Casa não vazia")"""

                    # if favorites get emptied, does nothing
                    if favorites == {}:
                        print("Todas as rolagens foram removidas!")

                    # else, reorganize everything
                    else:
                        size = len(favorites) + 9
                        teste = 0
                        while size != max(favorites.keys()):
                            try:
                                int(favorites[teste + 10][0])
                            except KeyError:
                                favorites[teste + 10] = favorites[teste + 11]
                                favorites.pop(teste + 11)
                            teste += 1

                # change favorite
                elif ans == 3:
                    print("-" * 30)
                    print("Alterar favorito:")

                    # just printing the options
                    for x, y in favorites.items():
                        if y[2] <= 0:
                            print(f"{x} - d{y[0]}+{y[1]}", end=' | ')
                        else:
                            print(f"{x} - {y[2]}d{y[0]} + {y[1]}", end=" | ")
                    print()  # because of "end"

                    print("-" * 30)
                    ans = input("Digite o dado que você quer alterar: (0 para cancelar) ")
                    # validate the input
                    while True:
                        if validate_integer(ans) == True:
                            ans = int(ans)
                            if ans == 0:
                                break
                            elif ans < min(favorites) or ans > max(favorites):
                                print("Opção inválida, tente novamente")
                                ans = input("Digite o dado que você quer alterar: (0 para cancelar) ")
                            else:
                                break
                        else:
                            print("Opção inválida, tente novamente")
                            ans = input("Digite o dado que você quer alterar: (0 para cancelar) ")

                    # if user wants to cancel
                    if ans == 0:
                        break

                    # else, will ask the changes
                    else:
                        if favorites[ans][2] <= 0:
                            print(f"{ans} - d{favorites[ans][0]}+{favorites[ans][1]} será alterado!")
                        else:
                            print(
                                f"{ans} - {favorites[ans][2]}d{favorites[ans][0]} + {favorites[ans][1]} será alterado!")

                        # asking the changes, sides - modifier - number of rolls
                        favorites[ans][0] = input("Quantidade de lados do dado: ")
                        favorites[ans][1] = input("Quantidade do modificador: ")
                        favorites[ans][2] = input("Quantidade de dados: (0 para não pré-definir) ")

                        # validate the input
                        while True:
                            if validate_integer(favorites[ans][0]) == True and validate_integer(
                                    favorites[ans][1]) == True and validate_integer(favorites[ans][2]) == True:
                                favorites[ans][0] = int(favorites[ans][0])
                                favorites[ans][1] = int(favorites[ans][1])
                                favorites[ans][2] = int(favorites[ans][2])
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                favorites[ans][0] = input("Quantidade de lados do dado: ")
                                favorites[ans][1] = input("Quantidade do modificador: ")
                                favorites[ans][2] = input("Quantidade de dados: (0 para não pré-definir) ")

                salvar()

                # just cancel
                if ans == 4:
                    break

                print("-" * 30)
                ans = input("Deseja favoritar outro dado?\n1 - SIM\n2 - NÃO\n     Sua opção: ")
                # validate the input
                while True:
                    if validate_integer(ans) == True:
                        ans = int(ans)
                        if ans > 2 or ans < 1:
                            print("Opção inválida, tente novamente")
                            ans = input("Escolha sua opção: ")
                        else:
                            break
                    else:
                        print("Opção inválida, tente novamente")
                        ans = input("Escolha sua opção: ")

                if ans == 2:
                    break

        # bye bye without doing anything
        elif ans == 5:
            break

        # DO IT AGAIN?! bye bye if did something
        print('-' * 30)
        ans = input("Deseja rolar outro dado?\n1 - SIM\n2 - NÃO\n     Sua opção: ")
        # validate the input
        ans = teste_val(ans, 1, 2)
        """while True:
            if validate_integer(ans) == True:
                ans = int(ans)
                if ans < 1 or ans > 2:
                    print("Opção inválida, tente novamente")
                    ans = input("Escolha sua opção: ")
                else:
                    break
            else:
                print("Opção inválida, tente novamente")
                ans = input("Escolha sua opção: ")"""
        if ans == 2:
            break


def character_sheet():
    global using_weight
    global hp_atual
    global sp_atual
    # predef to test, DELETE LATER
    """ficha_2["slots"].append({"Espada de ferro": ["1d20-4", "1d6"]})
    ficha_3["magic"].append({"Bola de fogo": ["1d20+5", "1d10"]})
    ficha_3["magic"].append({"Parede de gelo": ["1d20+3", "1d4"]})
    ficha_3["ability"].append({"Corte giratório": ["1d20-5", "1d8"]})
    ficha_3["ability"].append({"Corte rápido": ["1d20-4", "1d4"]})
    ficha_3["inventory"].append({"Livro de magia": [1, 100, "Permite usar magia", 3]})
    ficha_3["inventory"].append({"Espada de ferro": [5, 18, "1d6 di danu", 1]})
    ficha_3["annotation"] = "machucado"
    ficha_3["lore"] = "roubo muito >:D"""

    global ficha
    ficha = True
    print("="*30)
    print("Digite as informações")

    #input to some of the basics
    for x, y in ficha_1.items():
        if x == "player" or x == "name" or x == "level" or x == "race" or x == "background":
            ficha_1[x] = input(f"Digite o {x}: ")

            #validate the "level"
            if x == "level":
                while True:
                    if validate_integer(ficha_1[x]) == True :
                        ficha_1[x] = int(ficha_1[x])
                        if 20 >= ficha_1[x] >= 1:
                            break
                        else:
                            print("Opção inválida, digite um valor válido")
                            ficha_1[x] = input("Digite o level: ")
                    else:
                        print("Opção inválida, digite um valor válido")
                        ficha_1[x] = input("Digite o level: ")
            #validate the "race"
            if x == "race":
                while True:
                    if ficha_1[x].lower() in ["humano", "narim", "talvano", "nefelin", "alvoriano"]:
                        break
                    else:
                        ficha_1[x] = input("Digite a raça: ")

    #predef basics, to speed tests, DELETE LATER
    """
    ficha_1["player"] = jogador
    ficha_1["name"] = "Cícero"
    ficha_1["level"] = randint(1,20)
    ficha_1["race"] = "humano"
    ficha_1["background"] = "Thief"
    """

    #calculating the attributes points
    ficha_1["attributes point"] = 30 + (ficha_1["level"] - 1) * 2

    #printing title
    print("="*30)
    print(f"""Hora de evoluir os atributos, você tem {ficha_1["attributes point"]} pontos para gastar.
    OBSERVAÇÃO: Seus atributos começam nível 1! Atributos de nível 1 não gastam pontos.""")
    print("-"*30)
    #manual inputs attributes
    for x in ficha_1["attributes"]:
        ans = input(f"Digite o valor do atributo {x}: ")
        # validate the input
        while True:
            if validate_integer(ans) == True:
                ans = int(ans)
                if ans < 1 or ans > 20:
                    print("Opção inválida, tente novamente")
                    ans = input(f"Digite o valor do atributo {x}: ")
                else:
                    if ficha_1["attributes point"] < ans-1:
                        print(f"{Fore.RED}Pontos insuficientes, tente novamente{Style.RESET_ALL}")
                        ans = input(f"Digite o valor do atributo {x}: ")
                    else:
                        ficha_1["attributes point"] -= ans - 1
                        break
            else:
                print("Opção inválida, tente novamente")
                ans = input(f"Digite o valor do atributo {x}: ")
        ficha_1["attributes"][x] = ans
        print(f"Você tem {ficha_1["attributes point"]} pontos disponíveis.")
        print("-"*30)

    # printing options
    print("=" * 30)
    print("""Maestrias:
    1 - Imperito
    2 - Aprendiz
    3 - Adepto
    4 - Mestre""")
    print("-" * 30)
    # manual inputs skills
    for x in ficha_1["skills"]:
        for y in ficha_1["skills"][x]:
            ans = input(f"Digite o nível de maestria da perícia {y}: ")
            # validate the input
            while True:
                if validate_integer(ans) == True:
                    ans = int(ans)
                    if ans < 1 or ans > 4:
                        print("Opção inválida, tente novamente")
                        ans = input(f"Digite o nível de maestria da perícia {y}: ")
                    else:
                        ans -= 1
                        break
                else:
                    print("Opção inválida, tente um número")
                    ans = input(f"Digite o nível de maestria da perícia {y}: ")
            ficha_1["skills"][x][y] = ans


    #random attributes/skills, speed tests DELETE LATER
    """
    for x in ficha_1["attributes"]:
        ficha_1["attributes"][x] = randint(1, 20)

    for x in ficha_1["skills"]:
        for y in ficha_1["skills"][x]:
            ficha_1["skills"][x][y] = randint(0, 3)
    """

    #calculating the HP
    ficha_2["HP"] = escalonamento(8, 32, 48, 6, 4, ficha_1["attributes"]["endurance"])
    hp_atual = ficha_2["HP"]
    #calculating the SP
    ficha_2["SP"] = escalonamento(4, 20, 28, 4, 2, ficha_1["attributes"]["spirit"])
    sp_atual = ficha_2["SP"]
    #calculating the speed
    ficha_2["speed"] = escalonamento(3, 11, 15, 2, 1, ficha_1["attributes"]["agility"])
    #calculating the weight
    ficha_3["weight"] = escalonamento(10, 34, 50, 6, 4, ficha_1["attributes"]["strength"])
    using_weight = 0
    for x in range(len(ficha_3["inventory"])):
        for item in ficha_3["inventory"][x]:
            using_weight += (abs(ficha_3["inventory"][x][item][0]) * abs(ficha_3["inventory"][x][item][3]))

    #how many rolls i'll do
    num_dados = escalonamento(0, 4, 8, 1, 1, ficha_1["level"])
    # calculating the HP per level
    if ficha_1["race"].lower() == "humano":
        print(f"Serão jogados {num_dados} dados de 2 lados, os resultados serão somados à sua vida!")
        ficha_2["HP"] += hp_per_level(num_dados, 2)
    elif ficha_1["race"].lower() == "narim":
        print(f"Serão jogados {num_dados} dados de 3 lados, os resultados serão somados à sua vida!")
        ficha_2["HP"] += hp_per_level(num_dados, 3)
    elif ficha_1["race"].lower() == "talvano" or ficha_1["race"].lower() == "nefelin":
        print(f"Serão jogados {num_dados} dados de 4 lados, os resultados serão somados à sua vida!")
        ficha_2["HP"] += hp_per_level(num_dados, 4)
    elif ficha_1["race"].lower() == "alvoriano":
        print(f"Serão jogados {num_dados} dados de 6 lados, os resultados serão somados à sua vida!")
        ficha_2["HP"] += hp_per_level(num_dados, 6)


    ficha_2["armor"] = 0
    ficha_2["resistance"] = 0

    salvar()


def show_character_sheet():
    print("-" * 30)
    print("Basics: ")
    for x, y in ficha_1.items():
        if x != "skills" and x != "attributes":
            print(f"{x.capitalize()}: {y}")

    print("=" * 30)
    print("Attributes:")
    #NEW PRINT ATTRIBUTES
    color_count = 0
    for x, y in ficha_1["attributes"].items():
        cor = cores[color_count % len(cores)]
        mod_att = escalonamento(-4, 0, 4, 1, 1, ficha_1["attributes"][x])
        print(cor, f"{x.capitalize()} {Style.RESET_ALL}= {y}, {cor}Modificador{Style.RESET_ALL}: {mod_att}")
        color_count += 1

    print("=" * 30)
    #NEW PRINT SKILLS
    print("SKILLS:")
    for i, x in enumerate(ficha_1["skills"]):
        cor = cores[i % len(cores)]
        print(cor, f"{x.capitalize()}{Style.RESET_ALL}:")
        for y, z in ficha_1["skills"][x].items():
            dominio = list(modificador[z].keys())
            valor = list(modificador[z].values())
            print(f"{y.capitalize()} = {dominio[0].capitalize()}, {valor[0]}", end=' | ')
        print()

    print("=" * 30)
    print("Status: ")
    for x, y in ficha_2.items():
        if x == "slots":
            print(f"{x}: ")
            for teste in range(len(ficha_2[x])):
                for name, details in ficha_2[x][teste].items():
                    print(" " * 5, f"* {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")
        else:
            print(f"{x.capitalize()}: {y}")

    print("=" * 30)
    print("Others:")
    for x, y in ficha_3.items():
        if x == "weight":
            print(f"{x.capitalize()}: {using_weight}/{y}")
        elif x == "magic" or x == "ability" or x == "inventory":
            print(f"{x.capitalize()}: ")
            for z in range(len(ficha_3[x])):
                for name, details in ficha_3[x][z].items():
                    if x == "inventory":
                        print(" " * 2, f"{z+1} - {name.title()} - Peso: {details[0]}, Valor: {details[1]}, Extra: {details[2]}")
                    else:
                        print(" "*3, f"~ {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")
        else:
            print(f"{x.capitalize()}: {y.capitalize()}")


def edit_character_sheet():
    while True:
        print("=" * 30)
        print("""O que deseja alterar?
        1 - Basics (Name, level, race...)
        2 - Attributes (Strength, agility, spirit...)
        3 - Skills (athletics, memory, seduction...)
        4 - Status (HP, armor, favorites...)
        5 - Others (Annotation, magic, inventory...) 
        6 - Subir de nível
        7 - Sair""")
        print("-" * 50)
        ans = input("Digite sua opção: ")
        # validate the input
        while True:
            if validate_integer(ans) == True:
                ans = int(ans)
                if ans < 1 or ans > 7:
                    print("Opção inválida, tente novamente")
                    ans = input("Escolha sua opção: ")
                else:
                    break
            else:
                print("Opção inválida, tente novamente")
                ans = input("Escolha sua opção: ")

        #change the basics
        if ans == 1:
            #making the options numeric
            changeable = []
            lista = list(ficha_1.items())
            for x in range(len(lista)):
                if lista[x][0] != "attributes" and lista[x][0] != "skills" and lista[x][0] != "player":
                    changeable.append(lista[x][0])

            #printing menu
            print("="*30)
            print("Basics:")
            cont = 1
            for x, y in ficha_1.items():
                if x != "skills" and x != "attributes" and x != "player":
                    print(f"{cont} - {x.capitalize()}: {y}")
                    cont += 1

            print("-"*30)
            alt = input("O que você deseja alterar? (0 para cancelar) ")
            # validate the input
            while True:
                if validate_integer(alt) == True:
                    alt = int(alt)
                    if alt < 0 or alt > 6:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    alt = input("O que você deseja alterar? (0 para cancelar) ")
            if alt == 0:
                break

            if changeable[alt-1] == "level":
                # for the function evolve_status
                level_atual = ficha_1["level"]
                ans = input(f"Qual o novo {changeable[alt-1]}? (0 para cancelar) ")
                # validate the input
                while True:
                    if validate_integer(ans) == True:
                        ans = int(ans)
                        if ans < 0 or ans > 20:
                            print("Opção inválida, tente novamente")
                            ans = input("Escolha sua opção: ")
                        else:
                            break
                    else:
                        print("Opção inválida, tente novamente")
                        ans = input("Escolha sua opção: ")
                if ans == 0:
                    break

                ficha_1[changeable[alt - 1]] = ans
                ficha_1["attributes point"] += (2*(ficha_1["level"]-1) - 2*(level_atual-1))

                # calculating the rolls to HP increase
                num_dados = evolve_status("HP2", level_atual)

                if ficha_1["race"].lower() == "humano":
                    print(f"Serão jogados {num_dados} dados de 2 lados, os resultados serão somados à sua vida!")
                    ficha_2["HP"] += hp_per_level(num_dados, 2)

                elif ficha_1["race"].lower() == "narim":
                    print(f"Serão jogados {num_dados} dados de 3 lados, os resultados serão somados à sua vida!")
                    ficha_2["HP"] += hp_per_level(num_dados, 3)

                elif ficha_1["race"].lower() == "talvano" or ficha_1["race"].lower() == "nefelin":
                    print(f"Serão jogados {num_dados} dados de 4 lados, os resultados serão somados à sua vida!")
                    ficha_2["HP"] += hp_per_level(num_dados, 4)

                elif ficha_1["race"].lower() == "alvoriano":
                    print(f"Serão jogados {num_dados} dados de 6 lados, os resultados serão somados à sua vida!")
                    ficha_2["HP"] += hp_per_level(num_dados, 6)
            else:
                while True:
                    novo = input(f"Qual o novo {changeable[alt-1]}? (0 para cancelar) ")
                    if novo == "0":
                        break
                    if changeable[alt-1] == "race":
                        if novo.lower() in ["humano", "narim", "talvano", "nefelin", "alvoriano"]:
                            break
                        else:
                            print("Raça inválida, tente novamente")
                    #making sure AP is INT
                    elif changeable[alt-1] == "attributes point":
                        # validate the input
                        while True:
                            if validate_integer(novo) == True:
                                novo = int(novo)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                novo = input(f"Qual o novo {changeable[alt-1]}? (0 para cancelar) ")
                    else:
                        break
                if novo != 0 and novo != "0":
                    ficha_1[changeable[alt - 1]] = novo

        #change the attributes
        elif ans == 2:
            #if i want to make it so you need attributes point to change a attribute
            """# printing title
            print("=" * 30)
            print(f"Você tem {ficha_1["attributes point"]} pontos para gastar.")
            print("-" * 30)
            # manual inputs attributes
            for x in ficha_1["attributes"]:
                ans = input(f"Digite o valor do atributo {x}: ")
                # validate the input
                while True:
                    if validate_integer(ans) == True:
                        ans = int(ans)
                        if ans < 1 or ans > 20:
                            print("Opção inválida, tente novamente")
                            ans = input(f"Digite o valor do atributo {x}: ")
                        else:
                            if ficha_1["attributes point"] < ans-1:
                                print(f"{Fore.RED}Pontos insuficientes, tente novamente{Style.RESET_ALL}")
                                ans = input(f"Digite o valor do atributo {x}: ")
                            else:
                                ficha_1["attributes point"] -= ans - 1
                                break
                    else:
                        print("Opção inválida, tente novamente")
                        ans = input(f"Digite o valor do atributo {x}: ")
                ficha_1["attributes"][x] = ans
                print(f"Você tem {ficha_1["attributes point"]} pontos disponíveis.")
                print("-"*30)"""

            # making the options numeric
            lista = list(ficha_1["attributes"])

            #printing menu
            print("-"*30)
            print("Attributes:")
            cont = 1
            color_count = 0
            for x, y in ficha_1["attributes"].items():
                mod_att = escalonamento(-4, 0, 4, 1, 1, ficha_1["attributes"][x])
                cor = cores[color_count % len(cores)]
                print(f"{Fore.LIGHTMAGENTA_EX}{cont}{Style.RESET_ALL} - {cor}{x.capitalize()}{Style.RESET_ALL}: {y}, mod: {mod_att}", end=' | ')
                #just so it doesn't become a giant line of attributes
                if cont == 4:
                    print()
                    print()
                cont+=1
                color_count+=1
            print()

            #choose the attribute
            print("="*30)
            alt = input("O que você deseja alterar? (0 para cancelar) ")
            # validate the input
            while True:
                if validate_integer(alt) == True:
                    alt = int(alt)
                    if alt < 0 or alt > 8:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    alt = input("O que você deseja alterar? (0 para cancelar) ")
            if alt == 0:
                break

            #choose the value of the attribute
            valor = input(f"Digite o valor do atributo {lista[alt-1]}: (0 para cancelar) ")
            # validate the input
            while True:
                if validate_integer(valor) == True:
                    valor = int(valor)
                    if valor < 0 or valor > 20:
                        print("Opção inválida, tente novamente")
                        valor = input(f"Digite o valor do atributo {lista[alt-1]}: (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    valor = input(f"Digite o valor do atributo {lista[alt - 1]}: (0 para cancelar) ")
            if valor == 0:
                break


            # for the evolve status
            level_atual = ficha_1["attributes"][lista[alt - 1]]
            # updating the attribute
            ficha_1["attributes"][lista[alt - 1]] = valor


            #OLD SP, SPEED AND WEIGHT SCALE
            """
            if lista[alt-1] == "spirit":
                ficha_2["SP"] = escalonamento(4, 20, 28, 4, 2, ficha_1["attributes"]["spirit"])
            elif lista[alt-1] == "agility":
                ficha_2["speed"] = escalonamento(3, 11, 15, 2, 1, ficha_1["attributes"]["agility"])
            elif lista[alt-1] == "strength":
                ficha_3["weight"] = escalonamento(10, 34, 50, 6, 4, ficha_1["attributes"]["strength"])
            """

            #upgrading the SP, SPEED, WEIGHT, HP
            if lista[alt - 1] == "spirit":
                ficha_2["SP"] += evolve_status("SP", level_atual)
            elif lista[alt - 1] == "agility":
                ficha_2["speed"] += evolve_status("speed", level_atual)
            elif lista[alt - 1] == "strength":
                ficha_3["weight"] += evolve_status("weight", level_atual)
            elif lista[alt-1] == "endurance":
                ficha_2["HP"] += evolve_status("HP", level_atual)

        #change the skills
        elif ans == 3:
            #making it numeric options
            lista = []
            for x in ficha_1["skills"].keys():
                lista += list(ficha_1["skills"][x])

            #printing menu
            print("-"*30)
            print("Skills:")
            cont = 1
            for i, x in enumerate(ficha_1["skills"]):
                cor = cores[i % len(cores)]
                print(cor, f"{x.capitalize()}:", Style.RESET_ALL)
                for y, z in ficha_1["skills"][x].items():
                    dominio = list(modificador[z].keys())
                    valor = list(modificador[z].values())
                    print(f" {Fore.LIGHTMAGENTA_EX}{cont}{Style.RESET_ALL} - {y.capitalize()} = {dominio[0].capitalize()}, {valor[0]}", end=' | ')
                    cont+=1
                print()

            print("-" * 30)
            alt = input("O que você deseja alterar? (0 para cancelar) ")
            # validate input
            while True:
                if validate_integer(alt) == True:
                    alt = int(alt)
                    if alt < 0 or alt > 31:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    alt = input("O que você deseja alterar? (0 para cancelar) ")
            if alt == 0:
                break

            # printing options
            print("=" * 30)
            print("""Maestrias:
    1 - Imperito
    2 - Adepto
    3 - Intermediário
    4 - Mestre""")
            print("-" * 30)
            # manual inputs skills
            ans = input(f"Digite o nível de maestria da perícia {lista[alt-1]}: (0 para cancelar) ")
            if ans == "0":
                break
            # validate the input
            while True:
                if validate_integer(ans) == True:
                    ans = int(ans)
                    if ans < 1 or ans > 4:
                        print("Opção inválida, tente novamente")
                        ans = input(f"Digite o nível de maestria da perícia {lista[alt-1]}: ")
                    else:
                        ans -= 1
                        break
                else:
                    print("Opção inválida, tente um número")
                    ans = input(f"Digite o nível de maestria da perícia {lista[alt-1]}: ")
            # changing the skill
            for x in ficha_1["skills"].items():
                for y, z in ficha_1["skills"][x[0]].items():
                    if lista[alt-1] == y:
                        ficha_1["skills"][x[0]][y] = ans

            #Delete later i guess
            """#PRECISA VALIDAR
            #PRECISA MOSTRAR AS OPÇÕES
            ans = input(f"Qual o novo valor de {lista[alt-1]}? ")
            # validate the input
            while True:
                if validate_integer(ans) == True:
                    ans = int(ans)
                    if ans < 1 or ans > 4:
                        print("Opção inválida, tente novamente")
                        ans = input(f"Digite o nível de maestria da perícia {y}: ")
                    else:
                        ans -= 1
                        break
            ficha_1["skills"]["strength"][lista[alt-1]] = ans"""

        #change the status
        elif ans == 4:
            #making it numeric options
            lista = list(ficha_2.keys())
            #printing menu
            print("="*30)
            print("Status")
            cont = 1
            for x, y in ficha_2.items():
                if x == "slots":
                    print(f"{cont} - {x}: ")
                    for teste in range(len(ficha_2[x])):
                        for name, details in ficha_2[x][teste].items():
                            print(" " * 5, f"* {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")
                else:
                    print(f"{cont} - {x.capitalize()}: {y}")
                cont+=1

            print("-"*30)
            alt = input("O que você deseja alterar? (0 para cancelar) ")
            # validate input
            while True:
                if validate_integer(alt) == True:
                    alt = int(alt)
                    if alt < 0 or alt > 6:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    alt = input("O que você deseja alterar? (0 para cancelar) ")
            if alt == 0:
                break

            #favoriting an attack
            elif alt == 6:
                while True:
                    print("="*30)
                    print(f"Favoritando:\n1 - Adicionar favorito\n2 - Remover favorito\n3 - Alterar favorito\n4 - Sair")
                    print("-"*30)
                    ans = input("Escolha sua opção: ")
                    #add favorite
                    if ans == "1":
                        print("-"*30)
                        print("Adicionando:\nDigite 0 para cancelar")
                        item = input("Qual o nome do atalho? (nome da espada, magia, etc.) ")
                        if item == "0":
                            break
                        roll = input("Qual a rolagem? (Ex.: 1d20+5) ")
                        if roll == "0":
                            break
                        prop = input("Qual a propriedade? (Dano, efeito...) ")
                        if prop == "0":
                            break

                        ficha_2["slots"].append({f"{item}": [roll, prop]})

                    #remove favorite
                    elif ans == "2":
                        #printing options
                        print(f"Removendo {lista[alt-1].capitalize()}: ")
                        cont = 0

                        for x in range(len(ficha_2[lista[alt-1]])):
                            for name, details in ficha_2[lista[alt-1]][x].items():
                                cont += 1
                                print(f" ", f"{cont} - {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")

                        print("-"*30)
                        ans = input("Escolha sua opção: (0 para cancelar) ")
                        #validate input
                        while True:
                            if validate_integer(ans) == True:
                                ans = int(ans)
                                if ans < 0 or ans > len(ficha_2[lista[alt-1]]):
                                    print("Opção inválida, tente novamente")
                                    ans = input("Escolha sua opção: (0 para cancelar) ")
                                else:
                                    break
                            else:
                                print("Opção inválida, tente novamente")
                                ans = input("Escolha sua opção: (0 para cancelar) ")
                        if ans == 0:
                            break
                        ficha_2[lista[alt - 1]].pop(ans-1)

                    #change favorite
                    elif ans == "3":
                        # printing options
                        print(f"Alterando {lista[alt - 1].capitalize()}: ")
                        cont = 0
                        for z in range(len(ficha_2[lista[alt - 1]])):
                            cont += 1
                            for name, details in ficha_2[lista[alt - 1]][z].items():
                                print(f" ",
                                      f"{cont} - {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")

                        print("-"*30)
                        ans = input("Escolha sua opção: (0 para cancelar) ")
                        #validate input
                        while True:
                            if validate_integer(ans) == True:
                                ans = int(ans)
                                if ans < 0 or ans > len(ficha_2[lista[alt-1]]):
                                    print("Opção inválida, tente novamente")
                                    ans = input("Escolha sua opção: (0 para cancelar) ")
                                else:
                                    break
                            else:
                                print("Opção inválida, tente novamente")
                                ans = input("Escolha sua opção: (0 para cancelar) ")
                        if ans == 0:
                            break
                        name = input(f"Digite o nome da {lista[alt-1].title()}: (-1 para cancelar) ")
                        if name == "-1":
                            break
                        details1 = input(f"Digite o dado da {lista[alt-1].title()}: (-1 para cancelar) ")
                        if details1 == "-1":
                            break
                        details2 = input(f"Digite o efeito da {lista[alt - 1].title()}: (-1 para cancelar) ")
                        if details2 == "-1":
                            break
                        ficha_2[lista[alt - 1]][ans-1] = {f"{name}": [details1, details2]}

                    elif ans == "4":
                        break
                    else:
                        print("Opção inválida, tente novamente")
                        print("Escolha sua opção: ")
            else:
                valor = input(f"Qual o novo valor de {lista[alt-1]}? (-1 para cancelar) ")
                #
                if valor == "-1":
                    break
                # validate input
                while True:
                    if validate_integer(valor) == True:
                        valor = int(valor)
                        ficha_2[lista[alt - 1]] = valor
                        break
                    else:
                        print("Opção inválida, digite um número")
                        valor = input(f"Qual o novo valor de {lista[alt-1]}? (-1 para cancelar) ")
                        if valor == "-1":
                            break

        #change other things
        elif ans == 5:
            global using_weight
            #making it numeric options
            lista = list(ficha_3.keys())

            print("="*30)
            #printing options
            print("Others")
            cont = 1
            for x, y in ficha_3.items():
                if x == "weight":
                    print(f"{cont} - {x.capitalize()}: {using_weight}/{y}")
                elif x == "magic" or x == "ability" or x == "inventory":
                    print(f"{cont} - {x.capitalize()}: ")
                    for z in range(len(ficha_3[x])):
                        for name, details in ficha_3[x][z].items():
                            if x == "inventory":
                                print(" " * 3,
                                      f"{details[3]} ~ {name.title()} - Peso: {details[0]}, Valor: {details[1]}, Extra: {details[2]}")
                            else:
                                print(" " * 3,
                                      f"~ {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")
                else:
                    print(f"{cont} - {x.capitalize()}: {y.capitalize()}")
                cont += 1

            print("-"*30)
            alt = input("O que você deseja alterar? (0 para cancelar) ")
            #validate input
            while True:
                if validate_integer(alt) == True:
                    alt = int(alt)
                    if alt < 0 or alt > 6:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    alt = input("O que você deseja alterar? (0 para cancelar) ")
            if alt == 0:
                break

            if lista[alt-1] == "magic" or lista[alt-1] == "ability":
                while True:
                    print("="*30)
                    print(f"{lista[alt-1].title()}:\n1 - Adicionar item\n2 - Remover item\n3 - Alterar item\n4 - Sair")
                    print("-"*30)
                    ans = input("Escolha sua opção: ")
                    #add magic/ability
                    if ans == "1":
                        print("-"*30)
                        print("Adicionando: ")
                        name = input(f"Digite o nome da {lista[alt-1].title()}: ")
                        details1 = input(f"Digite o dado da {lista[alt-1].title()}: ")
                        details2 = input(f"Digite o efeito da {lista[alt - 1].title()}: ")
                        ficha_3[lista[alt - 1]].append({f"{name}": [details1, details2]})

                    #remove magic/ability
                    elif ans == "2":
                        #printing options
                        print(f"Removendo {lista[alt-1].capitalize()}: ")
                        cont = 0
                        for z in range(len(ficha_3[lista[alt-1]])):
                            cont += 1
                            for name, details in ficha_3[lista[alt-1]][z].items():
                                print(f" ", f"{cont} - {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")

                        print("-"*30)
                        ans = input("Escolha sua opção: (0 para cancelar) ")
                        #validate input
                        while True:
                            if validate_integer(ans) == True:
                                ans = int(ans)
                                if ans < 0 or ans > len(ficha_3[lista[alt-1]]):
                                    print("Opção inválida, tente novamente")
                                    ans = input("Escolha sua opção: (0 para cancelar) ")
                                else:
                                    break
                            else:
                                print("Opção inválida, tente novamente")
                                ans = input("Escolha sua opção: (0 para cancelar) ")
                        if ans == 0:
                            break
                        ficha_3[lista[alt - 1]].pop(ans-1)

                    #change magic/ability
                    elif ans == "3":
                        # printing options
                        print(f"Alterando {lista[alt - 1].capitalize()}: ")
                        cont = 0
                        for z in range(len(ficha_3[lista[alt - 1]])):
                            cont += 1
                            for name, details in ficha_3[lista[alt - 1]][z].items():
                                print(f" ",
                                      f"{cont} - {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")

                        print("-"*30)
                        ans = input("Escolha sua opção: (0 para cancelar) ")
                        #validate input
                        while True:
                            if validate_integer(ans) == True:
                                ans = int(ans)
                                if ans < 0 or ans > len(ficha_3[lista[alt-1]]):
                                    print("Opção inválida, tente novamente")
                                    ans = input("Escolha sua opção: (0 para cancelar) ")
                                else:
                                    break
                            else:
                                print("Opção inválida, tente novamente")
                                ans = input("Escolha sua opção: (0 para cancelar) ")
                        if ans == 0:
                            break
                        name = input(f"Digite o nome da {lista[alt-1].title()}: (-1 para cancelar) ")
                        if name == "-1":
                            break
                        details1 = input(f"Digite o dado da {lista[alt-1].title()}: (-1 para cancelar) ")
                        if details1 == "-1":
                            break
                        details2 = input(f"Digite o efeito da {lista[alt - 1].title()}: (-1 para cancelar) ")
                        if details2 == "-1":
                            break
                        ficha_3[lista[alt - 1]][ans-1] = {f"{name}": [details1, details2]}

                    elif ans == "4":
                        break
                    else:
                        print("Opção inválida, tente novamente")
                        print("Escolha sua opção: ")
            elif lista[alt-1] == "inventory":
                while True:
                    print("="*30)
                    print(f"{lista[alt-1].title()}:\n1 - Adicionar item\n2 - Remover item\n3 - Alterar item\n4 - Sair")
                    print("-"*30)
                    ans = input("Escolha sua opção: ")
                    #add item
                    if ans == "1":
                        print("-"*30)
                        print("Adicionando: ")
                        name = input("Digite o nome do item: ")
                        details1 = input("Digite o peso do item: ")
                        # validate input
                        while True:
                            if validate_integer(details1) == True:
                                details1 = int(details1)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details1 = input(f"Digite o valor do item: ")
                        details2 = input("Digite o valor do item: ")
                        # validate input
                        while True:
                            if validate_integer(details2) == True:
                                details2 = int(details2)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details2 = input(f"Digite o valor do item: ")
                        details3 = input("Digite algo extra do item: ")
                        details4 = input("Digite a quantidade desse item: ")
                        # validate input
                        while True:
                            if validate_integer(details4) == True:
                                details4 = int(details4)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details4 = input("Digite a quantidade desse item: ")
                        ficha_3[lista[alt - 1]].append({f"{name}": [details1, details2, details3, details4]})
                    #remove item
                    elif ans == "2":
                        # printing options
                        print(f"Removendo {lista[alt - 1].capitalize()}: ")
                        cont = 0
                        for z in range(len(ficha_3[lista[alt - 1]])):
                            cont += 1
                            for name, details in ficha_3[lista[alt - 1]][z].items():
                                print(" ", f"{cont} - {name.title()} - Peso: {details[0]}, Valor: {details[1]}, Extra: {details[2]}")

                        print("-" * 30)
                        ans = input("Escolha sua opção: (0 para cancelar) ")
                        # validate input
                        while True:
                            if validate_integer(ans) == True:
                                ans = int(ans)
                                if ans < 0 or ans > len(ficha_3[lista[alt - 1]]):
                                    print("Opção inválida, tente novamente")
                                    ans = input("Escolha sua opção: (0 para cancelar) ")
                                else:
                                    break
                            else:
                                print("Opção inválida, tente novamente")
                                ans = input("Escolha sua opção: (0 para cancelar) ")
                        if ans == 0:
                            break
                        ficha_3[lista[alt - 1]].pop(ans - 1)
                    #change item
                    elif ans == "3":
                        # printing options
                        print(f"Alterando {lista[alt - 1].capitalize()}: ")
                        cont = 0
                        for z in range(len(ficha_3[lista[alt - 1]])):
                            cont += 1
                            for name, details in ficha_3[lista[alt - 1]][z].items():
                                print(" ",
                                      f"{cont} - {name.title()} - Peso: {details[0]}, Valor: {details[1]}, Extra: {details[2]}")

                        print("-" * 30)
                        ans = input("Escolha sua opção: (0 para cancelar) ")
                        # validate input
                        while True:
                            if validate_integer(ans) == True:
                                ans = int(ans)
                                if ans < 0 or ans > len(ficha_3[lista[alt - 1]]):
                                    print("Opção inválida, tente novamente")
                                    ans = input("Escolha sua opção: (0 para cancelar) ")
                                else:
                                    break
                            else:
                                print("Opção inválida, tente novamente")
                                ans = input("Escolha sua opção: (0 para cancelar) ")
                        if ans == 0:
                            break
                        name = input(f"Digite o nome do item: (-1 para cancelar) ")
                        if name == "-1":
                            break

                        details1 = input(f"Digite o peso do item: (-1 para cancelar) ")
                        # validate input
                        while True:
                            if validate_integer(details1) == True:
                                details1 = int(details1)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details1 = input(f"Digite o peso do item: ")
                        if details1 == -1:
                            break

                        details2 = input(f"Digite o valor do item: (-1 para cancelar) ")
                        # validate input
                        while True:
                            if validate_integer(details2) == True:
                                details2 = int(details2)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details2 = input(f"Digite o valor do item: ")
                        if details2 == -1:
                            break

                        details3 = input(f"Digite algo extra do item: (-1 para cancelar) ")
                        if details3 == "-1":
                            break

                        ficha_3[lista[alt - 1]][ans-1] = ({f"{name}": [details1, details2, details3]})

                    elif ans == "4":
                        break
                    else:
                        print("Opção inválida, tente novamente")
                        print("Escolha sua opção: ")
            elif lista[alt-1] == "weight":
                ans = input(f"Digite o novo valor de {lista[alt-1]}: (0 para cancelar) ")
                # validate input
                while True:
                    if validate_integer(alt) == True:
                        alt = int(alt)
                        break
                    else:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                if ans == 0:
                    break
                ficha_3[lista[alt-1]] = ans
            else:
                ans = input("O que você deseja escrever? (0 para cancelar) ")
                if ans == "0":
                    break
                ficha_3[lista[alt - 1]] = ans

            using_weight = 0
            for x in range(len(ficha_3["inventory"])):
                for item in ficha_3["inventory"][x]:
                    using_weight += (abs(ficha_3["inventory"][x][item][0])*abs(ficha_3["inventory"][x][item][3]))

        #level up
        elif ans == 6:
            while True:
                print("="*30)
                print(f"Subir de nível\nSeu nível atual é: {ficha_1["level"]}\n1 - Subir de nível\n2 - Evoluir atributo\n3 - Evoluir perícia\n4 - Sair")
                print("-"*30)
                alt = input("Escolha uma opção: ")

                #Level up
                if alt == "1":
                    if ficha_1["level"] == 20:
                        print("Você já está no nível máximo, não é possível subir mais.")
                        sleep(1)
                        break
                    print("="*30)
                    print("Deseja subir o nível?\n1 - Sim\n2 - Não")
                    alt = input("Escolha uma opção: ")
                    if alt == "1":
                        # making the options numeric
                        lista = list(ficha_1["attributes"])
                        #for the function evolve_status
                        level_atual = ficha_1["level"]
                        ficha_1["level"] += 1
                        ficha_1["attributes point"] += 2
                        # calculating the HP increase
                        num_dados = evolve_status("HP2", level_atual)

                        if ficha_1["race"].lower() == "humano":
                            print(
                                f"Serão jogados {num_dados} dados de 2 lados, os resultados serão somados à sua vida!")
                            ficha_2["HP"] += hp_per_level(num_dados, 2)

                        elif ficha_1["race"].lower() == "narim":
                            print(
                                f"Serão jogados {num_dados} dados de 3 lados, os resultados serão somados à sua vida!")
                            ficha_2["HP"] += hp_per_level(num_dados, 3)

                        elif ficha_1["race"].lower() == "talvano" or ficha_1["race"].lower() == "nefelin":
                            print(
                                f"Serão jogados {num_dados} dados de 4 lados, os resultados serão somados à sua vida!")
                            ficha_2["HP"] += hp_per_level(num_dados, 4)

                        elif ficha_1["race"].lower() == "alvoriano":
                            print(f"Serão jogados {num_dados} dados de 6 lados, os resultados serão somados à sua vida!")
                            ficha_2["HP"] += hp_per_level(num_dados, 6)


                        # printing menu
                        print("-" * 30)
                        print("Attributes:")
                        cont = 1
                        color_count = 0
                        for x, y in ficha_1["attributes"].items():
                            cor = cores[color_count % len(cores)]
                            print(f"{Fore.LIGHTMAGENTA_EX}{cont}{Style.RESET_ALL} - {cor}{x.capitalize()}{Style.RESET_ALL}: {y}", end=' | ')
                            # just so it doesn't become a giant line of attributes
                            if cont == 4:
                                print()
                                print()
                            cont += 1
                            color_count += 1
                        print()

                        #evolving the attributes
                        while ficha_1["attributes point"] > 0:
                            print("=" * 30)
                            print(f"Você tem {ficha_1["attributes point"]} pontos disponíveis!")
                            alt = input("O que você deseja aumentar? (0 para cancelar) ")
                            # validate the input
                            while True:
                                    if validate_integer(alt) == True:
                                        alt = int(alt)
                                        if alt < 0 or alt > 8:
                                            print("Opção inválida, tente novamente")
                                            alt = input("O que você deseja aumentar? (0 para cancelar) ")
                                        elif ficha_1["attributes"][lista[alt - 1]] == 20:
                                            print("Opção inválida, o atributo já está maximizado")
                                            alt = input("O que você deseja aumentar? (0 para cancelar) ")
                                        else:
                                            break
                                    else:
                                        print("Opção inválida, tente novamente")
                                        alt = input("O que você deseja aumentar? (0 para cancelar) ")
                            if alt == 0:
                                break

                            valor = input(f"Digite o aumento no atributo {lista[alt - 1]}: (0 para cancelar) ")
                            # validate the input
                            while True:
                                    if validate_integer(valor) == True:
                                        valor = int(valor)
                                        if valor < 0 or valor > ficha_1["attributes point"]:
                                            print("Opção inválida, tente novamente")
                                            valor = input(f"Digite o aumento no atributo {lista[alt - 1]}: (0 para cancelar) ")
                                        elif (ficha_1["attributes"][lista[alt - 1]] + valor) > 20:
                                            print("Opção inválida, essa evolução passa do limite dos atributos de 20.")
                                            valor = input(
                                                f"Digite o aumento no atributo {lista[alt - 1]}: (0 para cancelar) ")
                                        else:
                                            break
                                    else:
                                        print("Opção inválida, tente novamente")
                                        valor = input(f"Digite o aumento no atributo {lista[alt - 1]}: (0 para cancelar) ")
                            if valor == 0:
                                break

                            #for the evolve status
                            level_atual = ficha_1["attributes"][lista[alt - 1]]
                            #updating the attribute
                            ficha_1["attributes"][lista[alt - 1]] += valor
                            ficha_1["attributes point"] -= valor

                            if lista[alt - 1] == "endurance":
                                ficha_2["HP"] += evolve_status("HP", level_atual)

                            elif lista[alt - 1] == "spirit":
                                ficha_2["spirit"] += evolve_status("SP", level_atual)

                            elif lista[alt - 1] == "agility":
                                ficha_2["speed"] += evolve_status("speed", level_atual)

                            elif lista[alt - 1] == "strength":
                                ficha_3["weight"] += evolve_status("weight", level_atual)


                    elif alt == "2":
                        break
                    else:
                        print("Opção inválida, tente novamente.")

                #evolve attribute
                elif alt == "2":
                    if ficha_1["attributes point"] == 0:
                        print("Você não tem pontos disponíveis")
                        sleep(1)
                    else:
                        lista = list(ficha_1["attributes"])
                        # printing menu
                        print("-" * 30)
                        print("Attributes:")
                        cont = 1
                        color_count = 0
                        for x, y in ficha_1["attributes"].items():
                            cor = cores[color_count % len(cores)]
                            print(
                                f"{Fore.LIGHTMAGENTA_EX}{cont}{Style.RESET_ALL} - {cor}{x.capitalize()}{Style.RESET_ALL}: {y}",
                                end=' | ')
                            # just so it doesn't become a giant line of attributes
                            if cont == 4:
                                print()
                                print()
                            cont += 1
                            color_count += 1
                        print()

                        # evolving the attributes
                        while ficha_1["attributes point"] > 0:
                            print("=" * 30)
                            print(f"Você tem {ficha_1["attributes point"]} pontos disponíveis!")
                            alt = input("O que você deseja aumentar? (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(alt) == True:
                                    alt = int(alt)
                                    if alt < 0 or alt > 8:
                                        print("Opção inválida, tente novamente")
                                        alt = input("O que você deseja aumentar? (0 para cancelar) ")
                                    elif ficha_1["attributes"][lista[alt - 1]] == 20:
                                        print("Opção inválida, o atributo já está maximizado")
                                        alt = input("O que você deseja aumentar? (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    alt = input("O que você deseja aumentar? (0 para cancelar) ")
                            if alt == 0:
                                break

                            valor = input(f"Digite o aumento no atributo {lista[alt - 1]}: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(valor) == True:
                                    valor = int(valor)
                                    if valor < 0 or valor > ficha_1["attributes point"]:
                                        print("Opção inválida, tente novamente")
                                        valor = input(f"Digite o aumento no atributo {lista[alt - 1]}: (0 para cancelar) ")
                                    elif (ficha_1["attributes"][lista[alt - 1]] + valor) > 20:
                                        print("Opção inválida, essa evolução passa do limite dos atributos de 20.")
                                        valor = input(
                                            f"Digite o aumento no atributo {lista[alt - 1]}: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    valor = input(f"Digite o aumento no atributo {lista[alt - 1]}: (0 para cancelar) ")
                            if valor == 0:
                                break

                            # for the evolve status
                            level_atual = ficha_1["attributes"][lista[alt - 1]]
                            # updating the attribute
                            ficha_1["attributes"][lista[alt - 1]] += valor
                            ficha_1["attributes point"] -= valor

                            if lista[alt - 1] == "endurance":
                                ficha_2["HP"] += evolve_status("HP", level_atual)

                            elif lista[alt - 1] == "spirit":
                                ficha_2["SP"] += evolve_status("SP", level_atual)

                            elif lista[alt - 1] == "agility":
                                ficha_2["speed"] += evolve_status("speed", level_atual)

                            elif lista[alt - 1] == "strength":
                                ficha_3["weight"] += evolve_status("weight", level_atual)

                #evolve skills
                elif alt == "3":
                    print("tem nada por enqt")

                #bye bye
                elif alt == "4":
                    break
                #womp womp
                else:
                    print("Opção inválida, tente novamente.")

        #bye bye
        elif ans == 7:
            save = input("Deseja salvar as alterações?\n1 - SIM\n2 - NÃO\n")
            if save == "2":
                print("Não será salvo")
                break
            else:
                print("Salvando...")
                sleep(1)
                salvar()
                break


#show basics
def papa(hp_atual, sp_atual):
    print("Basics: ")
    for x, y in ficha_1.items():
        if x == "name" or x == "level":
            print(f"{x.capitalize()}: {y}", end=" | ")
        if x == "situation":
            print()
            print(f"{x.capitalize()}: {y}")

    print("=" * 30)
    print("Status: ")
    cont = 0
    for x, y in ficha_2.items():
        if x == "slots":
            print()
            print(f"{x}: ")
            for teste in range(len(ficha_2[x])):
                for name, details in ficha_2[x][teste].items():
                    print(" " * 5, f"* {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")
        else:
            if cont == 2:
                print()
            if x == "HP":
                print(f"{x.capitalize()}: {hp_atual}/{y}", end=" | ")
            elif x == "SP":
                print(f"{x.capitalize()}: {sp_atual}/{y}", end=" | ")
            else:
                print(f"{x.capitalize()}: {y}", end = " | ")
        cont += 1

#show others
def pepe():
    print("=" * 30)
    print("Others:")
    for x, y in ficha_3.items():
        if x == "weight":
            pass
        elif x == "magic" or x == "ability" or x == "inventory":
            if x == "inventory":
                print(f"{x.capitalize()} ({using_weight}/{ficha_3["weight"]}) : ")
            else:
                print(f"{x.capitalize()}: ")
            for z in range(len(ficha_3[x])):
                for name, details in ficha_3[x][z].items():
                    if x == "inventory":
                        print(" " * 2,
                              f"{z + 1} - {name.title()} - Peso: {details[0]}, Valor: {details[1]}, Extra: {details[2]}")
                    else:
                        print(" " * 3, f"~ {name.title()} - Dado: {details[0]}, Efeito: {details[1].capitalize()}")
        elif x == "annotation":
            print(f"{x.capitalize()}: {y.capitalize()}")

#show attributes/skills
def pupu():
    print("=" * 30)
    cont = 1
    color_count = 0
    for x, y in ficha_1["attributes"].items():
        cor = cores[color_count % len(cores)]
        mod_att = escalonamento(-4, 0, 4, 1, 1, ficha_1["attributes"][x])
        print(f"{Fore.LIGHTMAGENTA_EX}{cont}{Style.RESET_ALL} - {cor}{x.capitalize()}{Style.RESET_ALL}: {y}, mod: {mod_att}", end=' | ')
        # just so it doesn't become a giant line of attributes
        if cont == 4:
            print()
            print()
        cont += 1
        color_count += 1
    print()

    cont = 1
    print("=" * 30)
    print("SKILLS:")
    for i, x in enumerate(ficha_1["skills"]):
        cor = cores[i % len(cores)]
        print(cor, f"{x.capitalize()}{Style.RESET_ALL}:")
        for y, z in ficha_1["skills"][x].items():
            dominio = list(modificador[z].keys())
            valor = list(modificador[z].values())
            print(f"{Fore.LIGHTMAGENTA_EX}{cont}{Style.RESET_ALL} - {y.capitalize()} = {dominio[0].capitalize()}, {valor[0]}", end=' | ')
            cont += 1
        print()

#edit to batte_mode
def edit_junior():
    while True:
        print("=" * 30)
        print("""O que deseja alterar?
        1 - Attributes (Strength, agility, spirit...)
        2 - Skills (athletics, memory, seduction...)
        3 - Status (HP, armor, favorites...)
        4 - Others (Annotation, weight, inventory) 
        5 - Sair""")
        print("-" * 50)
        ans = input("Digite sua opção: ")
        # validate the input
        while True:
            if validate_integer(ans) == True:
                ans = int(ans)
                if ans < 1 or ans > 5:
                    print("Opção inválida, tente novamente")
                    ans = input("Escolha sua opção: ")
                else:
                    break
            else:
                print("Opção inválida, tente novamente")
                ans = input("Escolha sua opção: ")

        #change the attributes
        if ans == 1:
            # making the options numeric
            lista = list(ficha_1["attributes"])

            #printing menu
            print("-"*30)
            print("Attributes:")
            cont = 1
            color_count = 0
            for x, y in ficha_1["attributes"].items():
                mod_att = escalonamento(-4, 0, 4, 1, 1, ficha_1["attributes"][x])
                cor = cores[color_count % len(cores)]
                print(f"{Fore.LIGHTMAGENTA_EX}{cont}{Style.RESET_ALL} - {cor}{x.capitalize()}{Style.RESET_ALL}: {y}, mod: {mod_att}", end=' | ')
                #just so it doesn't become a giant line of attributes
                if cont == 4:
                    print()
                    print()
                cont+=1
                color_count+=1
            print()

            #choose the attribute
            print("="*30)
            alt = input("O que você deseja alterar? (0 para cancelar) ")
            # validate the input
            while True:
                if validate_integer(alt) == True:
                    alt = int(alt)
                    if alt < 0 or alt > 8:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    alt = input("O que você deseja alterar? (0 para cancelar) ")
            if alt == 0:
                break

            #choose the value of the attribute
            valor = input(f"Digite o valor do atributo {lista[alt-1]}: (0 para cancelar) ")
            # validate the input
            while True:
                if validate_integer(valor) == True:
                    valor = int(valor)
                    if valor < 0 or valor > 20:
                        print("Opção inválida, tente novamente")
                        valor = input(f"Digite o valor do atributo {lista[alt-1]}: (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    valor = input(f"Digite o valor do atributo {lista[alt - 1]}: (0 para cancelar) ")
            if valor == 0:
                break

            ficha_1["attributes"][lista[alt - 1]] = valor

        #change the skills
        elif ans == 2:
            #making it numeric options
            lista = []
            for x in ficha_1["skills"].keys():
                lista += list(ficha_1["skills"][x])

            #printing menu
            print("-"*30)
            print("Skills:")
            cont = 1
            for i, x in enumerate(ficha_1["skills"]):
                cor = cores[i % len(cores)]
                print(cor, f"{x.capitalize()}:", Style.RESET_ALL)
                for y, z in ficha_1["skills"][x].items():
                    dominio = list(modificador[z].keys())
                    valor = list(modificador[z].values())
                    print(f" {Fore.LIGHTMAGENTA_EX}{cont}{Style.RESET_ALL} - {y.capitalize()} = {dominio[0].capitalize()}, {valor[0]}", end=' | ')
                    cont+=1
                print()

            print("-" * 30)
            alt = input("O que você deseja alterar? (0 para cancelar) ")
            # validate input
            while True:
                if validate_integer(alt) == True:
                    alt = int(alt)
                    if alt < 0 or alt > 31:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    alt = input("O que você deseja alterar? (0 para cancelar) ")
            if alt == 0:
                break

            # printing options
            print("=" * 30)
            print("""Maestrias:
    1 - Imperito
    2 - Adepto
    3 - Intermediário
    4 - Mestre""")
            print("-" * 30)
            # manual inputs skills
            ans = input(f"Digite o nível de maestria da perícia {lista[alt-1]}: (0 para cancelar) ")
            if ans == "0":
                break
            # validate the input
            while True:
                if validate_integer(ans) == True:
                    ans = int(ans)
                    if ans < 1 or ans > 4:
                        print("Opção inválida, tente novamente")
                        ans = input(f"Digite o nível de maestria da perícia {lista[alt-1]}: ")
                    else:
                        ans -= 1
                        break
                else:
                    print("Opção inválida, tente um número")
                    ans = input(f"Digite o nível de maestria da perícia {lista[alt-1]}: ")
            # changing the skill
            for x in ficha_1["skills"].items():
                for y, z in ficha_1["skills"][x[0]].items():
                    if lista[alt-1] == y:
                        ficha_1["skills"][x[0]][y] = ans

        #change the status
        elif ans == 3:
            #making it numeric options
            lista = []
            for x in ficha_2.keys():
                if x == "slots":
                    continue
                else:
                    lista.append(x)
            #printing menu
            print("="*30)
            print("Status")
            cont = 1
            for x, y in ficha_2.items():
                if x == "slots":
                    continue
                else:
                    print(f"{cont} - {x.capitalize()}: {y}")
                cont+=1

            print("-"*30)
            alt = input("O que você deseja alterar? (0 para cancelar) ")
            # validate input
            while True:
                if validate_integer(alt) == True:
                    alt = int(alt)
                    if alt < 0 or alt > 5:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    alt = input("O que você deseja alterar? (0 para cancelar) ")
            if alt == 0:
                break

            else:
                valor = input(f"Qual o novo valor de {lista[alt-1]}? (-1 para cancelar) ")
                #
                if valor == "-1":
                    break
                # validate input
                while True:
                    if validate_integer(valor) == True:
                        valor = int(valor)
                        ficha_2[lista[alt - 1]] = valor
                        break
                    else:
                        print("Opção inválida, digite um número")
                        valor = input(f"Qual o novo valor de {lista[alt-1]}? (-1 para cancelar) ")
                        if valor == "-1":
                            break

        #change other things
        elif ans == 4:
            global using_weight
            #making it numeric options
            lista = ["annotation", "weight", "inventory"]

            print("="*30)
            #printing options
            print("Others")
            for x, y in ficha_3.items():
                if x == "weight":
                    print(f"2 - {x.capitalize()}: {using_weight}/{y}")
                elif x == "inventory":
                    print(f"3 - {x.capitalize()}: ")
                    for z in range(len(ficha_3[x])):
                        for name, details in ficha_3[x][z].items():
                            print(" " * 3, f"{details[3]} ~ {name.title()} - Peso: {details[0]}, Valor: {details[1]}, Extra: {details[2]}")
                elif x == "annotation":
                    print(f"1 - {x.capitalize()}: {y.capitalize()}")

            print("-"*30)
            alt = input("O que você deseja alterar? (0 para cancelar) ")
            #validate input
            while True:
                if validate_integer(alt) == True:
                    alt = int(alt)
                    if alt < 0 or alt > 3:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente")
                    alt = input("O que você deseja alterar? (0 para cancelar) ")
            if alt == 0:
                break

            if lista[alt-1] == "inventory":
                while True:
                    print("="*30)
                    print(f"{lista[alt-1].title()}:\n1 - Adicionar item\n2 - Remover item\n3 - Alterar item\n4 - Sair")
                    print("-"*30)
                    ans = input("Escolha sua opção: ")
                    #add item
                    if ans == "1":
                        print("-"*30)
                        print("Adicionando: ")
                        name = input("Digite o nome do item: ")
                        details1 = input("Digite o peso do item: ")
                        # validate input
                        while True:
                            if validate_integer(details1) == True:
                                details1 = int(details1)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details1 = input(f"Digite o valor do item: ")
                        details2 = input("Digite o valor do item: ")
                        # validate input
                        while True:
                            if validate_integer(details2) == True:
                                details2 = int(details2)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details2 = input(f"Digite o valor do item: ")
                        details3 = input("Digite algo extra do item: ")
                        details4 = input("Digite a quantidade desse item: ")
                        # validate input
                        while True:
                            if validate_integer(details4) == True:
                                details4 = int(details4)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details4 = input("Digite a quantidade desse item: ")
                        ficha_3[lista[alt - 1]].append({f"{name}": [details1, details2, details3, details4]})
                    #remove item
                    elif ans == "2":
                        # printing options
                        print(f"Removendo {lista[alt - 1].capitalize()}: ")
                        cont = 0
                        for z in range(len(ficha_3[lista[alt - 1]])):
                            cont += 1
                            for name, details in ficha_3[lista[alt - 1]][z].items():
                                print(" ", f"{cont} - {name.title()} - Peso: {details[0]}, Valor: {details[1]}, Extra: {details[2]}")

                        print("-" * 30)
                        ans = input("Escolha sua opção: (0 para cancelar) ")
                        # validate input
                        while True:
                            if validate_integer(ans) == True:
                                ans = int(ans)
                                if ans < 0 or ans > len(ficha_3[lista[alt - 1]]):
                                    print("Opção inválida, tente novamente")
                                    ans = input("Escolha sua opção: (0 para cancelar) ")
                                else:
                                    break
                            else:
                                print("Opção inválida, tente novamente")
                                ans = input("Escolha sua opção: (0 para cancelar) ")
                        if ans == 0:
                            break
                        ficha_3[lista[alt - 1]].pop(ans - 1)
                    #change item
                    elif ans == "3":
                        # printing options
                        print(f"Alterando {lista[alt - 1].capitalize()}: ")
                        cont = 0
                        for z in range(len(ficha_3[lista[alt - 1]])):
                            cont += 1
                            for name, details in ficha_3[lista[alt - 1]][z].items():
                                print(" ",
                                      f"{cont} - {name.title()} - Peso: {details[0]}, Valor: {details[1]}, Extra: {details[2]}")

                        print("-" * 30)
                        ans = input("Escolha sua opção: (0 para cancelar) ")
                        # validate input
                        while True:
                            if validate_integer(ans) == True:
                                ans = int(ans)
                                if ans < 0 or ans > len(ficha_3[lista[alt - 1]]):
                                    print("Opção inválida, tente novamente")
                                    ans = input("Escolha sua opção: (0 para cancelar) ")
                                else:
                                    break
                            else:
                                print("Opção inválida, tente novamente")
                                ans = input("Escolha sua opção: (0 para cancelar) ")
                        if ans == 0:
                            break
                        name = input(f"Digite o nome do item: (-1 para cancelar) ")
                        if name == "-1":
                            break

                        details1 = input(f"Digite o peso do item: (-1 para cancelar) ")
                        # validate input
                        while True:
                            if validate_integer(details1) == True:
                                details1 = int(details1)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details1 = input(f"Digite o peso do item: ")
                        if details1 == -1:
                            break

                        details2 = input(f"Digite o valor do item: (-1 para cancelar) ")
                        # validate input
                        while True:
                            if validate_integer(details2) == True:
                                details2 = int(details2)
                                break
                            else:
                                print("Opção inválida, tente novamente")
                                details2 = input(f"Digite o valor do item: ")
                        if details2 == -1:
                            break

                        details3 = input(f"Digite algo extra do item: (-1 para cancelar) ")
                        if details3 == "-1":
                            break

                        ficha_3[lista[alt - 1]][ans-1] = ({f"{name}": [details1, details2, details3]})

                    elif ans == "4":
                        break
                    else:
                        print("Opção inválida, tente novamente")
                        print("Escolha sua opção: ")
            elif lista[alt-1] == "weight":
                ans = input(f"Digite o novo valor de {lista[alt-1]}: (0 para cancelar) ")
                # validate input
                while True:
                    if validate_integer(alt) == True:
                        alt = int(alt)
                        break
                    else:
                        print("Opção inválida, tente novamente")
                        alt = input("O que você deseja alterar? (0 para cancelar) ")
                if ans == 0:
                    break
                ficha_3[lista[alt-1]] = ans
            elif lista[alt-1] == "annotation":
                ans = input("O que você deseja escrever? (0 para cancelar) ")
                if ans == "0":
                    break
                ficha_3[lista[alt - 1]] = ans

            using_weight = 0
            for x in range(len(ficha_3["inventory"])):
                for item in ficha_3["inventory"][x]:
                    using_weight += (abs(ficha_3["inventory"][x][item][0])*abs(ficha_3["inventory"][x][item][3]))

        #bye bye
        elif ans == 5:
            break

#saving just some things from battle_mode
def salvar_simples():
    # saving basics
    with open("dados/basics.txt", "w", encoding="utf-8") as f:
        salvante = []
        for item, valor in ficha_1.items():
            if item == "attributes" or item == "skills":
                pass
            else:
                if validate_integer(valor) == True:
                    valor = str(valor)
                salvante.append(valor)
        f.write("#".join(salvante))
    # saving others
    with open("dados/others.txt", "w", encoding="utf-8") as f:
        salvante = []
        for item, valor in ficha_3.items():
            if item == "annotation" or item == "weight" or item == "lore":
                salvante.append(str(valor))
        f.write("#".join(salvante))
    # saving inventory
    with open("dados/inventory.txt", "w", encoding="utf-8") as f:
        # inventory order = "name": [weight, value, extra info, quantity]
        lista_itens = []
        for habilidades in ficha_3["inventory"]:
            for nome, detalhes in habilidades.items():
                lista_itens.append(nome)
                for x in detalhes:
                    lista_itens.append(str(x))
        f.write("#".join(lista_itens))
    # saving some extra things
    with open("dados/extra.txt", "w", encoding="utf-8") as f:
        lista_extras = [str(hp_atual), str(sp_atual), str(skill_points), str(using_weight), str(ficha)]
        f.write("#".join(lista_extras))


def battle_mode():
    global hp_atual
    global sp_atual
    turns = 1
    dmg = []
    dura_dmg = []
    regen = []
    dura_regen = []
    while True:
        total_dmg = 0
        total_regen = 0
        print("="*30)
        papa(hp_atual, sp_atual)
        print("-"*30)
        print("VOCÊ ESTÁ NO MODO BATALHA, NENHUMA ALTERAÇÃO FEITA SERÁ SALVA! ") #maybe some will be saved
        print(f"Turno = {turns}°\n  1 - Passar turno\n  2 - Girar dado\n  3 - Dano/Regeneração\n  4 - Mostrar itens e magias\n  5 - Editar ficha\n  6 - Sair")
        for x in dmg:
            total_dmg += x
        for x in regen:
            total_regen += x
        total = total_regen - total_dmg
        if total < 0:
            print("Dano por turno total:", abs(total))
        elif total > 0:
            print("Regeneração por turno total:", abs(total))

        print("-"*30)
        ans = input("Escolha uma opção: ")

        # pass the turn, take damage? regenerate if have it
        if ans == "1":
            while True:
                print("Deseja passar o turno?\n1 - Sim\n2 - Não")
                alt = input("Escolha sua opção: ")
                if alt == "1":
                    #THINK LATER TO MAKE IT BETTER
                    gasto = input("Qual foi seu gasto de mana? ")
                    #validate input
                    while True:
                        if validate_integer(gasto) == True:
                            gasto = int(gasto)
                            break
                        else:
                            print("Valor inválido, tente novamente.")
                            gasto = input("Qual foi seu gasto de mana? ")
                    sp_atual -= gasto
                    turns += 1
                    # taking dmg per turn
                    for x in range(len(dmg)):
                        hp_atual -= dmg[x]
                        dura_dmg[x] -= 1
                        if dura_dmg[x] == 0:
                            dura_dmg.pop(x)
                            dmg.pop(x)
                    # receiving regen per turn
                    for x in range(len(regen)):
                        hp_atual += regen[x]
                        dura_regen[x] -= 1
                        if dura_regen[x] == 0:
                            dura_regen.pop(x)
                            regen.pop(x)
                    if hp_atual > ficha_2["HP"]/2:
                        ficha_1["situation"] = "Alive/Healthy"
                    elif ficha_2["HP"]/2 >= hp_atual > 0:
                        ficha_1["situation"] = "Alive/Hurt"
                    elif 0 >= hp_atual:
                        ficha_1["situation"] = "Dead"
                    break
                elif alt == "2":
                    break
                else:
                    print("Opção inválida, tente novamente")
        # roll dice
        elif ans == "2":
            dice_roll()
        # suffer damage, ticks damage per turn? or make it only when presses "next turn"
        elif ans == "3":
            while True:
                print("-"*30)
                print("DANO OU REGENERAÇÃO POR TURNO:\n1 - Definir dano por turno\n2 - Definir regeneração por turno\n3 - Sair")
                print("-"*30)
                alt = input("Escolha uma opção: ")
                #damage per turn
                if alt == "1":
                    while True:
                        print("="*30)
                        print("Dano por turno:\n1 - Adicionar dano\n2 - Remover dano\n3 - Alterar dano\n4 - Sair")
                        ans = input("Escolha uma opção: ")
                        #add dmg
                        if ans == "1":
                            print("-"*30)
                            print("Adicionando - ")
                            # damage
                            opt = input("Digite o dano por turno: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(opt) == True:
                                    opt = int(opt)
                                    if opt < 0:
                                        print("Opção inválida, tente novamente")
                                        opt = input("Digite o dano por turno: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    opt = input("Digite o dano por turno: (0 para cancelar) ")
                            if opt == 0:
                                break
                            dmg.append(opt)

                            # duration
                            opt = input("Digite a duração do dano: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(opt) == True:
                                    opt = int(opt)
                                    if opt < 0:
                                        print("Opção inválida, tente novamente")
                                        opt = input("Digite a duração do dano: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    opt = input("Digite a duração do dano: (0 para cancelar) ")
                            if opt == 0:
                                break
                            dura_dmg.append(opt)

                        #rmv dmg
                        elif ans == "2":
                            print("-" * 30)
                            print("Removendo:")
                            for x in range(len(dmg)):
                                print(f"{x+1} - Dano: {dmg[x]}, Duração: {dura_dmg[x]}")
                            opt = input("Escolha uma opção: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(opt) == True:
                                    opt = int(opt)
                                    if opt < 0 or opt > len(dmg):
                                        print("Opção inválida, tente novamente")
                                        opt = input("Escolha uma opção: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    opt = input("Escolha uma opção: (0 para cancelar) ")
                            if opt == 0:
                                break
                            dmg.pop(opt-1)
                            dura_dmg.pop(opt - 1)

                        #chg dmg
                        elif ans == "3":
                            print("-" * 30)
                            print("Alterando:")
                            for x in range(len(dmg)):
                                print(f"{x+1} - Dano: {dmg[x]}, Duração: {dura_dmg[x]}")
                            opt = input("Escolha uma opção: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(opt) == True:
                                    opt = int(opt)
                                    if opt < 0 or opt > len(dmg):
                                        print("Opção inválida, tente novamente")
                                        opt = input("Escolha uma opção: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    opt = input("Escolha uma opção: (0 para cancelar) ")
                            if opt == 0:
                                break
                            # damage
                            esc = input("Digite o dano por turno: (0 para cancelar) ")
                            # validate the input
                            while True:
                                    if validate_integer(esc) == True:
                                        esc = int(esc)
                                        if esc < 0:
                                            print("Opção inválida, tente novamente")
                                            esc = input("Digite o dano por turno: (0 para cancelar) ")
                                        else:
                                            break
                                    else:
                                        print("Opção inválida, tente novamente")
                                        esc = input("Digite o dano por turno: (0 para cancelar) ")
                            if esc == 0:
                                break
                            dmg[opt-1] = esc

                            # duration
                            esc = input("Digite a duração do dano: (0 para cancelar) ")
                            # validate the input
                            while True:
                                    if validate_integer(esc) == True:
                                        esc = int(esc)
                                        if esc < 0:
                                            print("Opção inválida, tente novamente")
                                            esc = input("Digite a duração do dano: (0 para cancelar) ")
                                        else:
                                            break
                                    else:
                                        print("Opção inválida, tente novamente")
                                        esc = input("Digite a duração do dano: (0 para cancelar) ")
                            if esc == 0:
                                break
                            dura_dmg[opt-1] = esc

                        #bye bye
                        elif ans == "4":
                            break
                        else:
                            print("Opção inválida, tente novamente.")

                #regen per turn
                elif alt == "2":
                    while True:
                        print("=" * 30)
                        print("Regeneração por turno:\n1 - Adicionar regeneração\n2 - Remover regeneração\n3 - Alterar regeneração\n4 - Sair")
                        ans = input("Escolha uma opção: ")
                        #add regen
                        if ans == "1":
                            print("-" * 30)
                            print("Adicionando - ")
                            #regen
                            opt = input("Digite a regeneração por turno: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(opt) == True:
                                    opt = int(opt)
                                    if opt < 0:
                                        print("Opção inválida, tente novamente")
                                        opt = input("Digite a regeneração por turno: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    opt = input("Digite a regeneração por turno: (0 para cancelar) ")
                            if opt == 0:
                                break
                            regen.append(opt)

                            #duration
                            opt = input("Digite a duração da regeneração: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(opt) == True:
                                    opt = int(opt)
                                    if opt < 0:
                                        print("Opção inválida, tente novamente")
                                        opt = input("Digite a duração da regeneração: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    opt = input("Digite a duração da regeneração: (0 para cancelar) ")
                            if opt == 0:
                                break
                            dura_regen.append(opt)
                        #rmv regen
                        elif ans == "2":
                            print("-" * 30)
                            print("Removendo:")
                            for x in range(len(regen)):
                                print(f"{x + 1} - Regeneração: {regen[x]}, Duração: {dura_regen[x]}")
                            opt = input("Escolha uma opção: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(opt) == True:
                                    opt = int(opt)
                                    if opt < 0 or opt > len(regen):
                                        print("Opção inválida, tente novamente")
                                        opt = input("Escolha uma opção: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    opt = input("Escolha uma opção: (0 para cancelar) ")
                            if opt == 0:
                                break
                            regen.pop(opt - 1)
                            dura_regen.pop(opt - 1)
                        #chg regen
                        elif ans == "3":
                            print("-" * 30)
                            print("Alterando:")
                            for x in range(len(regen)):
                                print(f"{x + 1} - Regeneração: {regen[x]}, Duração: {dura_regen[x]}")
                            opt = input("Escolha uma opção: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(opt) == True:
                                    opt = int(opt)
                                    if opt < 0 or opt > len(regen):
                                        print("Opção inválida, tente novamente")
                                        opt = input("Escolha uma opção: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    opt = input("Escolha uma opção: (0 para cancelar) ")
                            if opt == 0:
                                break
                            # damage
                            esc = input("Digite a regeneração por turno: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(esc) == True:
                                    esc = int(esc)
                                    if esc < 0:
                                        print("Opção inválida, tente novamente")
                                        esc = input("Digite a regeneração por turno: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    esc = input("Digite a regeneração por turno: (0 para cancelar) ")
                            if esc == 0:
                                break
                            regen[opt - 1] = esc

                            # duration
                            esc = input("Digite a duração da regeneração: (0 para cancelar) ")
                            # validate the input
                            while True:
                                if validate_integer(esc) == True:
                                    esc = int(esc)
                                    if esc < 0:
                                        print("Opção inválida, tente novamente")
                                        esc = input("Digite a regeneração por turno: (0 para cancelar) ")
                                    else:
                                        break
                                else:
                                    print("Opção inválida, tente novamente")
                                    esc = input("Digite a regeneração por turno: (0 para cancelar) ")
                            if esc == 0:
                                break
                            dura_regen[opt - 1] = esc
                        #bye bye
                        elif ans == "4":
                            break
                        else:
                            print("Opção inválida, tente novamente")

                #bye bye
                elif alt == "3":
                    break

                #womp womp
                else:
                    print("opção inválida tente novamente")
        # show inventory, magics, etc. - OK
        elif ans == "4":
            pepe()
            input("Enter para continuar")

        # create a new function, just to limit the number of things you can edit, or let it all...? THINK LATER
        elif ans == "5":
            edit_junior()

        # bye bye
        elif ans == "6":
            alt = input("Tem certeza que deseja sair? As alterações serão apagadas.\n1 - SIM\n2 - NÃO")
            if alt == "1":
                break
            elif alt == "2":
                print()
            else:
                print("Opção inválida, tente novamente.")
                alt = input("Tem certeza que deseja sair? As alterações serão apagadas.\n1 - SIM\2n - NÃO")
        # womp womp
        else:
            print("Opção inválida, tente novamente.")
            sleep(1)
    salvar_simples()
    #SALVAR, MAS SÓ HP E SP ATUAL, SITUAÇÃO DE VIDA, INVENTÁRIO, QUANTIDADE DO INVENTÁRIO... algumas coisas ai
    #salvar extra, basics, inventory, weight (others),

"""
Ficha = 
Nome
Nível  1 - 20
Atributos + Modificadores
Perícias + Modificadores
Raça/origem
Carga
Situação (machucado, inconsciente...)
"""
"""
PV
PE (MANA)
Deslocamento
Armadura / RESISTÊNCIA A DANO
Combate rápido (equipamentos/magias principais/habilidades)
"""
"""
Inventário
Lugar pra anotação (proficiencias, informações que o jogador quiser colocar, personalizável)
Lore
Magias (todas)
Habilidades físicas
"""

"""
Força
Agilidade
Resistência
Coordenação
Espírito
Percepção
Intelecto
Carisma

Atletismo
Luta corporal
Esgrima Pesada
Esgrima leve
Arremessar

Reflexo
Furtividade
Acrobacia

Montaria
Pontaria
Fechaduras
Furtar

Fôlego
Tolerância
Defender

Canalização
Evocação
Transmutação
Visualização

Intuição
Investigação

Memória
Raciocínio
Vontade
Conhecimento

Domesticar
Manipulação
Intimidação
Diplomacia
Performance
Sedução
"""

while True:
    try:
        carregar()
    except:
        pass
    print("=" * 30)
    print("Sistema de ficha - Genesis")
    print("=" * 30)
    print("Escolha sua opção: ")
    print("1 - Rolagem de dado")
    print("2 - Ver ficha")
    print("3 - Editar ficha")
    print("4 - Modo batalha")
    print("5 - Criar ficha")
    print("6 - Salvar")
    print("7 - Sair")
    print("-" * 30)
    ans = input("Sua opção: ")

    # validate the input
    while True:
        if validate_integer(ans) == True:
            ans = int(ans)
            break
        else:
            print("Opção inválida, tente novamente")
            ans = input("Sua opção: ")

    #roll dice
    if ans == 1:
        dice_roll()
    #see CS
    elif ans == 2:
        if ficha == False:
            print("Você não possui ficha, crie uma.")
            sleep(1)
        else:
            show_character_sheet()
    #edit CS
    elif ans == 3:
        if ficha == False:
            print("Você não possui ficha, crie uma.")
            sleep(1)
        else:
            edit_character_sheet()
    #battle mode
    elif ans == 4:
        if ficha == False:
            print("Você não possui ficha, crie uma.")
            sleep(1)
        else:
            battle_mode()
    #create CS
    elif ans == 5:
        if ficha == True:
            ans = input("Você já possui ficha, deseja criar outra e substituir a atual?\n1 - SIM\n2 - NÃO\n")
            #validate input
            while True:
                if validate_integer(ans) == True:
                    ans = int(ans)
                    if ans > 2 or ans < 1:
                        print("Opção inválida, tente novamente.")
                        ans = input(
                            "Você já possui ficha, deseja criar outra e substituir a atual?\n1 - SIM\n2 - NÃO\n")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente.")
                    ans = input("Você já possui ficha, deseja criar outra e substituir a atual?\n1 - SIM\n2 - NÃO\n")
            if ans == 1:
                print("Nova ficha será criada.")
                character_sheet()
        else:
            ans = input("Você não possui uma ficha, deseja criar uma?\n1 - SIM\n2 - NÃO\n")
            #validate input
            while True:
                if validate_integer(ans) == True:
                    ans = int(ans)
                    if ans > 2 or ans < 1:
                        print("Opção inválida, tente novamente.")
                        ans = input("Você não possui uma ficha, deseja criar uma?\n1 - SIM\n2 - NÃO\n")
                    else:
                        break
                else:
                    print("Opção inválida, tente novamente.")
                    ans = input("Você não possui uma ficha, deseja criar uma?\n1 - SIM\n2 - NÃO\n")
            if ans == 1:
                character_sheet()
    #save
    elif ans == 6:
        """if ficha == False:
            print("Você não possui ficha, crie uma.")
            sleep(1)
        else:
            ans = int(input("Deseja salvar e substituir o salvamento anterior?\n1 - SIM\n2 - NÃO\n"))
            if ans == 1:
                print("Ainda n tem nada :3")"""
        salvar()
        #SALVAR_manual()

    #exit
    elif ans == 7:
        print("Saindo...")
        sleep(1)
        break
    else:
        print("Opção inválida, tente novamente")
        sleep(1)
