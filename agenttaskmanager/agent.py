from google.adk import Agent
from trello import TrelloClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os


# ==================================
# LOAD ENV
# ==================================

load_dotenv()


# ==================================
# TRELLO CLIENT
# ==================================

def get_trello_client():
    return TrelloClient(
        api_key=os.getenv("TRELLO_API_KEY"),
        api_secret=os.getenv("TRELLO_API_SECRET"),
        token=os.getenv("TRELLO_TOKEN")
    )


def get_board():
    """
    Busca o board DIO.
    """

    client = get_trello_client()

    boards = client.list_boards()

    board = next(
        (
            b for b in boards
            if b.name.strip().upper() == "DIO"
        ),
        None
    )

    if not board:
        raise Exception(
            "Board 'DIO' não encontrado."
        )

    return board


def get_lista_por_nome(nome_lista: str):
    """
    Busca lista pelo nome.
    """

    board = get_board()

    listas = board.list_lists()

    lista = next(
        (
            l for l in listas
            if l.name.strip().lower()
            == nome_lista.strip().lower()
        ),
        None
    )

    if not lista:
        nomes = [
            l.name
            for l in listas
        ]

        raise Exception(
            f"Lista '{nome_lista}' "
            f"não encontrada.\n"
            f"Disponíveis: {nomes}"
        )

    return lista


# ==================================
# TEMPORAL TOOL
# ==================================

def get_temporal_context():
    """
    Retorna data e hora atual.
    """

    now = datetime.now()

    return now.strftime(
        "%d/%m/%Y %H:%M"
    )


# ==================================
# DATE PARSER
# ==================================

def interpretar_data(
    texto_data: str
):
    """
    Interpreta datas naturais.
    """

    if not texto_data:
        return None

    hoje = datetime.now()

    texto = texto_data.lower().strip()

    if texto == "hoje":
        return hoje.isoformat()

    elif texto == "amanhã":
        return (
            hoje +
            timedelta(days=1)
        ).isoformat()

    elif texto == "semana que vem":
        return (
            hoje +
            timedelta(days=7)
        ).isoformat()

    # formato DD/MM/YYYY
    try:
        data = datetime.strptime(
            texto_data,
            "%d/%m/%Y"
        )

        return data.isoformat()

    except Exception:
        return None


# ==================================
# ADD TASK
# ==================================

def adicionar_tarefa(
    nome_da_task: str,
    descricao_da_task: str = "",
    due_date: str = None
):
    """
    Adiciona uma ou múltiplas tarefas.
    """

    try:

        lista = get_lista_por_nome(
            "A Fazer"
        )

        data_vencimento = None

        if due_date:
            data_vencimento = (
                interpretar_data(
                    due_date
                )
            )

        separadores = [
            ",",
            ";",
            " e "
        ]

        tarefas = [nome_da_task]

        for sep in separadores:
            if sep in nome_da_task:

                tarefas = [
                    t.strip()
                    for t in nome_da_task.split(sep)
                    if t.strip()
                ]

                break

        cards_criados = []

        for tarefa in tarefas:

            card = lista.add_card(
                name=tarefa,
                desc=(
                    descricao_da_task
                    if descricao_da_task
                    else f"Tarefa: {tarefa}"
                ),
                due=data_vencimento
            )

            cards_criados.append(
                card.name
            )

        return (
            "Tarefas criadas com sucesso: "
            + ", ".join(cards_criados)
        )

    except Exception as e:

        return (
            "Erro ao criar tarefa: "
            f"{str(e)}"
        )


# ==================================
# LIST TASKS
# ==================================

def listar_tarefas(
    status: str = "pendente"
):
    """
    Lista tarefas por status.
    """

    try:

        status_map = {
            "pendente": "A Fazer",
            "em andamento": "Em Andamento",
            "concluída": "Concluído",
            "concluida": "Concluído"
        }

        nome_lista = status_map.get(
            status.lower()
        )

        if not nome_lista:
            return (
                "Status inválido. "
                "Use: pendente, "
                "em andamento "
                "ou concluída."
            )

        lista = get_lista_por_nome(
            nome_lista
        )

        cards = lista.list_cards()

        if not cards:
            return (
                f"Não há tarefas "
                f"em '{status}'."
            )

        tarefas = []

        for card in cards:
            tarefas.append(
                card.name
            )

        return tarefas

    except Exception as e:

        return (
            "Erro ao listar tarefas: "
            f"{str(e)}"
        )


# ==================================
# PRIORITY
# ==================================

