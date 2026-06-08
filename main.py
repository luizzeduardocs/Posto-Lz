from crud import cadastrar_abastecimento, listar_abastecimentos
from crud import buscar_abastecimento, editar_abastecimento
from crud import excluir_abastecimento, relatorio


def menu():
    """Mostra o menu principal do sistema."""
    print("\n====== POSTO LUIZÃO ======")
    print("1 - Cadastrar abastecimento")
    print("2 - Listar abastecimentos")
    print("3 - Buscar abastecimento")
    print("4 - Editar abastecimento")
    print("5 - Excluir abastecimento")
    print("6 - Relatório")
    print("0 - Sair")


def main():
    """Controla o funcionamento principal do sistema."""
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_abastecimento()
        elif opcao == "2":
            listar_abastecimentos()
        elif opcao == "3":
            buscar_abastecimento()
        elif opcao == "4":
            editar_abastecimento()
        elif opcao == "5":
            excluir_abastecimento()
        elif opcao == "6":
            relatorio()
        elif opcao == "0":
            print("Sistema encerrado. Volte sempre ao Posto Luizão!")
            break
        else:
            print("Opção inválida.")


main()
