import pickle # Importa o módulo pickle para serialização
import tkinter as tk # Importa o módulo tkinter para interface gráfica
from tkinter import messagebox, simpledialog  # Importa classes específicas de tkinter para caixas de diálogo
import json # Importa o módulo json para manipulação de dados JSON
import os  # Importa o módulo os para operações de sistema

from jogadores import Jogador  # Importa a classe Jogador do módulo jogadores
from jogos import Jogo  # Importa a classe Jogo do módulo jogos
from equipes import Equipe  # Importa a classe Equipe do módulo equipes

DATA_DIR = "data"  # Define o diretório de dados como "data"
JOGADORES_FILE = os.path.join(DATA_DIR, "jogadores.json")  # Caminho do arquivo JSON dos jogadores
JOGOS_FILE = os.path.join(DATA_DIR, "jogos.json")  # Caminho do arquivo JSON dos jogos
EQUIPES_FILE = os.path.join(DATA_DIR, "equipes.json")  # Caminho do arquivo JSON das equipes

ADMIN_USER = "admin"  # Define o nome de usuário do administrador
ADMIN_PASSWORD = "admin"  # Define a senha do administrador

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Jogos")

        # Carregar dados de arquivos JSON
        self.jogadores = self.carregar_dados(JOGADORES_FILE, Jogador)
        self.equipes = self.carregar_dados(EQUIPES_FILE, Equipe)
        self.jogos = self.carregar_dados(JOGOS_FILE, Jogo, ['requisitos'])  # Ignorar o campo requisitos

        self.label_nome = tk.Label(root, text="Nome de usuário:")
        self.label_nome.pack()
        self.entry_nome = tk.Entry(root)
        self.entry_nome.pack()

        self.label_senha = tk.Label(root, text="Senha:")
        self.label_senha.pack()
        self.entry_senha = tk.Entry(root, show="*")
        self.entry_senha.pack()

        self.btn_login = tk.Button(root, text="Login", command=self.verificar_login)
        self.btn_login.pack()

        self.btn_cadastrar_jogador = tk.Button(root, text="Cadastrar Jogador", command=self.cadastrar_jogador)
        self.btn_cadastrar_jogador.pack()

    def carregar_dados(self, arquivo, classe, campos_ignorar=None):
        if os.path.exists(arquivo):  # Verifica se o arquivo existe
            with open(arquivo, 'r') as f:
                try:
                    dados = json.load(f) # Carrega os dados do arquivo JSON
                    if campos_ignorar:
                        for item in dados:
                            for campo in campos_ignorar:
                                if campo in item:
                                    del item[campo]
                    return [classe(**self.preparar_item(item, classe)) for item in dados]
                except json.JSONDecodeError:
                    return []
        return []

    def preparar_item(self, item, classe):
        parametros = classe.__init__.__code__.co_varnames[1:classe.__init__.__code__.co_argcount]
        for parametro in parametros:
            if parametro not in item:
                item[parametro] = None
        return item

    # Método para salvar dados em arquivos JSON
    def salvar_dados(self, filename, data):
        with open(filename, 'w') as f:
            json.dump([obj.__dict__ for obj in data], f, ensure_ascii=False, indent=4)

    #Verifica o login do usuário com base no nome de usuário e senha fornecidos.
    def verificar_login(self):
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()

        if nome == ADMIN_USER and senha == ADMIN_PASSWORD:
            messagebox.showinfo("Login", "Bem-vindo, administrador!")
            self.abrir_menu_administrador()
            self.root.withdraw()  # Esconde a janela de login após o login
        else:
            jogador = self.buscar_jogador(nome)
            if jogador and jogador.senha == senha:
                messagebox.showinfo("Login", f"Bem-vindo, {jogador.nome}!")
                self.abrir_menu_jogador(jogador)
                self.root.withdraw()  # Esconde a janela de login após o login
            else:
                messagebox.showerror("Erro de Login", "Nome de usuário ou senha incorretos.")

    # Busca um jogador pelo nome de usuário.
    def buscar_jogador(self, nome):
        for jogador in self.jogadores:
            if jogador.nome == nome:
                return jogador
        return None
