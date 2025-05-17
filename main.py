from random import randint
from time import sleep

ficha = True
ficha_1 = {"player": "", "name": "", "level": 0, "attributes_point": 0,
           "attributes": {"strength": 0,
                          "agility": 0,
                          "endurance": 0,
                          "dexterity": 0,
                          "spirit": 0,
                          "perception": 0,
                          "intelligence": 0,
                          "charisma": 0},
           "skills": {
               "strength": {"athletics": 0,
                            "fighting": 0,
                            "weapons_heavy": 0,
                            "weapons_light": 0,
                            "throwing": 0},
               "agility": {"reflex": 0,
                           "stealth": 0,
                           "acrobatics": 0},
               "endurance": {"breath": 0,
                             "tolerance": 0,
                             "defending": 0, },
               "dexterity": {"mounting": 0,
                             "aiming": 0,
                             "lockpicking": 0,
                             "pickpocket": 0},
               "spirit": {"channeling": 0,
                          "summon": 0,
                          "transmutation": 0,
                          "magic_senses": 0},
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
           "race": "", "background": "", "situation": "Alive"}
ficha_2 = {"HP": 0, "SP": 0, "speed": 0, "armor": 0, "resistance": 0, "slots": {}}
ficha_3 = {"annotation": "", "magic": [], "ability": [], "weight": 0, "inventory": [], "lore": ""}
favorites = {}
# favorites order = "number": [sides / modifier / number of rolls]

"""def titulo_estilo_1(texto):

    print()"""

# A way to test the type of success, a unique mechanic from our system
def sucess(dice, mod, cd):
    soma = dice + mod - cd
    result = ''
    if dice == 1:
        result = 'Fracasso Extremo'
    elif soma <= -10:
        result = 'Fracasso Crítico'
    elif -9 <= soma <= -1:
        result = 'Fracasso'
    elif 9 >= soma >= 0:
        result = 'Sucesso'
    elif 20 > soma >= 10:
        result = 'Sucesso Crítico'
    elif dice == 20:
        result = 'Sucesso Extremo'
    return result

# ok
def dice_roll():
    while True:
        result = []
        total = 0

        print("=" * 30)
        print("Rolagem de dados - Genesis")
        print("-" * 30)
        print("1 - Rolagem rápida (dados pré-definidos)")
        print("2 - Rolagem customizada")
        print("3 - Favoritar")
        print("4 - sair")
        print("-" * 30)
        ans = input("Escolha sua opção: ")

        # validate the input
        while True:
            if validate_integer(ans) == True:
                ans = int(ans)
                if ans < 1 or ans > 4:
                    print("Opção inválida, tente novamente")
                    ans = input("Escolha sua opção: ")
                else:
                    break
            else:
                print("Opção inválida, tente novamente")
                ans = input("Escolha sua opção: ")

        # fast roll - ok
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
            while True:
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
            # cancel, back to main menu
            if ans == 0:
                break

            # Using basic rolls
            if 9 >= ans >= 1:
                # choose the roll/modifier quantities
                quant = 3  # input("Digite a quantidade de rolagens: ")
                mod = 1  # input("Digite a quantidade do modificador: ")
                cd = 5  # int(input("Digite o nível de desafio do teste ou armadura: ")) #PRECISA VALIDAR

                # validate the input
                while True:
                    if validate_integer(quant) == True and validate_integer(mod) == True and validate_integer(cd):
                        quant = int(quant)
                        mod = int(mod)
                        cd = int(cd)
                        break
                    else:
                        print("Opção inválida, tente novamente")
                        quant = input("Digite a quantidade de rolagens: ")
                        mod = input("Digite a quantidade do modificador: ")
                        cd = input("Digite o nível de desafio do teste ou armadura: ")

                # rolling dices and printing results
                for x in range(quant):
                    result.append(randint(1, basic_rolls[ans - 1]))
                    soma = result[x] + mod - cd
                    print(f"{result[x]} + {mod} - {cd} = {soma}", end='')
                    if basic_rolls[ans - 1] == 20:
                        print(f'; {sucess(result[x], mod, cd)}')
                    else:
                        total += result[x] + mod - cd
                        print()

                # printing some specified results
                print("-" * 30)
                if basic_rolls[ans - 1] != 20:
                    print(f"Total = {total}")
                else:
                    print(f"Maior = {max(result) + mod - cd}; {sucess(max(result), mod, cd)}")
                    print(f"Menor = {min(result) + mod - cd}; {sucess(min(result), mod, cd)}")

            # Using favorite ones
            else:
                alterado = False
                # if favorite without roll quantity
                if favorites[ans][2] <= 0:
                    favorites[ans][2] = 3  # input("Digite a quantidade de rolagens: ")

                    # validate the input
                    while True:
                        if validate_integer(favorites[ans][2]) == True:
                            favorites[ans][2] = int(favorites[ans][2])
                            break
                        else:
                            print("Opção inválida, tente novamente")
                            favorites[ans][2] = input("Digite a quantidade de rolagens: ")
                    alterado = True

                cd = 5  # input("Digite o nível de desafio do teste: ")
                # validate the input
                while True:
                    if validate_integer(cd) == True:
                        cd = int(cd)
                        break
                    else:
                        print("Opção inválida, tente novamente")
                        cd = input("Digite o nível de desafio ou armadura: ")

                # rolling dices and printing results
                for x in range(favorites[ans][2]):
                    result.append(randint(1, favorites[ans][0]))
                    soma = result[x] + favorites[ans][1] - cd
                    print(f"{result[x]} + {favorites[ans][1]} - {cd} = {soma}", end='')
                    if favorites[ans][0] == 20:
                        print(f"; {sucess(max(result), favorites[ans][1], cd)}")
                    else:
                        total += result[x] + favorites[ans][1] - cd
                        print()

                # printing some specified results
                print('-' * 30)
                if favorites[ans][0] != 20:
                    print(f"Total = {total}")
                else:
                    print(
                        f"Maior = {max(result) + favorites[ans][1] - cd}; {sucess(max(result), favorites[ans][1], cd)}")
                    print(
                        f"Menor = {min(result) + favorites[ans][1] - cd}; {sucess(max(result), favorites[ans][1], cd)}")

                # just to change back the number to zero, if it was changed.
                if alterado == True:
                    favorites[ans][2] = 0

        # custom roll - ok
        elif ans == 2:
            # make your choices
            lado = 20  # input("Quantos lados tem o dado? ")
            quant = input("Quantos dados serão jogados? ")
            mod = 1  # input("Quanto de modificador será adicionado? ")
            cd = 5  # input("Digite o nível de desafio do teste: ")

            # validate the input
            while True:
                if validate_integer(lado) == True and validate_integer(quant) == True and validate_integer(
                        mod) == True and validate_integer(cd) == True:
                    lado = int(lado)
                    quant = int(quant)
                    mod = int(mod)
                    cd = int(cd)
                    break
                else:
                    print("Opção inválida, tente novamente")
                    quant = input("Digite a quantidade de rolagens: ")
                    mod = input("Digite a quantidade do modificador: ")
                    lado = input("Quantos lados tem o dado? ")
                    cd = input("Digite o nível de desafio do teste ou armadura: ")

            # rolling dices and printing results!
            for x in range(quant):
                result.append(randint(1, lado))
                soma = result[x] + mod - cd
                print(f"{result[x]} + {mod} - {cd} = {soma}", end='')
                if lado == 20:
                    print(f"; {sucess(result[x], mod, cd)}")
                else:
                    total += result[x] + mod - cd
                    print()

            print('-' * 30)  # because the end
            if lado != 20:
                print(f"total = {total}")
            else:
                print(f"maior = {max(result) + mod - cd}; {sucess(max(result), mod, cd)}")
                print(f"menor = {min(result) + mod - cd}; {sucess(min(result), mod, cd)}")

        # creating, removing or changing a favorite roll - ok
        elif ans == 3:
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

                # just some predef favorites, to test. DELETE LATER
                if favorites == {}:
                    favorites[10] = [20, 1, 0]
                    favorites[11] = [20, 1, 2]
                    favorites[12] = [20, 1, 3]
                    favorites[13] = [12, 1, 4]

                # add favorite
                if ans == 1:
                    print("-" * 30)
                    print("Adicionar favorito:")

                    # make your choices
                    lado = input("Quantos lados terá dado? ")  # 20
                    mod = input("Quanto de modificador será adicionado? ")  # 1
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
                            if ans < min(favorites) or ans > max(favorites):
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
                            if ans < min(favorites) or ans > max(favorites):
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

                # just cancel
                elif ans == 4:
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
        elif ans == 4:
            break

        # DO IT AGAIN?! bye bye if did something
        print('-' * 30)
        ans = input("Deseja rolar outro dado?\n1 - SIM\n2 - NÃO\n     Sua opção: ")
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


def character_sheet(bruno="bruno"):
    print("Digite as informações: ")
    """if ficha == False:
        ans = input("Você não tem uma ficha, deseja criar uma? [S/N] ")
        if ans == "S":
            ficha_1["player"] = input("Digite o nome do player: ")
            ficha_1["name"] = input("Digite o nome do personagem: ")
            ficha_1["level"] = int(input("Digite o nível do personagem: "))

            if ficha_1["level"] == 1:
                ficha_1["attributes_point"] = 30
            else:
                ficha_1["attributes_point"] = 30 + (ficha_1["level"] - 1) * 2

            print(f"Você tem {ficha_1["attributes_point"]} pontos para distribuir nos atributos!")
            for x in ficha_1["attributes"]:
                #ficha_1["attributes"][x] = randint(1,20)
                ficha_1["attributes"][x] = int(input(f"Digite o valor do atributo {x}: "))
            for x in ficha_1["skills"]:
                for y in ficha_1["skills"][x]:
                    #ficha_1["skills"][x][y] = randint(1,20)
                    ficha_1["skills"][x][y] = int(input(f"Digite o valor da perícia {y}: "))
            ficha_1["race"] = input("Digite a raça dele: ")
            ficha_1["background"] = input("Qual a origem? ")
            ficha_1["situation"] = "Alive/Healthy"

            ficha_2["HP"] = ficha_1["attributes"]["endurance"] * 5
            ficha_2["SP"] = ficha_1["attributes"]["spirit"] * 2
            ficha_2["speed"] = ficha_1["attributes"]["agility"] * 3
            ficha_2["weight"] = ficha_1["attributes"]["strength"] * 5
            ficha_2["armor"] = 0
            ficha_2["resistance"] = 0
        """

    ficha_1["player"] = "Bruno"
    ficha_1["name"] = "Cícero"
    ficha_1["level"] = 1
    ficha_1["attributes_point"] = 30 + (ficha_1["level"] - 1) * 2
    for x in ficha_1["attributes"]:
        ficha_1["attributes"][x] = randint(1, 20)
        # ficha_1["attributes"][x] = int(input(f"Digite o valor do atributo {x}: "))
    for x in ficha_1["skills"]:
        for y in ficha_1["skills"][x]:
            ficha_1["skills"][x][y] = randint(1, 20)
            # ficha_1["skills"][x][y] = int(input(f"Digite o valor da perícia {y}: "))
    ficha_1["race"] = "Human"
    ficha_1["background"] = "Thief"
    ficha_1["situation"] = "Alive/Healthy"

    ficha_2["HP"] = ficha_1["attributes"]["endurance"] * 5
    ficha_2["SP"] = ficha_1["attributes"]["spirit"] * 2
    ficha_2["speed"] = ficha_1["attributes"]["agility"] * 3
    ficha_2["weight"] = ficha_1["attributes"]["strength"] * 5
    ficha_2["armor"] = 5
    ficha_2["resistance"] = 2

# ok
def show_character_sheet():
    print("-" * 30)
    print("Basics: ")
    for x, y in ficha_1.items():
        if x != "skills" and x != "attributes":
            print(f"{x.capitalize()}: {y}")

    print("=" * 30)
    print("Attributes:")
    for x, y in ficha_1["attributes"].items():
        print(f"{x.capitalize()} = {y}")

    print("=" * 30)
    print("Skills:")
    for x in ficha_1["skills"].keys():
        print(f"{x.capitalize()}:")
        for y in ficha_1["skills"][x]:
            print(f"{y.capitalize()} = {ficha_1["skills"][x][y]}", end=' | ')
        print()

    print("=" * 30)
    print("Status: ")
    for x, y in ficha_2.items():
        print(f"{x.capitalize()}: {y}")

    print("=" * 30)
    print("Outros:")
    for x, y in ficha_3.items():
        print(f"{x.capitalize()}: {y}")


def edit_character_sheet():
    character_sheet()
    while True:
        print("=" * 30)
        print("""O que deseja alterar?
        1 - Basics (Name, level, race...)
        2 - Attributes (Strength, agility, spirit...)
        3 - Skills (athletics, memory, seduction...)
        4 - Status (HP, armor, favorites...)
        5 - Outros (Annotation, magic, inventory...)
        6 - Sair""")
        print("=" * 50)
        ans = input("Digite sua opção: ")
        print("-" * 30)
        if ans == "1":
            print("Basics:")
            for x, y in ficha_1.items():
                if x != "skills" and x != "attributes":
                    print(f"{x.capitalize()}: {y}")
            alt = input("O que você deseja alterar? (Digite o nome da característica) ")
            ficha_1[alt] = input(f"Qual o novo {alt}? ")

        elif ans == "2":
            print("Attributes:")
            for x, y in ficha_1["attributes"].items():
                print(f"{x.capitalize()}: {y}", end=' | ')
            print()
            alt = input("O que você deseja alterar? (Digite o nome do atributo) ")
            ficha_1["attributes"][alt] = input(f"Qual o novo {alt}? ")

        elif ans == "3":
            print("Skills:")
            for x in ficha_1["skills"].keys():
                print(f"{x.capitalize()}:")
                for y in ficha_1["skills"][x]:
                    print(f"{y.capitalize()} = {ficha_1["skills"][x][y]}", end=' | ')
                print()
            alt = input("O que você deseja alterar? (Digite o nome da perícia) ")
            # provisório
            ficha_1["skills"]["strength"][alt] = int(input(f"Qual o novo {alt}? "))
            # ficha[] fazer algum sistema para procurar?

        elif ans == "4":
            print("Status")
            for x, y in ficha_2.items():
                print(f"{x.capitalize()}: {y}")
            alt = input("O que você deseja alterar? (Digite o nome do status) ")
            if alt == "slots":
                item = input("Qual o novo atalho? (nome da espada, magia, etc...) ")
                rol = input("Qual a rolagem? (Ex.: 1d20+5) ")
                prop = input("Qual a propriedade? (Dano, efeito...) ")
                ficha_2["slots"][item] = []
                ficha_2["slots"][item].append(rol)
                ficha_2["slots"][item].append(prop)
            else:
                ficha_2[alt] = input(f"Qual o novo {alt}? ")

        elif ans == "5":
            print("Outros")
            for x, y in ficha_3.items():
                print(f"{x.capitalize()}: {y}")
            alt = input("O que você deseja alterar? (Digite nome) ")
            if alt == "magic" or alt == "ability" or alt == "inventory":
                ficha_3[alt].append(input("O que você deseja escrever? "))
            else:
                ficha_3[alt] = input("O que você deseja escrever? ")

        elif ans == "6":
            save = input("Deseja salvar as alterações? [S/N]")
            if save == "N":
                break
            else:
                break


def battle_mod():
    print("VOCÊ ESTÁ NO MODO BATALHA, NENHUMA ALTERAÇÃO FEITA SERÁ SALVA! ")
    while True:
        print("=" * 30)
        print("""O que deseja alterar?
        1 - Basics (Name, level, race...)
        2 - Attributes (Strength, agility, spirit...)
        3 - Skills (athletics, memory, seduction...)
        4 - Status (HP, armor, favorites...)
        5 - Outros (Annotation, magic, inventory...)
        6 - Sair""")
        print("=" * 50)
        ans = input("Digite sua opção: ")
        print("-" * 30)
        if ans == "1":
            print("Basics:")
            for x, y in ficha_1.items():
                if x != "skills" and x != "attributes":
                    print(f"{x.capitalize()}: {y}")
            alt = input("O que você deseja alterar? (Digite o nome da característica) ")
            ficha_1[alt] = input(f"Qual o novo {alt}? ")

        elif ans == "2":
            print("Attributes:")
            for x, y in ficha_1["attributes"].items():
                print(f"{x.capitalize()}: {y}", end=' | ')
            print()
            alt = input("O que você deseja alterar? (Digite o nome do atributo) ")
            ficha_1["attributes"][alt] = input(f"Qual o novo {alt}? ")

        elif ans == "3":
            print("Skills:")
            for x in ficha_1["skills"].keys():
                print(f"{x.capitalize()}:")
                for y in ficha_1["skills"][x]:
                    print(f"{y.capitalize()} = {ficha_1["skills"][x][y]}", end=' | ')
                print()
            alt = input("O que você deseja alterar? (Digite o nome da perícia) ")
            # provisório
            ficha_1["skills"]["strength"][alt] = int(input(f"Qual o novo {alt}? "))
            # ficha[] fazer algum sistema para procurar?

        elif ans == "4":
            print("Status")
            for x, y in ficha_2.items():
                print(f"{x.capitalize()}: {y}")
            alt = input("O que você deseja alterar? (Digite o nome do status) ")
            if alt == "slots":
                item = input("Qual o novo atalho? (nome da espada, magia, etc...) ")
                rol = input("Qual a rolagem? (Ex.: 1d20+5) ")
                prop = input("Qual a propriedade? (Dano, efeito...) ")
                ficha_2["slots"][item] = []
                ficha_2["slots"][item].append(rol)
                ficha_2["slots"][item].append(prop)
            else:
                ficha_2[alt] = input(f"Qual o novo {alt}? ")

        elif ans == "5":
            print("Outros")
            for x, y in ficha_3.items():
                print(f"{x.capitalize()}: {y}")
            alt = input("O que você deseja alterar? (Digite nome) ")
            if alt == "magic" or alt == "ability" or alt == "inventory":
                ficha_3[alt].append(input("O que você deseja escrever? "))
            else:
                ficha_3[alt] = input("O que você deseja escrever? ")

        elif ans == "6":
            save = input("Deseja salvar as alterações? [S/N]")
            if save == "N":
                break
            else:
                break


def validate_integer(user_input):
    try:
        int(user_input)
    except:
        pass
    else:
        return True


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
    print("=" * 30)
    print("Sistema de ficha - Genesis")
    print("=" * 30)
    print("Escolha sua opção: ")
    print("1 - Rolagem de dado")
    print("2 - Ver ficha")
    print("3 - Editar ficha")
    print("4 - Modo batalha")
    print("5 - Sair")
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

    if ans == 1:
        dice_roll()
    elif ans == 2:
        show_character_sheet()
    elif ans == 3:
        edit_character_sheet()
    elif ans == 4:
        battle_mod()
    elif ans == 5:
        break
    else:
        print("Opção inválida, tente novamente")
        sleep(1)
