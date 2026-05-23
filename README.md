# 🤖 Agent Task Manager com Trello + Google ADK

Agente inteligente de gerenciamento de tarefas integrado ao Trello, desenvolvido com **Python**, **Google Agent Development Kit (ADK)** e **Gemini API**.

O projeto permite criar, listar, atualizar, priorizar e remover tarefas utilizando linguagem natural, automatizando a organização do dia a dia diretamente em um board do Trello.

---

## 📌 Sobre o Projeto

Este projeto foi desenvolvido como parte do desafio da **DIO (Digital Innovation One)**, com foco na integração entre **Python** e a **API do Trello**, aplicando conceitos de agentes inteligentes utilizando o **Google ADK**.

O agente atua como um assistente organizador de tarefas, interpretando solicitações do usuário e executando ações automaticamente no Trello.

---

## 🚀 Funcionalidades

✅ Criar tarefas automaticamente no Trello  
✅ Criar múltiplas tarefas de uma vez  
✅ Listar tarefas por status  
✅ Alterar status de tarefas  
✅ Definir prioridade usando labels  
✅ Remover tarefas do board  
✅ Contexto temporal (data e hora atual)  
✅ Interação em linguagem natural com agente IA

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Google ADK (Agent Development Kit)**
- **Gemini API**
- **Trello API**
- **python-dotenv**
- **py-trello**

---

## 📂 Estrutura do Projeto

```txt
agent04/
│── agenttaskmanager/
│   ├── __init__.py
│   ├── agent.py
│   ├── .env
│   └── .adk/
│
│── requirements.txt
│── .gitignore
│── README.md
```

---

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/danieli-dutra/dio-agent-task-manager.git
```

Entre na pasta do projeto:

```bash
cd dio-agent-task-manager
```

---

### 2. Crie e ative o ambiente virtual

#### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

#### Git Bash

```bash
source venv/Scripts/activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` dentro da pasta `agenttaskmanager/`:

```env
TRELLO_API_KEY=sua_api_key
TRELLO_API_SECRET=seu_api_secret
TRELLO_TOKEN=seu_token
GOOGLE_API_KEY=sua_google_api_key
```

---

## 🔑 Configuração do Trello

1. Criar conta no Trello  
2. Gerar **API Key** e **Token**  
3. Criar um board chamado:

```txt
DIO
```

Criar as listas:

```txt
A Fazer
Em Andamento
Concluído
```

---

## ▶️ Executando o Projeto

Com o ambiente virtual ativado, execute:

```bash
adk web
```

O servidor será iniciado localmente:

```txt
http://127.0.0.1:8000
```

---

## 💬 Exemplos de Interação

### Criar tarefas

```txt
Quero incluir 3 tarefas:
comprar comida para as dogs,
enviar AVA 2
e marcar provas
```

### Listar tarefas

```txt
quero listar tarefas pendentes
```

### Alterar status

```txt
marcar "enviar AVA 2" como concluída
```

### Definir prioridade

```txt
"marcar provas" é urgente
```

### Remover tarefa

```txt
remover tarefa comprar comida para as dogs
```

---

## 🧠 Como o Agente Funciona

O agente utiliza o **Google ADK** com o modelo **Gemini**, interpretando comandos em linguagem natural e executando ações via integração com a **API do Trello**.

Entre as ferramentas implementadas estão:

- `adicionar_tarefa()`
- `listar_tarefas()`
- `mudar_status_tarefa()`
- `remover_tarefa()`
- `definir_prioridade()`
- `get_temporal_context()`

---

## 📷 Demonstração

Você pode adicionar screenshots do funcionamento do agente aqui futuramente.

Exemplo:

- Criação de tarefas
- Mudança de status
- Integração com Trello
- Interface do ADK funcionando

---

## 📚 Aprendizados

Durante o desenvolvimento deste projeto, foi possível praticar:

- Integração com APIs
- Manipulação do Trello via Python
- Criação de agentes inteligentes
- Engenharia de prompt
- Organização de projetos Python
- Controle de dependências
- Versionamento com Git e GitHub

---

## 👩‍💻 Desenvolvido por

**Danieli Dutra**

Estudante de **Análise e Desenvolvimento de Sistemas**, com foco em **Desenvolvimento Full Stack**, **UX/UI** e **Inteligência Artificial aplicada a produtos digitais**.

GitHub:

```txt
https://github.com/danieli-dutra
```

---

## 📄 Licença

Projeto desenvolvido para fins educacionais como parte do desafio da **DIO**.
