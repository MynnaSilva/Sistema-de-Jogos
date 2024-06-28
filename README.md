<h1 align="center"> SISTEMA DE JOGOS </h1>

UNIVERSIDADE FEDERAL DO MARANHÃO – UFMA

CENTRO DE CIÊNCIAS EXATAS E TECNOLOGIA – CCET

CURSO DE CIÊNCIA E TECNOLOGIA

EECP0005 - PARADIGMAS DE PROGRAMAÇÃO (2024 .1 - T02)

PEDRO  ARTHUR 
2021.....

AMÁBELIE MYNNA PEREIRA SILVA
2021061852</p>



## Descrição do Projeto
Este projeto em Python utilizando Tkinter foi desenvolvido para criar um sistema simples de jogos. O sistema permite interação tanto como administrador quanto como jogador. Utilizando Tkinter, uma biblioteca conhecida pela sua facilidade de uso para criar interfaces gráficas em Python, o sistema oferece uma experiência interativa onde administradores podem gerenciar jogos, configurar regras básicas e monitorar o sistema. Por outro lado, os jogadores podem explorar diferentes jogos disponíveis, compra-los e até mesmo formar equipes, tudo de forma intuitiva.

## Objetivos
O objetivo central deste projeto é demonstrar como os princípios da Programação Orientada a Objetos (OOP) foram empregados na implementação das funcionalidades essenciais do sistema de jogos. Através da OOP, o sistema será estruturado em classes que representam entidades como jogos, jogadores, administradores e funcionalidades específicas de cada jogo.

O objetivo secundário deste cenário é desenvolver um sistema de jogos funcional em Python, com as seguintes metas específicas:

- Criar classes que representem diferentes tipos de jogos, cada uma com métodos para iniciar, pausar e encerrar o jogo.
- Implementar uma hierarquia de classes que permita a extensão fácil de novos tipos de jogos.
- Utilizar herança para compartilhar comportamentos comuns entre os diferentes tipos de jogos, como a lógica de pontuação ou regras básicas.
- Criar classes para administradores e jogadores, com métodos que permitam a gestão de usuários, adição e remoção de jogos, e gerenciamento de partidas em andamento.

## Descrição de entidades
`Jogo (Jogo):` Representa um jogo no sistema. Possui atributos como código, nome, gênero, avaliação, valor e requisitos.

`Jogador (Jogador):` Representa um jogador no sistema. Possui atributos como código, nome, idade, saldo, senha, lista de amigos, lista de jogos que possui e equipe à qual pertence.

`Equipe (Equipe):` Representa uma equipe no sistema. Possui atributos como código, nome, jogo associado e lista de integrantes.

## Funcinalidades
`Cadastro de Jogos e Jogadores`
- Permite registrar novos jogos na plataforma, com informações como título, gênero, valor, requisitos,  etc.
- Facilita a inclusão de novos jogadores com dados como nome de usuário e código.
  
`Alteração de Jogos e Saldo de Jogadores`
- Possibilita a atualização de informações de jogos existentes, como modificar título, gênero, ou ajustar parâmetros de jogabilidade.
- Permite a modificação do saldo dos jogadores, adicionando ou subtraindo conforme ações realizadas na compra de jogos.

`Localização de Jogos e Amigos por Código`
- Permite encontrar um jogo específico na plataforma utilizando seu código único.
- Facilita a localização de amigos dentro do sistema de jogadores, utilizando seus códigos de identificação.

`Listagem Geral de Jogos e Jogadores`
- Apresenta uma visão geral de todos os jogos cadastrados.
- Fornece estatísticas como a média de compras de jogos, jogos compadros e amigos adcionados.

## Instruções para execução:
Para executar o sistema de jogo que você está desenvolvendo em Python usando Tkinter e OOP, siga estes passos básicos:

- Certifique-se de ter Python instalado: Verifique se você tem o Python instalado no seu sistema. Você pode baixá-lo em python.org.

- Instale as dependências necessárias: Se você estiver usando bibliotecas adicionais além das padrões, instale-as utilizando o pip. Por exemplo, se estiver usando o Tkinter:
`pip install tk`

- Baixando ou Clonando o Repositório do Github:
O projeto está hospedado em um repositório no github;
Para baixar ou clonar o rece´tório, siga estas etapas:

``1`` Abra o navegador da web e acesse o repositório do projeto no GitHub.
``2``Clique no botão "Code" (ou "Código") e selecione a opção de download ZIP para baixar o projeto como um arquivo ZIP.
Ou, se preferir, copie o URL do repositório e use um cliente Git para clonar o repositório em sua máquina local:


- Execute o arquivo principal:
  `main.py`
- Interaja com o sistema: Após iniciar o sistema, interaja com ele conforme o fluxo implementado. Envolvendo cadastro de jogadores, criação de equipes, compra de jogos, entre outras funcionalidades desenvolvidas.
 ![image](https://github.com/MynnaSilva/Sistema-de-Jogos/assets/151090210/c69a5000-a8d1-489d-80d0-47409d66f4e3)
