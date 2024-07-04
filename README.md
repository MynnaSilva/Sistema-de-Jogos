<h1 align="center"> SISTEMA DE JOGOS </h1>

## Descrição do Projeto
Este projeto em Python utilizando Tkinter foi desenvolvido para criar um sistema simples de jogos. O sistema permite interação tanto como administrador quanto como jogador. Utilizando Tkinter, uma biblioteca conhecida pela sua facilidade de uso para criar interfaces gráficas em Python, o sistema oferece uma experiência interativa onde administradores podem gerenciar jogos, configurar regras básicas e monitorar o sistema. Por outro lado, os jogadores podem explorar diferentes jogos disponíveis, compra-los e até mesmo formar equipes, tudo de forma intuitiva.

## Objetivo
O objetivo central deste projeto é demonstrar a aplicação dos princípios da Programação Orientada a Objetos (OOP) na implementação das funcionalidades essenciais de um sistema de jogos. Utilizando OOP, o sistema será estruturado em classes que representam entidades como jogos, jogadores, administradores e funcionalidades típicas de um ambiente de jogos.

## Descrição de entidades
Jogo (Jogo): Representa um jogo no sistema. Possui atributos como código, nome, gênero, avaliação, valor e requisitos.

Jogador (Jogador): Representa um jogador no sistema. Possui atributos como código, nome, idade, saldo, senha, lista de amigos, lista de jogos que possui e equipe à qual pertence.

Equipe (Equipe): Representa uma equipe no sistema. Possui atributos como código, nome, jogo associado e lista de integrantes.

## Funcinalidades
Cadastro de Jogos e Jogadores
- Permite registrar novos jogos na plataforma, com informações como título, gênero, valor, requisitos,  etc.
- Facilita a inclusão de novos jogadores com dados como nome de usuário e código.
  
Alteração de Jogos e Saldo de Jogadores
- Possibilita a atualização de informações de jogos existentes, como modificar título, gênero, ou ajustar parâmetros de jogabilidade.
- Permite a modificação do saldo dos jogadores, adicionando ou subtraindo conforme ações realizadas na compra de jogos.

Localização de Jogos e Amigos por Código
- Permite encontrar um jogo específico na plataforma utilizando seu código único.
- Facilita a localização de amigos dentro do sistema de jogadores, utilizando seus códigos de identificação.

Listagem Geral de Jogos e Jogadores
- Apresenta uma visão geral de todos os jogos cadastrados.
- Fornece estatísticas como a média de compras de jogos, jogos compadros e amigos adcionados.

## Instruções para execução:
Para executar o sistema de jogo que você está desenvolvendo em Python usando Tkinter e OOP, siga estes passos básicos:

- Certifique-se de ter Python instalado: Verifique se você tem o Python instalado no seu sistema. Você pode baixá-lo em python.org.

- Instale as dependências necessárias: Se você estiver usando bibliotecas adicionais além das padrões, instale-as utilizando o pip. Por exemplo, se estiver usando o Tkinter:
pip install tk

- Baixando ou Clonando o Repositório do Github:
O projeto está hospedado em um repositório no github;
Para baixar ou clonar o rece´tório, siga estas etapas:

`1` Abra o navegador da web e acesse o repositório do projeto no GitHub.
`2`Clique no botão "Code" (ou "Código") e selecione a opção de download ZIP para baixar o projeto como um arquivo ZIP.
Ou, se preferir, copie o URL do repositório e use um cliente Git para clonar o repositório em sua máquina local:`https://github.com/MynnaSilva/Sistema-de-Jogos.git`


- Execute o arquivo principal:
  main.py
- Interaja com o sistema: Após iniciar o sistema, interaja com ele conforme o fluxo implementado. Envolvendo cadastro de jogadores, criação de equipes, compra de jogos, entre outras funcionalidades desenvolvidas.
