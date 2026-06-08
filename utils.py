from dados import ids_usados


def ler_float(texto):
    """Lê um número decimal com tratamento de erro."""
    while True:
        try:
            valor = float(input(texto).replace(",", "."))
            if valor <= 0:
                print("Digite um valor maior que zero.")
            else:
                return valor
        except ValueError:
            print("Valor inválido. Digite apenas números.")


def ler_int(texto):
    """Lê um número inteiro com tratamento de erro."""
    while True:
        try:
            return int(input(texto))
        except ValueError:
            print("Digite um número inteiro válido.")


def gerar_id():
    """Gera um ID simples sem repetir."""
    novo_id = len(ids_usados) + 1

    while novo_id in ids_usados:
        novo_id += 1

    ids_usados.add(novo_id)
    return novo_id


def mostrar_iniciais(nome):
    """Retorna as iniciais do nome usando slicing."""
    partes = nome.strip().split()
    iniciais = ""

    for parte in partes:
        iniciais += parte[:1].upper()

    return iniciais


def gerador_registros(lista):
    """Percorre os registros usando yield."""
    for item in lista:
        yield item


def calcular_total(litros, valor_litro):
    """Calcula o valor total do abastecimento."""
    # Bug corrigido:
    # Antes o cálculo poderia dar erro porque input retorna texto.
    # Agora os valores são convertidos para float antes do cálculo.
    return litros * valor_litro
