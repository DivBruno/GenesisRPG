from random import randint
ficha = True
ficha_1 = {"name": "", "level": 0,
           "attributes_point": 0,
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
                                  "defending": 0,},
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
                    "intelligence":{"memory": 0,
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


def dice_roll():
    while True:
        print("-" * 30)
        print("Rolagem de dados - Genesis")
        print("-" * 30)
        result = []
        basic_rolls = [2, 3, 4, 6, 8, 10, 12, 20, 100]
        #favorites order = "number": [sides / modifier / number of rolls]
        favorites = {}
        total = 0
        print("1 - Rolagem rápida - (dados pré-definidos)")
        print("2 - Rolagem customizada")
        print("3 - Favoritar")
        print("4 - sair")
        print("-" * 30)
        ans = int(input("Escolha sua opção: "))
        print("-" * 30)
        if ans == 1:
            print("=" * 30)
            print("Rolagens pré-definidas:")
            cont = 0
            for x in basic_rolls:
                cont += 1
                print(f"{cont} - d{x}", end = " | ")
            print()
            print("Rolagens favoritadas: ")
            print("=" * 30)
            for x in favorites:
                print(x)
            ans = int(input("Escolha sua opção: "))
        elif ans == 2:
            lado = 20  # int(input("Quantos lados tem o dado? "))
            quant = int(input("Quantos dados serão jogados? "))
            mod = 1  # int(input("Quanto de modificador será adicionado? "))

            for x in range(quant):
                result.append(randint(1, lado))
                soma = result[x] + mod
                print(f"{result[x]} + {mod} = {soma}")
                total += result[x]

            print()
            print(f"total = {total}")
            print(f"maior = {max(result)}")
            print(f"menor = {min(result)}")
            opcao = int(input("Deseja rolar outro dado?\n1 - SIM\n2 - NÃO\n     Sua opção: "))
            if opcao == 2:
                break
        elif ans == 3:
            print("Favoritar")
            print("1 - Adicionar uma rolada favorita")
            print("2 - Remover uma rolada favoritada")
            print("3 - Alterar uma rolada favoritada")
            print("4 - Sair")

            if ans == 1:
                lado = 20  # int(input("Quantos lados terá dado? "))
                mod = 1  # int(input("Quanto de modificador será adicionado? "))
                quant = int(input("Quantidade de rolagens [0 se não quiser definir]: "))
                favorites[f"{len(favorites)+1}"].append(lado)


            elif ans == 2:

            elif ans == 3:

            elif ans == 4:
                break

        elif ans == 4:
            break
        else:
            print("Opção inválida")

def character_sheet(bruno = "bruno"):
    print("_Digite as informações_ ")
    """if ficha == False:
        ans = input("Você não tem uma ficha, deseja criar uma? [S/N] ")
        if ans == "S":
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

    ficha_1["name"] = "Bruno"
    ficha_1["level"] = 2
    if ficha_1["level"] == 1:
        ficha_1["attributes_point"] = 30
    else:
        ficha_1["attributes_point"] = 30 + (ficha_1["level"] - 1) * 2
    for x in ficha_1["attributes"]:
        ficha_1["attributes"][x] = randint(1,20)
        #ficha_1["attributes"][x] = int(input(f"Digite o valor do atributo {x}: "))
    for x in ficha_1["skills"]:
        for y in ficha_1["skills"][x]:
            ficha_1["skills"][x][y] = randint(1,20)
            #ficha_1["skills"][x][y] = int(input(f"Digite o valor da perícia {y}: "))
    ficha_1["race"] = "Human"
    ficha_1["background"] = "Thief"
    ficha_1["situation"] = "Alive/Healthy"

    ficha_2["HP"] = ficha_1["attributes"]["endurance"] * 5
    ficha_2["SP"] = ficha_1["attributes"]["spirit"] * 2
    ficha_2["speed"] = ficha_1["attributes"]["agility"] * 3
    ficha_2["weight"] = ficha_1["attributes"]["strength"] * 5
    ficha_2["armor"] = 5
    ficha_2["resistance"] = 2

def show_character_sheet():
    print("-" * 30)
    print("Basics: ")
    for x, y in ficha_1.items():
        if x != "skills" and x != "attributes":
            print(f"{x.capitalize()}: {y}")

    print("="*30)
    print("Attributes:")
    for x, y in ficha_1["attributes"].items():
        print(f"{x.capitalize()} = {y}")

    print("="*30)
    print("Skills:")
    for x in ficha_1["skills"].keys():
        print(f"{x.capitalize()}:")
        for y in ficha_1["skills"][x]:
            print(f"{y.capitalize()} = {ficha_1["skills"][x][y]}", end = ' | ')
        print()

    print("="*30)
    print("Status: ")
    for x, y in ficha_2.items():
        print(f"{x.capitalize()}: {y}")

    print("=" * 30)
    print("Outros:")
    for x, y in ficha_3.items():
        print(f"{x.capitalize()}: {y}")

    print("-" * 30)

def edit_character_sheet():
    character_sheet()
    while True:
        print("="*30)
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
                print(f"{x.capitalize()}: {y}", end =' | ')
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
            #provisório
            ficha_1["skills"]["strength"][alt] = int(input(f"Qual o novo {alt}? "))
            #ficha[] fazer algum sistema para procurar?

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
    print("="*30)
    print("Sistema de ficha - Genesis")
    print("="*30)
    print("Escolha sua opção: ")
    print("1 - Rolagem de dado")
    print("2 - Ver ficha")
    print("3 - Editar ficha")
    print("4 - Modo batalha")
    print("5 - Sair")
    print("-"*30)
    opcao = int(input("Sua opção: "))

    if opcao == 1:
        dice_roll()
    elif opcao == 2:
        show_character_sheet()
    elif opcao == 3:
        edit_character_sheet()
    elif opcao == 4:
        battle_mod()
    elif opcao == 5:
        break
    else:
        print("Opção inválida")