# Abre uma nova janela para cadastrar um novo jogador.
    def cadastrar_jogador(self):
        novo_codigo = len(self.jogadores) + 1

        cadastrar_window = tk.Toplevel(self.root)
        cadastrar_window.title("Cadastrar Novo Jogador")

        label_nome = tk.Label(cadastrar_window, text="Nome:")
        label_nome.pack()
        entry_nome = tk.Entry(cadastrar_window)
        entry_nome.pack()

        label_senha = tk.Label(cadastrar_window, text="Senha:")
        label_senha.pack()
        entry_senha = tk.Entry(cadastrar_window, show="*")
        entry_senha.pack()

        btn_confirmar = tk.Button(cadastrar_window, text="Confirmar", command=lambda: self.salvar_novo_jogador(
            novo_codigo, entry_nome.get(), entry_senha.get(), cadastrar_window))
        btn_confirmar.pack()

    def salvar_novo_jogador(self, codigo, nome, senha, window):
        # Verificar se já existe um jogador com o mesmo nome de usuário
        if any(jogador.nome == nome for jogador in self.jogadores):
            messagebox.showerror("Erro", "Já existe um jogador com este nome de usuário.")
            return
        
        # Se o nome de usuário for único, prosseguir com o cadastro
        novo_jogador = Jogador(codigo, nome, idade=None, saldo=None, senha=senha)
        self.jogadores.append(novo_jogador)
        self.salvar_dados(JOGADORES_FILE, self.jogadores)
        window.destroy()
        messagebox.showinfo("Cadastro", "Jogador cadastrado com sucesso!")


    # Método para abrir o menu do jogador
    def abrir_menu_jogador(self, jogador):
        menu_jogador_window = tk.Toplevel(self.root)
        menu_jogador_window.title(f"Menu do Jogador - {jogador.nome}")

        label_nome = tk.Label(menu_jogador_window, text=f"Bem-vindo, {jogador.nome}!")
        label_nome.pack()

        # Exibir o código do jogador
        label_codigo = tk.Label(menu_jogador_window, text=f"Seu Código: {jogador.codigo}")
        label_codigo.pack()

        # Exibir o saldo do jogador
        if jogador.saldo is not None:
            label_saldo = tk.Label(menu_jogador_window, text=f"Saldo: R$ {jogador.saldo:.2f}")
        else:
            label_saldo = tk.Label(menu_jogador_window, text="Saldo: Não definido")
        label_saldo.pack()

        btn_colocar_saldo = tk.Button(menu_jogador_window, text="Colocar Saldo", command=lambda: self.colocar_saldo(jogador, menu_jogador_window))
        btn_colocar_saldo.pack()

        btn_comprar_jogo = tk.Button(menu_jogador_window, text="Comprar Jogo", command=lambda: self.comprar_jogo(jogador, menu_jogador_window))
        btn_comprar_jogo.pack()

        btn_listar_jogos = tk.Button(menu_jogador_window, text="Listar Jogos", command=lambda: self.listar_jogos_jogador(jogador, menu_jogador_window))
        btn_listar_jogos.pack()

        # Botão para adicionar amigo
        btn_adicionar_amigo = tk.Button(menu_jogador_window, text="Adicionar Amigo", command=lambda: self.adicionar_amigo(jogador, menu_jogador_window))
        btn_adicionar_amigo.pack()


        btn_listar_amigos = tk.Button(menu_jogador_window, text="Listar Amigos", command=lambda: self.listar_amigos(jogador, menu_jogador_window))
        btn_listar_amigos.pack()

        btn_listar_equipe = tk.Button(menu_jogador_window, text="Menu de equipes", command=lambda: self.menu_equipe(jogador, menu_jogador_window))
        btn_listar_equipe.pack()

        btn_voltar = tk.Button(menu_jogador_window, text="Voltar", command=lambda: self.voltar_tela_login_jogador(menu_jogador_window))
        btn_voltar.pack()

        menu_jogador_window.grab_set()  # Garante que apenas esta janela seja interativa

    # Define uma nova janela Toplevel para gerenciar a equipe do jogador 
    def menu_equipe(self, jogador, menu_jogador_window):
        menu_equipe_window = tk.Toplevel(menu_jogador_window)
        menu_equipe_window.title(f"Gerenciar Equipe - {jogador.nome}")

        btn_formar_equipe = tk.Button(menu_equipe_window, text="Formar Equipe", command=lambda: self.formar_equipe(jogador, menu_equipe_window))
        btn_formar_equipe.pack()

        btn_fiscalizar_equipe = tk.Button(menu_equipe_window, text="Fiscalizar Equipe", command=lambda: self.fiscalizar_equipe(jogador, menu_equipe_window))
        btn_fiscalizar_equipe.pack()

        btn_mostrar_excluir_equipes = tk.Button(menu_equipe_window, text="Mostrar/Excluir Equipes", command=lambda: self.mostrar_excluir_equipes(jogador, menu_equipe_window))
        btn_mostrar_excluir_equipes.pack()

        btn_voltar = tk.Button(menu_equipe_window, text="Voltar", command=menu_equipe_window.destroy)
        btn_voltar.pack()

        menu_equipe_window.grab_set()


    # Fechar a janela do menu do jogador
    def voltar_tela_login_jogador(self, menu_jogador_window):
        menu_jogador_window.destroy()  # Fechar a janela do menu do jogador
        self.root.deiconify()  # Mostrar a janela de login novamente

    # Solicita ao usuário que digite o valor a ser adicionado ao saldo do jogador
    def colocar_saldo(self, jogador, menu_jogador_window):
        valor_saldo = simpledialog.askfloat("Colocar Saldo", f"Digite o valor a ser adicionado ao saldo de {jogador.nome}:")
        if valor_saldo is not None:
            if jogador.saldo is None:
                jogador.saldo = valor_saldo
            else:
             jogador.saldo += valor_saldo
        self.salvar_dados(JOGADORES_FILE, self.jogadores)
        messagebox.showinfo("Saldo Atualizado", f"Saldo de {jogador.nome} atualizado com sucesso!")

        # Atualizar o widget de texto do saldo na mesma janela
        for widget in menu_jogador_window.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text").startswith("Saldo:"):
                widget.config(text=f"Saldo: R$ {jogador.saldo:.2f}")
                break

    # Atualiza o texto do widget de saldo na janela do jogador
    def atualizar_widget_saldo(self, menu_jogador_window, novo_saldo):
        for widget in menu_jogador_window.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text").startswith("Saldo:"):
                widget.config(text=f"Saldo: R$ {novo_saldo:.2f}")
                break
    # Função para permitir que o jogador compre um jogo disponível
    def comprar_jogo(self, jogador, menu_jogador_window):
        if not self.jogos:
            messagebox.showinfo("Jogos", "Não há jogos disponíveis para compra.")
            return

        jogos_disponiveis = "\n".join([f"Código: {jogo.codigo}, Nome: {jogo.nome}, Preço: R$ {jogo.valor:.2f}" for jogo in self.jogos])
        jogo_codigo_str = simpledialog.askstring("Comprar Jogo", f"Jogos disponíveis:\n{jogos_disponiveis}\nDigite o código do jogo que deseja comprar:")

        if jogo_codigo_str:
            try:
                jogo_codigo = int(jogo_codigo_str)
                jogo = self.buscar_jogo_por_codigo(jogo_codigo)
                if not jogo:
                    messagebox.showerror("Erro", "Código do jogo inválido.")
                    return

                saldo_atual = jogador.saldo if jogador.saldo is not None else 0.0
                if saldo_atual < jogo.valor:
                    messagebox.showerror("Erro", "Saldo insuficiente para comprar este jogo.")
                    return

                jogador.saldo = saldo_atual - jogo.valor
                if not jogador.jogos:
                    jogador.jogos = []
                jogador.jogos.append(jogo.codigo)
                self.salvar_dados(JOGADORES_FILE, self.jogadores)
                messagebox.showinfo("Compra", f"Você comprou o jogo '{jogo.nome}' por R$ {jogo.valor:.2f}. Novo saldo: R$ {jogador.saldo:.2f}")

                # Atualizar a exibição do saldo na janela do jogador
                self.atualizar_widget_saldo(menu_jogador_window, jogador.saldo)
            except ValueError:
                messagebox.showerror("Erro", "Código inválido. Por favor, insira um número válido.")
    
    # Permite ao jogador adicionar um amigo à sua lista de amigos
    def adicionar_amigo(self, jogador, menu_jogador_window):
        amigo_nome = simpledialog.askstring("Adicionar Amigo", "Digite o nome do amigo que deseja adicionar:")

        if amigo_nome:
            if amigo_nome == jogador.nome:
                messagebox.showerror("Erro", "Você não pode adicionar a si mesmo como amigo.")
                return

            amigo = self.buscar_jogador_por_nome(amigo_nome)
            if not amigo:
                messagebox.showerror("Erro", "Jogador não encontrado.")
                return

            if amigo_nome in jogador.amigos:
                messagebox.showinfo("Adicionar Amigo", f"{amigo_nome} já é seu amigo.")
            else:
                jogador.amigos.append(amigo_nome)
                self.salvar_dados(JOGADORES_FILE, self.jogadores)
                messagebox.showinfo("Adicionar Amigo", f"{amigo_nome} foi adicionado aos seus amigos.")

                # Atualizar a lista de amigos na interface do jogador
                self.atualizar_lista_amigos(menu_jogador_window, jogador.amigos)
    # Abre a janela para gerenciar as equipes do jogador
    def gerenciar_equipe(self, jogador, menu_jogador_window):
        gerenciar_equipe_window = tk.Toplevel(menu_jogador_window)
        gerenciar_equipe_window.title(f"Gerenciar Equipe - {jogador.nome}")

        btn_formar_equipe = tk.Button(gerenciar_equipe_window, text="Formar Equipe", command=lambda: self.formar_equipe(jogador, gerenciar_equipe_window))
        btn_formar_equipe.pack()

        btn_fiscalizar_equipe = tk.Button(gerenciar_equipe_window, text="Fiscalizar Equipe", command=lambda: self.fiscalizar_equipe(jogador, gerenciar_equipe_window))
        btn_fiscalizar_equipe.pack()

        btn_mostrar_excluir_equipes = tk.Button(gerenciar_equipe_window, text="Mostrar/Excluir Equipes", command=lambda: self.mostrar_excluir_equipes(jogador, gerenciar_equipe_window))
        btn_mostrar_excluir_equipes.pack()

        btn_voltar = tk.Button(gerenciar_equipe_window, text="Voltar", command=gerenciar_equipe_window.destroy)
        btn_voltar.pack()

        gerenciar_equipe_window.grab_set()

    # Permite ao jogador formar uma nova equipe
    def formar_equipe(self, jogador, menu_equipe_window):
        formar_equipe_window = tk.Toplevel(menu_equipe_window)
        formar_equipe_window.title("Formar Nova Equipe")

        label_nome = tk.Label(formar_equipe_window, text="Nome da Equipe:")
        label_nome.pack()
        entry_nome = tk.Entry(formar_equipe_window)
        entry_nome.pack()

        label_jogo = tk.Label(formar_equipe_window, text="Código do Jogo:")
        label_jogo.pack()
        entry_jogo = tk.Entry(formar_equipe_window)
        entry_jogo.pack()

        btn_confirmar = tk.Button(formar_equipe_window, text="Confirmar", command=lambda: self.salvar_nova_equipe(jogador, entry_nome.get(), entry_jogo.get(), formar_equipe_window))
        btn_confirmar.pack()

    # Salva uma nova equipe formada pelo jogador
    def salvar_nova_equipe(self, jogador, nome, codigo_jogo, window):
        nome_jogo = self.obter_nome_jogo_por_codigo(codigo_jogo)

        if not nome_jogo:
            messagebox.showerror("Erro", "Código do jogo inválido.")
            return

        novo_codigo = len(self.equipes) + 1
        nova_equipe = Equipe(novo_codigo, nome, nome_jogo)
        nova_equipe.integrantes.append(jogador.nome)
        self.equipes.append(nova_equipe)
        self.salvar_dados(EQUIPES_FILE, self.equipes)
        jogador.equipe = novo_codigo
        self.salvar_dados(JOGADORES_FILE, self.jogadores)
        window.destroy()
        messagebox.showinfo("Equipe", "Equipe formada com sucesso!")

    # Retorna o nome do jogo dado seu código
    def obter_nome_jogo_por_codigo(self, codigo_jogo):
        jogos = self.carregar_dados('jogos.json', Jogo)
        for jogo in jogos:
            if jogo.codigo == codigo_jogo:
                return jogo.nome
        return None

    # Permite ao jogador fiscalizar a equipe da qual faz parte
    def fiscalizar_equipe(self, jogador, gerenciar_equipe_window):
        if not jogador.equipe:
            messagebox.showerror("Erro", "Você não está em nenhuma equipe.")
            return

        equipe = self.buscar_equipe_por_codigo(jogador.equipe)
        if not equipe:
            messagebox.showerror("Erro", "Equipe não encontrada.")
            return

        fiscalizar_equipe_window = tk.Toplevel(gerenciar_equipe_window)
        fiscalizar_equipe_window.title(f"Fiscalizar Equipe - {equipe.nome}")

        label_lider = tk.Label(fiscalizar_equipe_window, text=f"Líder: {equipe.lider}")
        label_lider.pack()

        label_membros = tk.Label(fiscalizar_equipe_window, text="Membros:")
        label_membros.pack()

        membros_listbox = tk.Listbox(fiscalizar_equipe_window)
        membros_listbox.pack(fill=tk.BOTH, expand=True)
        for membro in equipe.membros:
            membros_listbox.insert(tk.END, membro)

        if jogador.nome == equipe.lider:
            btn_adicionar_membro = tk.Button(fiscalizar_equipe_window, text="Adicionar Membro", command=lambda: self.adicionar_membro(jogador, equipe, membros_listbox))
            btn_adicionar_membro.pack()

        btn_fechar = tk.Button(fiscalizar_equipe_window, text="Fechar", command=fiscalizar_equipe_window.destroy)
        btn_fechar.pack()

        fiscalizar_equipe_window.grab_set()

    # Carrega dados de um arquivo JSON para uma lista de objetos do tipo especificado
    def carregar_dados_json(filename, class_type):
        with open(filename, 'r') as f:
            data = json.load(f)
            return [class_type(**item) for item in data]

    def salvar_dados_json(filename, data):
        with open(filename, 'w') as f:
            json.dump([obj.__dict__ for obj in data], f, indent=4)



    # Salva uma lista de objetos em formato JSON no arquivo especificado
    def listar_amigos(self, jogador, menu_jogador_window):
        listar_amigos_window = tk.Toplevel(menu_jogador_window)
        listar_amigos_window.title(f"Amigos de {jogador.nome}")

        # Adicionando informação sobre a quantidade total de amigos
        total_amigos_label = tk.Label(listar_amigos_window, text=f"Total de amigos: {len(jogador.amigos)}")
        total_amigos_label.pack()

        label_amigos = tk.Label(listar_amigos_window, text="Seus Amigos:")
        label_amigos.pack()

        amigos_listbox = tk.Listbox(listar_amigos_window)
        amigos_listbox.pack(fill=tk.BOTH, expand=True)

        for amigo_nome in jogador.amigos:
            amigos_listbox.insert(tk.END, amigo_nome)

        btn_fechar = tk.Button(listar_amigos_window, text="Fechar", command=listar_amigos_window.destroy)
        btn_fechar.pack()

        listar_amigos_window.grab_set()

    def listar_jogos_jogador(self, jogador):
        if jogador.jogos:
            jogos = ", ".join([str(codigo) for codigo in jogador.jogos])
            messagebox.showinfo("Jogos", f"Jogos de {jogador.nome}: {jogos}")
        else:
            messagebox.showinfo("Jogos", f"{jogador.nome} não possui nenhum jogo ainda.")

    def ver_equipe(self, jogador):
        if jogador.equipe:
            equipe = self.buscar_equipe_por_codigo(jogador.equipe)
            messagebox.showinfo("Equipe", f"{jogador.nome} está na equipe {equipe.nome} do jogo {equipe.jogo}.")
        else:
            messagebox.showinfo("Equipe", f"{jogador.nome} não está em nenhuma equipe.")

    def buscar_jogador_por_codigo(self, codigo):
        for jogador in self.jogadores:
            if jogador.codigo == codigo:
                return jogador
        return None

    def buscar_jogador_por_nome(self, nome):
        for jogador in self.jogadores:
            if jogador.nome == nome:
                return jogador
        return None

    def atualizar_lista_amigos(self, menu_jogador_window, lista_amigos):
        amigos_widget = None
        for widget in menu_jogador_window.winfo_children():
            if isinstance(widget, tk.Listbox) and widget.cget("listvariable") == "amigos":
                amigos_widget = widget
                break

        if amigos_widget:
            amigos_widget.delete(0, tk.END)
            for amigo in lista_amigos:
                amigos_widget.insert(tk.END, amigo)
                
    def buscar_equipe_por_codigo(self, codigo):
        for equipe in self.equipes:
            if equipe.codigo == codigo:
                return equipe
        return None

    #Abre a janela do menu do administrador com opções para gerenciar jogos.
    def abrir_menu_administrador(self):
        menu_admin_window = tk.Toplevel(self.root)
        menu_admin_window.title("Menu do Administrador")

        label_admin = tk.Label(menu_admin_window, text="Bem-vindo, administrador!")
        label_admin.pack()

        btn_cadastrar_jogo = tk.Button(menu_admin_window, text="Cadastrar Jogo", command=self.cadastrar_jogo)
        btn_cadastrar_jogo.pack()

        btn_alterar_jogo = tk.Button(menu_admin_window, text="Alterar Jogo", command=self.alterar_jogo)
        btn_alterar_jogo.pack()

        btn_excluir_jogo = tk.Button(menu_admin_window, text="Excluir Jogo", command=self.excluir_jogo)
        btn_excluir_jogo.pack()

        btn_listar_jogos = tk.Button(menu_admin_window, text="Listar Jogos", command=self.listar_jogos_admin)
        btn_listar_jogos.pack()

        btn_localizar_jogo = tk.Button(menu_admin_window, text="Localizar Jogo", command=self.localizar_jogo)
        btn_localizar_jogo.pack()

        btn_voltar = tk.Button(menu_admin_window, text="Voltar", command=self.voltar_tela_login)
        btn_voltar.pack()

    #Volta para a tela de login, destruindo os widgets da tela atual.
    def voltar_tela_login(self):
        self.root.deiconify()  # Mostrar a janela de login
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

    #Abre a janela para cadastrar um novo jogo e insere os dados do jogo.
    def cadastrar_jogo(self):
        novo_codigo = len(self.jogos) + 1

        cadastrar_jogo_window = tk.Toplevel(self.root)
        cadastrar_jogo_window.title("Cadastrar Novo Jogo")

        label_codigo = tk.Label(cadastrar_jogo_window, text="Código do Jogo:")
        label_codigo.pack()
        entry_codigo = tk.Entry(cadastrar_jogo_window)
        entry_codigo.insert(0, novo_codigo)
        entry_codigo.pack()

        label_nome = tk.Label(cadastrar_jogo_window, text="Nome do Jogo:")
        label_nome.pack()
        entry_nome = tk.Entry(cadastrar_jogo_window)
        entry_nome.pack()

        label_genero = tk.Label(cadastrar_jogo_window, text="Gênero do Jogo:")
        label_genero.pack()
        entry_genero = tk.Entry(cadastrar_jogo_window)
        entry_genero.pack()

        label_avaliacao = tk.Label(cadastrar_jogo_window, text="Avaliação do Jogo:")
        label_avaliacao.pack()
        entry_avaliacao = tk.Entry(cadastrar_jogo_window)
        entry_avaliacao.pack()

        label_valor = tk.Label(cadastrar_jogo_window, text="Valor do Jogo:")
        label_valor.pack()
        entry_valor = tk.Entry(cadastrar_jogo_window)
        entry_valor.pack()

        label_requisitos = tk.Label(cadastrar_jogo_window, text="Requisitos do Jogo:")
        label_requisitos.pack()
        entry_requisitos = tk.Entry(cadastrar_jogo_window)
        entry_requisitos.pack()

        btn_confirmar = tk.Button(cadastrar_jogo_window, text="Confirmar", command=lambda: self.salvar_novo_jogo(
            entry_codigo.get(), entry_nome.get(), entry_genero.get(), float(entry_avaliacao.get()), float(entry_valor.get()), entry_requisitos.get(), cadastrar_jogo_window))
        btn_confirmar.pack()

    #Salva os dados do novo jogo e o adiciona à lista de jogos.
    # Verifica se já existe um jogo com o mesmo código 
    def salvar_novo_jogo(self, codigo, nome, genero, avaliacao, valor, requisitos, window):
        if any(jogo.codigo == codigo for jogo in self.jogos):
         messagebox.showerror("Erro", "Já existe um jogo com este código.")
         return
        novo_jogo = Jogo(codigo, nome, genero, avaliacao, valor, requisitos)
        self.jogos.append(novo_jogo)
        self.salvar_dados(JOGOS_FILE, self.jogos)
        window.destroy()
        messagebox.showinfo("Cadastro", "Jogo cadastrado com sucesso!")


    def alterar_jogo(self):
     codigo = simpledialog.askstring("Alterar Jogo", "Digite o código do jogo a ser alterado:")
     jogo = self.buscar_jogo_por_codigo(codigo)
     if jogo:
        alterar_jogo_window = tk.Toplevel(self.root)
        alterar_jogo_window.title("Alterar Jogo")

        label_nome = tk.Label(alterar_jogo_window, text="Nome do Jogo:")
        label_nome.pack()
        entry_nome = tk.Entry(alterar_jogo_window)
        entry_nome.insert(0, jogo.nome)
        entry_nome.pack()

        label_genero = tk.Label(alterar_jogo_window, text="Gênero do Jogo:")
        label_genero.pack()
        entry_genero = tk.Entry(alterar_jogo_window)
        entry_genero.insert(0, jogo.genero)
        entry_genero.pack()

        label_avaliacao = tk.Label(alterar_jogo_window, text="Avaliação do Jogo:")
        label_avaliacao.pack()
        entry_avaliacao = tk.Entry(alterar_jogo_window)
        entry_avaliacao.insert(0, jogo.avaliacao)
        entry_avaliacao.pack()

        label_valor = tk.Label(alterar_jogo_window, text="Valor do Jogo:")
        label_valor.pack()
        entry_valor = tk.Entry(alterar_jogo_window)
        entry_valor.insert(0, jogo.valor)
        entry_valor.pack()

        label_requisitos = tk.Label(alterar_jogo_window, text="Requisitos do Jogo:")
        label_requisitos.pack()
        entry_requisitos = tk.Entry(alterar_jogo_window)
        entry_requisitos.insert(0, jogo.requisitos if jogo.requisitos else "")
        entry_requisitos.pack()

        btn_confirmar = tk.Button(alterar_jogo_window, text="Confirmar", command=lambda: self.salvar_jogo_alterado(
            jogo, entry_nome.get(), entry_genero.get(), float(entry_avaliacao.get()), float(entry_valor.get()), entry_requisitos.get(), alterar_jogo_window))
        btn_confirmar.pack()
     else:
        messagebox.showerror("Erro", "Jogo não encontrado.")

    def salvar_jogo_alterado(self, jogo, nome, genero, avaliacao, valor, requisitos, window):
        jogo.nome = nome
        jogo.genero = genero
        jogo.avaliacao = avaliacao
        jogo.valor = valor
        jogo.requisitos = requisitos
        self.salvar_dados(JOGOS_FILE, self.jogos)
        window.destroy()
        messagebox.showinfo("Alteração", "Jogo alterado com sucesso!")


    #Solicita o código do jogo a ser excluído e realiza a exclusão se confirmado.
    def excluir_jogo(self):
        codigo = simpledialog.askinteger("Excluir Jogo", "Digite o código do jogo que deseja excluir:")
        if codigo is None:
            return

        jogo = self.buscar_jogo_por_codigo(codigo)

        if jogo:
            confirmacao = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o jogo '{jogo.nome}'?")
            if confirmacao:
                self.jogos = [j for j in self.jogos if str(j.codigo) != str(codigo)]
                self.salvar_dados(JOGOS_FILE, self.jogos)
                messagebox.showinfo("Exclusão", f"Jogo '{jogo.nome}' excluído com sucesso!")
            else:
                messagebox.showinfo("Cancelado", "Exclusão cancelada.")
        else:
            messagebox.showerror("Erro", f"Jogo com código {codigo} não encontrado.")


    #Lista todos os jogos cadastrados e exibe em uma caixa de mensagem.
    def listar_jogos_admin(self):
        if self.jogos:
            lista_jogos = "\n\n".join([
                f"Código: {jogo.codigo}, Nome: {jogo.nome}, Gênero: {jogo.genero}, "
                f"Avaliação: {jogo.avaliacao}, Valor: R$ {jogo.valor:.2f}, Requisitos: {jogo.requisitos}"
                for jogo in self.jogos
            ])
            messagebox.showinfo("Lista de Jogos", lista_jogos)
        else:
            messagebox.showinfo("Lista de Jogos", "Não há jogos cadastrados ainda.")

    # Abre uma janela listando todos os jogos do jogador especificado.
    def listar_jogos_jogador(self, jogador, menu_jogador_window):
        listar_jogos_window = tk.Toplevel(menu_jogador_window)
        listar_jogos_window.title(f"Jogos de {jogador.nome}")

        # Adicionando informação sobre a quantidade total de jogos
        total_jogos_label = tk.Label(listar_jogos_window, text=f"Total de jogos: {len(jogador.jogos)}")
        total_jogos_label.pack()

        label_jogos = tk.Label(listar_jogos_window, text="Seus Jogos:")
        label_jogos.pack()

        jogos_listbox = tk.Listbox(listar_jogos_window)
        jogos_listbox.pack(fill=tk.BOTH, expand=True)

        for jogo_codigo in jogador.jogos:
            jogo = self.buscar_jogo_por_codigo(jogo_codigo)
            if jogo:
                jogos_listbox.insert(tk.END, f"{jogo.nome} (Código: {jogo.codigo})")

        btn_fechar = tk.Button(listar_jogos_window, text="Fechar", command=listar_jogos_window.destroy)
        btn_fechar.pack()

        listar_jogos_window.grab_set()

    #Solicita o código de um jogo e exibe suas informações se encontrado.  
    def localizar_jogo(self):
        codigo = simpledialog.askinteger("Localizar Jogo", "Digite o código do jogo que deseja localizar:")
        jogo = self.buscar_jogo_por_codigo(codigo)

        if jogo:
            messagebox.showinfo("Jogo Encontrado", 
                f"Código: {jogo.codigo}\n"
                f"Nome: {jogo.nome}\n"
                f"Gênero: {jogo.genero}\n"
                f"Avaliação: {jogo.avaliacao}\n"
                f"Valor: R$ {jogo.valor:.2f}\n"
                f"Requisitos: {jogo.requisitos}"
            )
        else:
            messagebox.showerror("Erro", f"Jogo com código {codigo} não encontrado.")

    #Busca um jogo na lista de jogos pelo seu código.
    def buscar_jogo_por_codigo(self, codigo):
        for jogo in self.jogos:
            if str(jogo.codigo) == str(codigo):
                return jogo
        return None

# Cria a aplicação principal e inicia o loop de eventos
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()
