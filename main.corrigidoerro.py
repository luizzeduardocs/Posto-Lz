TIPOS_COMBUSTIVEL = ("gasolina", "etanol", "diesel")

abastecimentos = []
ids_usados = set()


def ler_float(texto):
    """Lê um número decimal."""
    while True:
        try:
            valor = float(input(texto).replace(",", "."))
            if valor <= 0:
                print("Digite um valor maior que zero.")
            else:
                return valor
        except ValueError:
            print("Valor inválido.")


def ler_int(texto):
    """Lê um número inteiro."""
    while True:
        try:
            return int(input(texto))
        except ValueError:
            print("Digite um número inteiro válido.")


def gerar_id():
    """Gera um ID sem repetir."""
    novo_id = len(ids_usados) + 1

    while novo_id in ids_usados:
        novo_id += 1

    ids_usados.add(novo_id)
    return novo_id


def iniciais(nome):
    """Pega as iniciais do cliente usando slicing."""
    partes = nome.split()
    resultado = ""

    for parte in partes:
        resultado += parte[:1].upper()

    return resultado


def gerador(lista):
    """Percorre os registros com yield."""
    for item in lista:
        yield item


def calcular_total(litros, valor_litro):
    """Calcula o total do abastecimento."""
    return litros * valor_litro


def cadastrar():
    """Cadastra um abastecimento."""
    print("\n--- Cadastrar abastecimento ---")

    cliente = input("Nome do cliente: ").strip()

    if cliente == "":
        print("O nome não pode ficar vazio.")
        return

    print("\nCombustíveis disponíveis:")
    for tipo in TIPOS_COMBUSTIVEL:
        print("-", tipo)

    combustivel = input("Combustível: ").lower().strip()

    if combustivel not in TIPOS_COMBUSTIVEL:
        print("Combustível inválido.")
        return

    litros = ler_float("Quantidade de litros: ")
    valor_litro = ler_float("Valor por litro: R$ ")

    abastecimento = {
        "id": gerar_id(),
        "cliente": cliente,
        "iniciais": iniciais(cliente),
        "combustivel": combustivel,
        "litros": litros,
        "valor_litro": valor_litro,
        "total": calcular_total(litros, valor_litro),
        "pago": False
    }

    abastecimentos.append(abastecimento)
    print("Abastecimento cadastrado com sucesso!")


def listar():
    """Lista todos os abastecimentos."""
    print("\n--- Abastecimentos do Posto Luizão ---")

    if not abastecimentos:
        print("Nenhum abastecimento cadastrado.")
        return

    print("-" * 75)
    print("ID | Cliente        | Combustível | Litros | Valor/L | Total   | Pago")
    print("-" * 75)

    for item in gerador(abastecimentos):
        pago = "Sim" if item["pago"] else "Não"

        print(
            f'{item["id"]:<2} | '
            f'{item["cliente"][:14]:<14} | '
            f'{item["combustivel"]:<11} | '
            f'{item["litros"]:<6.2f} | '
            f'R${item["valor_litro"]:<6.2f} | '
            f'R${item["total"]:<6.2f} | '
            f'{pago}'
        )


def buscar_por_id(id_busca):
    """Busca um abastecimento pelo ID."""

    # Erro que encontrei:
    # Ao digitar letras no lugar do id, o programa apresentava ValueError
    # e poderia encerrar a execuçao. A correção foi feita com try/except,
    # convertendo o id para inteiro somente quando a entrada for válida.
    try:
        id_busca = int(id_busca)
    except ValueError:
        return None

    for item in abastecimentos:
        if item["id"] == id_busca:
            return item

    return None


def mostrar_item(item):
    """Mostra os dados de um abastecimento."""
    print("\nID:", item["id"])
    print("Cliente:", item["cliente"])
    print("Iniciais:", item["iniciais"])
    print("Combustível:", item["combustivel"])
    print("Litros:", item["litros"])
    print("Valor por litro: R$", f'{item["valor_litro"]:.2f}')
    print("Total: R$", f'{item["total"]:.2f}')
    print("Pago:", "Sim" if item["pago"] else "Não")


