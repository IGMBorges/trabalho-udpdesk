# Implementação do TAD Node usando dicionário
def initialize_node(value):
    return {
        'value': value,
        'previous': None,  # Conforme o diagrama T.A.D
        'next': None
    }

# Implementação do TAD Queue usando dicionário (com head e tail)


def initialize_queue():
    return {
        'head': None,
        'tail': None,
        'size': 0
    }
