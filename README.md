# Backend Sprint 1: Desenvolvimento Full Stack Básico - Instruções de Uso

Este projeto é um backend para o MVP da primeira sprint de fullstack basico da PUCRJ usando **Flask** em Python.

## 📦 Requisitos

- Python 3.8 ou superior (foi utilizado o 3.10.8 na criação desse projeto)

## ⚙️ Passo a passo para rodar o projeto

### 1. Clone o repositório (caso ainda não tenha feito isso)

```bash
git clone https://github.com/gusta7597/backend-fullstack-mvp.git
cd backend-fullstack-mvp
```
### 2. Caso precise crie um virtual enviroment (É recomendado)

```bash
python -m venv venv
```
### 3. Ative o virtual enviroment (Caso tenha criado)

```bash
.\venv\Scripts\activate
```
### 4. Instale as dependências

```bash
pip install -r requirements.txt
```
### 5. Execute o arquivo app.py

```bash
python app.py
```
### 6. Ative o ambiente flask

```bash
flask run --host 0.0.0.0 --port 5000
```

### Após isso o ambiente estará rodando no link **http://localhost:5000**, caso deseje a documentação do swagger estará no **http://localhost:5000/openapi/swagger#/**
