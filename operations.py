import TADs


def is_empty(queue):
    return queue['size'] == 0


def push(queue, value):
    """Enfileira um novo chamado no final da fila (Enqueue)"""
    new_node = TADs.initialize_node(value)
    if is_empty(queue):
        queue['head'] = new_node
        queue['tail'] = new_node
    else:
        new_node['previous'] = queue['tail']
        queue['tail']['next'] = new_node
        queue['tail'] = new_node
    queue['size'] += 1
    return True


def pop(queue):
    """Desenfileira e retorna o valor do primeiro chamado (Dequeue)"""
    if is_empty(queue):
        return None

    removed_node = queue['head']
    queue['head'] = queue['head']['next']

    if queue['head'] is not None:
        queue['head']['previous'] = None
    else:
        queue['tail'] = None

    queue['size'] -= 1
    return removed_node['value']


def peek(queue):
    """Retorna o primeiro valor sem remover"""
    if is_empty(queue):
        return None
    return queue['head']['value']


def get_all(queue):
    """Retorna uma lista com todos os elementos para exibição"""
    elementos = []
    atual = queue['head']
    while atual is not None:
        elementos.append(atual['value'])
        atual = atual['next']
    return elementos
