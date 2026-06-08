from dados import abastecimentos, TIPOS_COMBUSTIVEL, ids_usados
from utils import gerar_id, ler_float, ler_int, mostrar_iniciais
from utils import gerador_registros, calcular_total


def cadastrar_abastecimento():
    """Cadastra um novo abastecimento."""
    print("\n--- Novo abastecimento ---")

    cliente = input("Nome do cliente: ").strip()

    if cliente == "":
        print("O nome não pode ficar vazio.")
        return

    print("\nCombustíveis disponíveis:")
    for tipo in TIPOS_COMBUSTIVEL:
        print("-", tipo)

    combustivel = input("Tipo de combustível: ").lower().strip()

    if combustivel not in TIPOS_COMBUSTIVEL:
        print("Combustível inválido.")
        return

    litros = ler_float("Quantidade de litros: ")
    valor_litro = ler_float("Valor por litro: R$ ")

    total = calcular_total(litros, valor_litro)

    registro = {
        "id": gerar_id(),
        "cliente": cliente,
        "iniciais": mostrar_iniciais(cliente),
        "combustivel": combustivel,
        "litros": litros,
        "valor_litro": valor_litro,
        "total": total,
        "pago": False
    }

    abastecimentos.append(registro)

    print("\nAbastecimento cadastrado com sucesso!")


def listar_abastecimentos():
    """Lista todos os abastecimentos cadastrados."""
    print("\n--- Lista de abastecimentos - Posto Luizão ---")

    if not abastecimentos:
        print("Nenhum abastecimento cadastrado.")
        return

    print("-" * 78)
    print("ID | Cliente        | Combustível | Litros | Valor/L | Total   | Pago")
    print("-" * 78)

    for item in gerador_registros(abastecimentos):
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
    try:
        id_busca = int(id_busca)
    except ValueError:
        print("ID inválido.")
        return None

    for item in abastecimentos:
        if item["id"] == id_busca:
            return item

    return None


def buscar_abastecimento():
    """Busca abastecimento por ID ou nome do cliente."""
    print("\n--- Buscar abastecimento ---")
    opcao = input("Buscar por ID ou nome? ").lower().strip()

    if opcao == "id":
        id_busca = input("Digite o ID: ")
        item = buscar_por_id(id_busca)

        if item:
            mostrar_registro(item)
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
                mostrar_registro(item)
        else:
            print("Nenhum cliente encontrado.")

    else:
        print("Opção inválida.")


def mostrar_registro(item):
    """Mostra um registro completo."""
    print("\nID:", item["id"])
    print("Cliente:", item["cliente"])
    print("Iniciais:", item["iniciais"])
    print("Combustível:", item["combustivel"])
    print("Litros:", item["litros"])
    print("Valor por litro: R$", f'{item["valor_litro"]:.2f}')
    print("Total: R$", f'{item["total"]:.2f}')
    print("Pago:", "Sim" if item["pago"] else "Não")


def editar_abastecimento():
    """Edita um abastecimento existente."""
    print("\n--- Editar abastecimento ---")
    id_busca = input("Digite o ID: ")
    item = buscar_por_id(id_busca)

    if item is None:
        print("Registro não encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")

    novo_cliente = input("Novo nome do cliente: ").strip()
    if novo_cliente != "":
        item["cliente"] = novo_cliente
        item["iniciais"] = mostrar_iniciais(novo_cliente)

    novo_combustivel = input("Novo combustível: ").lower().strip()
    if novo_combustivel != "":
        if novo_combustivel in TIPOS_COMBUSTIVEL:
            item["combustivel"] = novo_combustivel
        else:
            print("Combustível inválido. Campo não alterado.")

    alterar_valores = input("Alterar litros e valor? [s/n]: ").lower().strip()

    if alterar_valores == "s":
        item["litros"] = ler_float("Nova quantidade de litros: ")
        item["valor_litro"] = ler_float("Novo valor por litro: R$ ")
        item["total"] = calcular_total(item["litros"], item["valor_litro"])

    pago = input("Marcar como pago? [s/n]: ").lower().strip()

    if pago == "s":
        item["pago"] = True
    elif pago == "n":
        item["pago"] = False

    print("Registro atualizado com sucesso!")


def excluir_abastecimento():
    """Remove um abastecimento pelo ID."""
    print("\n--- Excluir abastecimento ---")
    id_busca = input("Digite o ID: ")
    item = buscar_por_id(id_busca)

    if item is None:
        print("Registro não encontrado.")
        return

    confirmar = input("Tem certeza que deseja excluir? [s/n]: ").lower().strip()

    if confirmar == "s":
        abastecimentos.remove(item)
        ids_usados.discard(item["id"])
        print("Registro excluído.")
    else:
        print("Exclusão cancelada.")


def relatorio():
    """Mostra um relatório simples do posto."""
    print("\n--- Relatório do Posto Luizão ---")

    if not abastecimentos:
        print("Não há dados para gerar relatório.")
        return

    total_geral = sum(item["total"] for item in abastecimentos)

    pendentes = [
        item for item in abastecimentos
        if item["pago"] is False
    ]

    resumo = {
        tipo: sum(
            item["litros"] for item in abastecimentos
            if item["combustivel"] == tipo
        )
        for tipo in TIPOS_COMBUSTIVEL
    }

    print("Total vendido: R$", f"{total_geral:.2f}")
    print("Abastecimentos pendentes:", len(pendentes))

    print("\nLitros vendidos por combustível:")
    for tipo, litros in resumo.items():
        print(f"{tipo.capitalize()}: {litros:.2f} litros")
