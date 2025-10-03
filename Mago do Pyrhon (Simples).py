import random

def main():
    vida = 100
    vida2 = 100
    vidainimigo = 100
    dano = 0
    danoinimigo = 0
    acerto = 0
    acertoinimigo = 0
    opcao = 0
    opcaoinimigo = 0
    chancejogador = 0
    chanceinimigo = 0
    pocaousos = 2

    while vida > 0 and vidainimigo > 0:
        print(f"\nVida do jogador: {vida} | Vida do inimigo: {vidainimigo}")
        print("\nEscolha seu feitiço:")
        print("1 - Bola de Fogo (dano: 30, acerto de 60%)")
        print("2 - Raio Congelante (dano: 20, acerto de 80%)")
        print("3 - Chuva de Meteoros (dano: 50, acerto de 30%)")
        print("4 - Poção de cura (Recupera 35 de vida)")
        
        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Opção inválida. Tente novamente.")
            continue

        # Define o dano e a chance de acerto do jogador
        if opcao == 1:
            print("Você lançou Bola de Fogo ......")
            dano = 30
            acerto = 60
        elif opcao == 2:
            print("Você lançou Raio Congelante ......")
            dano = 20
            acerto = 80
        elif opcao == 3:
            print("Você lançou Chuva de Meteoros ......")
            dano = 50
            acerto = 30
        elif opcao == 4:
            if pocaousos > 0:
                pocaousos -= 1
                print(f"Poção usada, restam {pocaousos} poções")
                dano = 0
                acerto = 100
                if vida <= 65:
                    vida += 35
                else:
                    vida = vida2
            else:
                print("\nLimite de poções atingido....")
                dano = 0
                acerto = 0
        else:
            print("Feitiço inválido")
            dano = 0
            acerto = 0

        # Sorteia o acerto do jogador
        chancejogador = random.randint(1, 100)
        if chancejogador <= acerto:
            print(f"\nVocê acertou e causou {dano} de dano!")
            vidainimigo -= dano
        else:
            print("\nVocê errou o feitiço! :(")

        if vidainimigo <= 0:
            break

        # Inimigo ataca
        opcaoinimigo = random.randint(1, 3)

        if opcaoinimigo == 1:
            print("\nInimigo lançou Bola de Fogo ......")
            danoinimigo = 30
            acertoinimigo = 60
        elif opcaoinimigo == 2:
            print("\nInimigo lançou Raio Congelante ......")
            danoinimigo = 20
            acertoinimigo = 80
        elif opcaoinimigo == 3:
            print("\nInimigo lançou Chuva de Meteoros ......")
            danoinimigo = 50
            acertoinimigo = 30

        # Sorteia o acerto do inimigo
        chanceinimigo = random.randint(1, 100)
        if chanceinimigo <= acertoinimigo:
            print(f"\nInimigo acertou e causou {danoinimigo} de dano!")
            vida -= danoinimigo
        else:
            print("\nO inimigo errou o feitiço!")

    # Resultado final
    if vida <= 0:
        print("\nVocê perdeu o combate!")
    elif vidainimigo <= 0:
        print("\nVocê venceu o combate!")

if __name__ == "__main__":
    main()