def definir_prioridade(
    nome_da_task: str,
    prioridade: str
):
    """
    Define prioridade via labels.
    """

    try:

        board = get_board()
        listas = board.list_lists()

        cores = {
            "baixa": "green",
            "media": "yellow",
            "média": "yellow",
            "alta": "red",
            "urgente": "purple"
        }

        cor = cores.get(
            prioridade.lower()
        )

        if not cor:
            return (
                "Prioridade inválida. "
                "Use: baixa, média, "
                "alta ou urgente."
            )

        for lista in listas:

            cards = lista.list_cards()

            for card in cards:

                if (
                    card.name.lower()
                    ==
                    nome_da_task.lower()
                ):

                    labels = (
                        board.get_labels()
                    )

                    label_existente = next(
                        (
                            l for l in labels
                            if l.name.lower()
                            ==
                            prioridade.lower()
                        ),
                        None
                    )

                    if not label_existente:

                        label_existente = (
                            board.add_label(
                                prioridade,
                                color=cor
                            )
                        )

                    card.add_label(
                        label_existente
                    )

                    return (
                        f"Prioridade "
                        f"'{prioridade}' "
                        f"adicionada à tarefa "
                        f"'{nome_da_task}'."
                    )

        return (
            f"Tarefa "
            f"'{nome_da_task}' "
            f"não encontrada."
        )

    except Exception as e:

        return f"Erro: {str(e)}"


# ==================================
# CHANGE STATUS
# ==================================

def mudar_status_tarefa(
    nome_da_task: str,
    novo_status: str
):
    """
    Move tarefa entre listas.
    """

    try:

        board = get_board()

        listas = board.list_lists()

        status_map = {
            "pendente": "A Fazer",
            "em andamento": "Em Andamento",
            "concluída": "Concluído",
            "concluida": "Concluído"
        }

        nome_lista_destino = (
            status_map.get(
                novo_status.lower()
            )
        )

        if not nome_lista_destino:
            return (
                "Status inválido."
            )

        lista_destino = (
            get_lista_por_nome(
                nome_lista_destino
            )
        )

        for lista in listas:

            cards = (
                lista.list_cards()
            )

            for card in cards:

                if (
                    card.name.lower()
                    ==
                    nome_da_task.lower()
                ):

                    card.change_list(
                        lista_destino.id
                    )

                    return (
                        f"Tarefa "
                        f"'{nome_da_task}' "
                        f"movida para "
                        f"'{novo_status}'."
                    )

        return (
            f"Tarefa "
            f"'{nome_da_task}' "
            f"não encontrada."
        )

    except Exception as e:

        return (
            "Erro ao mover tarefa: "
            f"{str(e)}"
        )


# ==================================
# REMOVE TASK
# ==================================

def remover_tarefa(
    nome_da_task: str
):
    """
    Remove tarefa.
    """

    try:

        board = get_board()

        listas = board.list_lists()

        for lista in listas:

            cards = lista.list_cards()

            for card in cards:

                if (
                    card.name.lower()
                    ==
                    nome_da_task.lower()
                ):

                    card.delete()

                    return (
                        f"Tarefa "
                        f"'{nome_da_task}' "
                        f"removida com sucesso."
                    )

        return (
            f"Tarefa "
            f"'{nome_da_task}' "
            f"não encontrada."
        )

    except Exception as e:

        return (
            "Erro ao remover tarefa: "
            f"{str(e)}"
        )


# ==================================
# ROOT AGENT
# ==================================

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description=(
        "Agente organizador "
        "de tarefas no Trello"
    ),

    instruction="""
Você é um agente organizador de tarefas integrado ao Trello.

REGRAS:

1. Sempre inicie perguntando as tarefas do dia.

2. Antes disso, obtenha a data atual usando get_temporal_context.

3. Quando o usuário informar tarefas:
- use adicionar_tarefa
- crie uma tarefa para cada item
- adicione descrição automática

4. Quando o usuário pedir:
- listar tarefas
- mostrar tarefas
- ver tarefas

Use listar_tarefas.

5. Quando o usuário pedir remover, apagar ou excluir:
use remover_tarefa.

6. Quando o usuário disser urgente, importante ou prioridade:
use definir_prioridade.

7. Quando o usuário quiser concluir tarefa:
use mudar_status_tarefa.

8. Após adicionar tarefas pergunte:
'Deseja adicionar mais alguma tarefa?'

9. Você possui acesso ao Trello pelas tools.

10. Sempre utilize as ferramentas.
""",

    tools=[
        get_temporal_context,
        adicionar_tarefa,
        listar_tarefas,
        mudar_status_tarefa,
        remover_tarefa,
        definir_prioridade
    ]
)