def buscar():
    """Busca abastecimento por ID ou nome."""
    print("\n--- Buscar abastecimento ---")
    opcao = input("Buscar por ID ou nome? ").lower().strip()

    if opcao == "id":
        id_busca = input("Digite o ID: ")
        item = buscar_por_id(id_busca)

        if item:
            mostrar_item(item)
        else:
            print("Registro não encontrado.")

    elif opcao == "nome":
        nome = input("Digite parte do nome: ").lower().strip()

        encontrados = [
            item for item in abastecimentos
            if nome in item["cliente"].lower()
        ]

        if encontrados:
            for item in encontrados:
                mostrar_item(item)
        else:
            print("Nenhum cliente encontrado.")
    else:
        print("Opção inválida.")


def editar():
    """Edita um abastecimento."""
    print("\n--- Editar abastecimento ---")
    id_busca = input("Digite o ID: ")
    item = buscar_por_id(id_busca)

    if item is None:
        print("Registro não encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")

    novo_nome = input("Novo nome do cliente: ").strip()
    if novo_nome != "":
        item["cliente"] = novo_nome
        item["iniciais"] = iniciais(novo_nome)

    novo_combustivel = input("Novo combustível: ").lower().strip()
    if novo_combustivel != "":
        if novo_combustivel in TIPOS_COMBUSTIVEL:
            item["combustivel"] = novo_combustivel
        else:
            print("Combustível inválido. Não alterado.")

    mudar_valores = input("Alterar litros e valor? [s/n]: ").lower().strip()

    if mudar_valores == "s":
        item["litros"] = ler_float("Nova quantidade de litros: ")
        item["valor_litro"] = ler_float("Novo valor por litro: R$ ")
        item["total"] = calcular_total(item["litros"], item["valor_litro"])

    pago = input("Está pago? [s/n]: ").lower().strip()

    if pago == "s":
        item["pago"] = True
    elif pago == "n":
        item["pago"] = False

    print("Registro atualizado com sucesso!")


def excluir():
    """Exclui um abastecimento."""
    print("\n--- Excluir abastecimento ---")
    id_busca = input("Digite o ID: ")
    item = buscar_por_id(id_busca)

    if item is None:
        print("Registro não encontrado.")
        return

    confirmar = input("Deseja excluir mesmo? [s/n]: ").lower().strip()

    if confirmar == "s":
        abastecimentos.remove(item)
        ids_usados.discard(item["id"])
        print("Registro excluído com sucesso.")
    else:
        print("Exclusão cancelada.")


def relatorio():
    """Mostra um relatório geral."""
    print("\n--- Relatório do Posto Luizão ---")

    if not abastecimentos:
        print("Não existem dados para o relatório.")
        return

    total_vendido = sum(item["total"] for item in abastecimentos)

    pendentes = [
        item for item in abastecimentos
        if item["pago"] is False
    ]

    resumo_litros = {
        tipo: sum(
            item["litros"] for item in abastecimentos
            if item["combustivel"] == tipo
        )
        for tipo in TIPOS_COMBUSTIVEL
    }

    print("Total vendido: R$", f"{total_vendido:.2f}")
    print("Abastecimentos pendentes:", len(pendentes))

    print("\nLitros vendidos por combustível:")
    for tipo, litros in resumo_litros.items():
        print(f"{tipo.capitalize()}: {litros:.2f} litros")


def menu():
    """Mostra o menu principal."""
    print("\n====== POSTO LUIZÃO ======")
    print("1 - Cadastrar abastecimento")
    print("2 - Listar abastecimentos")
    print("3 - Buscar abastecimento")
    print("4 - Editar abastecimento")
    print("5 - Excluir abastecimento")
    print("6 - Relatório")
    print("0 - Sair")


def main():
    """Função principal do sistema."""
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            buscar()
        elif opcao == "4":
            editar()
        elif opcao == "5":
            excluir()
        elif opcao == "6":
            relatorio()
        elif opcao == "0":
            print("Sistema encerrado. Obrigado por usar o Posto Luizão!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
