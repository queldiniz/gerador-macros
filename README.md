# ⚙️ NutriAPI: Gestão Nutricional de Pacientes (Back-End)

![Status: Concluído](https://img.shields.io/badge/status-Concluído-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-RESTX-black)

Este projeto consiste em uma API RESTful desenvolvida para ser o "cérebro" do ecossistema **Nutra-se e Evolua**. A aplicação back-end foi construída em **Python** utilizando o framework **Flask** e a extensão **Flask-RestX** para oferecer uma interface robusta, documentada e pronta para produção.

O objetivo principal é fornecer endpoints para realizar as operações de um sistema de cadastro (CRUD), além de atuar como um proxy seguro para integração com bancos de dados externos e gerenciar o compartilhamento público de prontuários médicos.

## 📋 Índice

- [Funcionalidades Principais](#-funcionalidades-principais)
- [Tecnologias e Arquitetura](#-tecnologias-e-arquitetura)
- [Segurança e Compartilhamento (Tokens UUID)](#-segurança-e-compartilhamento-tokens-uuid)
- [Documentação Interativa (Swagger)](#-documentação-interativa-swagger)
- [API FatSecret e Configuração de IP](#-api-fatsecret-e-configuração-de-ip)
- [Instalação e Execução (Passo a Passo)](#-instalação-e-execução-passo-a-passo)

## ✨ Funcionalidades Principais

- **Gestão de Prontuários (CRUD em Cascata):** Armazena dados complexos dos pacientes no banco de dados. Exclusões removem automaticamente todo o histórico e dieta vinculados ao paciente.
- **Histórico e Evolução:** Endpoints dedicados para salvar o histórico mensal de peso e percentual de gordura.
- **Proxy FatSecret:** O servidor realiza a troca de chaves OAuth 2.0 com a base global de alimentos do FatSecret, buscando e higienizando os dados (calorias e macronutrientes) antes de enviá-los ao Front-End.
- **Compartilhamento Público:** Geração de rotas públicas de "somente-leitura" baseadas em Tokens UUID criptografados.

## 🚀 Tecnologias e Arquitetura

- **Linguagem:** Python 3.12
- **Framework Web:** Flask + Flask-RestX (Arquitetura baseada em Namespaces)
- **ORM & Banco de Dados:** SQLAlchemy com persistência em SQLite.
- **Servidor de Produção:** **Gunicorn** (Servidor WSGI). Utilizado para gerenciar múltiplos "workers" (processos paralelos), permitindo que a API lide com dezenas de requisições simultâneas sem perdas de performance.
- **Infraestrutura:** **Docker**. O projeto utiliza uma imagem `python:3.12-slim` para otimizar o tamanho final do contêiner e garantir o funcionamento idêntico em qualquer ambiente. O Compose também realiza healthchecks periódicos na API.

## 🔒 Segurança e Compartilhamento (Tokens UUID)

A funcionalidade de acesso dos pacientes aos seus próprios dados utiliza uma arquitetura de segurança rigorosa:
- **Tokens UUID v4:** São gerados identificadores de 128 bits aleatórios, tornando impossível adivinhar a URL de outro paciente. O ID real do banco de dados nunca é exposto.
- **Validação:** A API verifica a validade do token (`is_active` e datas de expiração) antes de permitir a visualização.
- **Isolamento Read-Only:** As rotas públicas (`/api/public/`) aceitam apenas requisições `GET`, garantindo que ninguém altere os dados externamente.

## 📚 Documentação Interativa (Swagger)

A API gera automaticamente sua própria documentação testável com **Swagger UI** (o Docker Compose é programado para monitorar a saúde desta rota). Com a aplicação rodando, basta acessar pelo navegador:

👉 `http://localhost:5000/api/doc`

Lá você encontrará todos os modelos de dados esperados (Schemas) e poderá testar as rotas diretamente.

## 🌐 API FatSecret e Configuração de IP

Para que o módulo de prescrição de dietas consiga buscar os alimentos, é obrigatório realizar as seguintes configurações na API:

1. **Cadastro de Desenvolvedor:** Crie uma conta gratuita no portal [FatSecret Developer](https://platform.fatsecret.com/) para obter as chaves de acesso (`Client ID` e `Client Secret`).
2. **Liberação de IP (OBRIGATÓRIO):** A API do FatSecret possui um bloqueio de segurança rigoroso por IP. Você **deve** cadastrar o endereço IP público da máquina que está executando este servidor lá no painel do FatSecret.

> ⚠️ **Atenção:** Caso o seu IP mude (comum ao reiniciar o roteador ou acessar de outra rede), as requisições de busca falharão. Lembre-se de atualizar o IP no painel do FatSecret caso isso ocorra.

## 🐳 Instalação e Execução (Passo a Passo)

O projeto foi construído para ser executado integralmente via Docker. Isso significa que você não precisa instalar o Python ou configurar bancos de dados na sua máquina, o Docker fará tudo isso por você de forma isolada!

Siga os passos abaixo para rodar o projeto do zero:


1. **Clone o repositório:**
   ```bash
    > git clone [https://github.com/seu-usuario/gerador-macros.git](https://github.com/seu-usuario/gerador-macros.git)
    > cd gerador-macros/back_end
  
   ```
   
2. **Configurar as Variáveis de Ambiente (.env)**
Para que o servidor consiga se comunicar com a API de alimentos, você precisa configurar suas chaves de acesso seguras.

    1. Na pasta do projeto, localize o arquivo chamado `.env.sample`.
    
    2. Crie uma cópia desse arquivo e renomeie a cópia para `.env` (exatamente assim, com o ponto no início).
    
    3. Abra o arquivo `.env` no seu editor de código.

    4. Cole as chaves que você gerou no site do FatSecret.
  ```bash
      FATSECRET_CLIENT_ID=cole_seu_id_aqui
      FATSECRET_CLIENT_SECRET=cole_seu_secret_aqui
  ```

3. **Rodar o Projeto com Docker**
```bash
  docker compose up --build -d
   ```


4. **Acessar a Aplicação**
```bash    
   O Docker vai baixar as dependências e subir o servidor na porta 5000. O banco de dados (data.sqlite3) será criado e salvo
   ```


   
