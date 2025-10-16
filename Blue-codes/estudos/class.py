class Clientes:
    def __init__(self, nome, email, telefone):
        self.nome = nome
        self.email = email
        self.telefone = telefone
    pass

class Produtos:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

class Pedidos:
    def __init__(self, cliente, produto, quantidade):
        self.cliente = cliente
        self.produto = produto
        self.quantidade = quantidade
    pass

cliente = Clientes("João", "joao@gmail.com", "1234567890")
print(Clientes.nome)