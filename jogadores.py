class Jogador:
    def __init__(self, codigo, nome, idade=None, saldo=None, senha=None, amigos=None, jogos=None, equipe=None):
        self.codigo = codigo
        self.nome = nome
        self.idade = idade
        self.saldo = saldo
        self.senha = senha
        self.amigos = amigos if amigos is not None else []
        self.jogos = jogos if jogos is not None else []
        self.equipe = equipe

    def adicionar_amigo(self, codigo_amigo):
        if codigo_amigo not in self.amigos:
            self.amigos.append(codigo_amigo)

    def adicionar_jogo(self, codigo_jogo):
        if codigo_jogo not in self.jogos:
            self.jogos.append(codigo_jogo)

    def definir_equipe(self, codigo_equipe):
        self.equipe = codigo_equipe