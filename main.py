# main.py
import sys
from datetime import datetime, timedelta

from database.connection import ConnectionManager
from dao.factory import DAOFactory
from business.usuario_service import UsuarioService
from business.laboratorio_service import LaboratorioService
from business.equipamento_service import EquipamentoService
from business.reserva_service import ReservaService

from controllers.usuario_controller import UsuarioController
from controllers.laboratorio_controller import LaboratorioController
from controllers.equipamento_controller import EquipamentoController
from controllers.reserva_controller import ReservaController


def run_demonstration():
    print("=========================================================")
    print(" SISTEMA DE GESTÃO DE LABORATÓRIOS - DEMONSTRAÇÃO BACKEND")
    print("=========================================================\n")

    # 1. Inicialização das Instâncias das Camadas (Sem Métodos Estáticos!)
    connection_manager = ConnectionManager(
        host="127.0.0.1",
        port=5432,
        database="gestao_laboratorio",
        user="lab_user",
        password="lab_password"
    )
    dao_factory = DAOFactory()

    # Serviços (Camada de Negócio)
    usuario_service = UsuarioService(connection_manager, dao_factory)
    laboratorio_service = LaboratorioService(connection_manager, dao_factory)
    equipamento_service = EquipamentoService(connection_manager, dao_factory)
    reserva_service = ReservaService(connection_manager, dao_factory)

    # Controladores (Camada de Tratamento de Eventos/Interface)
    usuario_controller = UsuarioController(usuario_service)
    laboratorio_controller = LaboratorioController(laboratorio_service)
    equipamento_controller = EquipamentoController(equipamento_service)
    reserva_controller = ReservaController(reserva_service)

    # =========================================================
    # PASSO 1: Exibição dos Dados Semeados (Requisito: Mínimo 3 por tabela)
    # =========================================================
    print("--- 1. VERIFICANDO DADOS BÁSICOS PRE-CADASTRADOS (SEED) ---")
    
    print("\n[USUÁRIOS CADASTRADOS]:")
    res_users = usuario_controller.listar()
    if res_users["success"]:
        for u in res_users["data"]:
            print(f"  - ID: {u['id']} | Nome: {u['nome']} | E-mail: {u['email']} | Tipo: {u['tipo']}")
    else:
        print(f"  Erro: {res_users['message']}")

    print("\n[LABORATÓRIOS CADASTRADOS]:")
    res_labs = laboratorio_controller.listar()
    if res_labs["success"]:
        for l in res_labs["data"]:
            print(f"  - ID: {l['id']} | Nome: {l['nome']} | Sala: {l['sala']} | Cap: {l['capacidade']}")
    else:
        print(f"  Erro: {res_labs['message']}")

    print("\n[EQUIPAMENTOS CADASTRADOS]:")
    res_equip = equipamento_controller.listar()
    if res_equip["success"]:
        for eq in res_equip["data"]:
            print(f"  - ID: {eq['id']} | Nome: {eq['nome']} | Marca: {eq['marca']} | Lab ID: {eq['laboratorio_id']} | Status: {eq['status']}")
    else:
        print(f"  Erro: {res_equip['message']}")

    print("\n[RESERVAS CADASTRADAS]:")
    res_reservas = reserva_controller.listar()
    if res_reservas["success"]:
        for r in res_reservas["data"]:
            print(f"  - ID: {r['id']} | Lab ID: {r['laboratorio_id']} | User ID: {r['usuario_id']} | Início: {r['data_inicio']} | Fim: {r['data_fim']} | Status: {r['status']}")
    else:
        print(f"  Erro: {res_reservas['message']}")
        
    print("\n---------------------------------------------------------\n")

    # =========================================================
    # PASSO 2: Cadastro de Novos Dados Básicos
    # =========================================================
    print("--- 2. REALIZANDO NOVOS CADASTROS BÁSICOS ---")
    
    print("\n[Cadastrando Novo Usuário]...")
    res_new_user = usuario_controller.cadastrar(
        nome="Lucas Oliveira",
        email="lucas.oliveira@universidade.edu",
        senha="minhasenhaforte",
        tipo="ALUNO"
    )
    print(f"  Resultado: {res_new_user['message']}")
    lucas_id = res_new_user["data"]["id"] if res_new_user["success"] else None

    print("\n[Cadastrando Novo Laboratório]...")
    res_new_lab = laboratorio_controller.cadastrar(
        nome="Laboratório de Redes de Computadores",
        sala="Sala 108-B",
        capacidade=15,
        descricao="Destinado a práticas de infraestrutura de redes e roteamento."
    )
    print(f"  Resultado: {res_new_lab['message']}")
    redes_lab_id = res_new_lab["data"]["id"] if res_new_lab["success"] else None

    print("\n[Cadastrando Novo Equipamento no Laboratório de Redes]...")
    res_new_eq = equipamento_controller.cadastrar(
        nome="Switch Gerenciável 24 Portas L3",
        marca="Cisco",
        num_serie="SW-999888777",
        laboratorio_id=redes_lab_id,
        status="ATIVO"
    )
    print(f"  Resultado: {res_new_eq['message']}")
    
    print("\n---------------------------------------------------------\n")

    # =========================================================
    # PASSO 3: Consulta por Dados Relacionados (Requisito Crítico!)
    # =========================================================
    print("--- 3. CONSULTANDO DADOS RELACIONADOS ---")
    
    # 3.1 Consultar equipamentos de um laboratório específico (Laboratório de Química ID = 1)
    lab_id_busca = 1
    print(f"\n[Consulta 1] - Equipamentos localizados no Laboratório ID {lab_id_busca}:")
    res_related_eq = laboratorio_controller.listar_equipamentos(lab_id_busca)
    if res_related_eq["success"]:
        for eq in res_related_eq["data"]:
            print(f"  - Equipamento: {eq['nome']} (Marca: {eq['marca']}) | Número de Série: {eq['num_serie']} | Status: {eq['status']}")
    else:
        print(f"  Erro: {res_related_eq['message']}")

    # 3.2 Consultar reservas de um laboratório específico (Laboratório de Química ID = 1)
    print(f"\n[Consulta 2] - Reservas realizadas para o Laboratório ID {lab_id_busca}:")
    res_related_res = laboratorio_controller.listar_reservas(lab_id_busca)
    if res_related_res["success"]:
        for r in res_related_res["data"]:
            print(f"  - Reserva ID: {r['id']} | Período: {r['data_inicio']} até {r['data_fim']} | Finalidade: {r['finalidade']} | Status: {r['status']}")
    else:
        print(f"  Erro: {res_related_res['message']}")

    # 3.3 Consultar dados relacionados de uma Reserva específica (Reserva ID = 1)
    reserva_id_busca = 1
    print(f"\n[Consulta 3] - Dados relacionados da Reserva ID {reserva_id_busca}:")
    
    res_rel_user = reserva_controller.obter_usuario_relacionado(reserva_id_busca)
    if res_rel_user["success"]:
        u = res_rel_user["data"]
        print(f"  - Usuário que reservou: {u['nome']} ({u['email']}) - Perfil: {u['tipo']}")
    else:
        print(f"  Erro ao buscar usuário: {res_rel_user['message']}")

    res_rel_lab = reserva_controller.obter_laboratorio_relacionado(reserva_id_busca)
    if res_rel_lab["success"]:
        l = res_rel_lab["data"]
        print(f"  - Laboratório reservado: {l['nome']} localizado na {l['sala']} (Capacidade: {l['capacidade']})")
    else:
        print(f"  Erro ao buscar laboratório: {res_rel_lab['message']}")

    print("\n---------------------------------------------------------\n")

    # =========================================================
    # PASSO 4: Demonstração das Regras de Negócio e Validações (GoF Strategy)
    # =========================================================
    print("--- 4. DEMONSTRANDO AS REGRAS DE NEGÓCIO E VALIDAÇÕES (GOF STRATEGY) ---")
    
    # 4.1 Teste de Limitação de Tempo de Aluno (Estratégia: UserPermissionStrategy)
    # Aluno tenta reservar por 5 horas (máximo permitido é 4)
    print("\n[Cenário 1] Aluno tenta reservar laboratório por 5 horas:")
    data_inicio_teste = datetime.now() + timedelta(days=5)
    data_fim_teste = data_inicio_teste + timedelta(hours=5) # 5 horas
    
    res_val_aluno = reserva_controller.solicitar(
        laboratorio_id=1,
        usuario_id=lucas_id,  # Usuário Lucas (ALUNO)
        data_inicio=data_inicio_teste.strftime("%Y-%m-%d %H:%M:%S"),
        data_fim=data_fim_teste.strftime("%Y-%m-%d %H:%M:%S"),
        finalidade="Estudo para prova de cálculo"
    )
    print(f"  Resultado esperado (Erro): success={res_val_aluno['success']}")
    print(f"  Mensagem de Validação: {res_val_aluno['message']}")

    # 4.2 Teste de Conflito de Horário (Estratégia: TimeConflictStrategy)
    # Professor Carlos tem reserva aprovada dia 2026-06-20 das 08:00 às 12:00 (Reserva 1)
    # Outro usuário tenta reservar o mesmo laboratório das 10:00 às 11:30 (sobreposição)
    print("\n[Cenário 2] Tentativa de reserva sobreposta no mesmo laboratório e horário:")
    res_val_conflito = reserva_controller.solicitar(
        laboratorio_id=1,
        usuario_id=3, # Mariana Costa (ADMINISTRADOR)
        data_inicio="2026-06-20 10:00:00",
        data_fim="2026-06-20 11:30:00",
        finalidade="Reunião de pesquisa de emergência"
    )
    print(f"  Resultado esperado (Erro): success={res_val_conflito['success']}")
    print(f"  Mensagem de Validação: {res_val_conflito['message']}")

    # 4.3 Solicitação Válida por Professor
    print("\n[Cenário 3] Reserva válida solicitada por Professor (Dr. Carlos):")
    res_val_sucesso = reserva_controller.solicitar(
        laboratorio_id=1,
        usuario_id=2, # Dr. Carlos (PROFESSOR)
        data_inicio="2026-06-20 14:00:00",
        data_fim="2026-06-20 17:00:00",
        finalidade="Pesquisa Avançada de Polímeros"
    )
    print(f"  Resultado esperado (Sucesso): success={res_val_sucesso['success']}")
    print(f"  Mensagem: {res_val_sucesso['message']}")
    if res_val_sucesso["success"]:
        print(f"  Dados da Reserva: {res_val_sucesso['data']}")
        
    print("\n---------------------------------------------------------\n")

    # =========================================================
    # PASSO 5: Demonstração de Atualização e Exclusão
    # =========================================================
    print("--- 5. TESTANDO ATUALIZAÇÃO E EXCLUSÃO ---")
    
    # 5.1 Atualizar status de um equipamento
    print("\n[Atualizando Status de Equipamento]...")
    print("  Buscando equipamento ID 3...")
    res_eq_antigo = equipamento_controller.buscar_por_id(3)
    if res_eq_antigo["success"]:
        eq_data = res_eq_antigo["data"]
        print(f"  Status antigo do equipamento ID 3: {eq_data['status']}")
        
        # Mudar status de MANUTENCAO para ATIVO
        res_update_eq = equipamento_controller.atualizar(
            id_equipamento=3,
            nome=eq_data["nome"],
            marca=eq_data["marca"],
            num_serie=eq_data["num_serie"],
            laboratorio_id=eq_data["laboratorio_id"],
            status="ATIVO"
        )
        print(f"  Resultado da atualização: {res_update_eq['message']}")
        
        res_eq_novo = equipamento_controller.buscar_por_id(3)
        print(f"  Novo status do equipamento ID 3: {res_eq_novo['data']['status']}")
    else:
        print(f"  Erro ao buscar equipamento: {res_eq_antigo['message']}")

    # 5.2 Exclusão de Reserva
    print("\n[Excluindo uma Reserva]...")
    reserva_id_del = 2
    print(f"  Excluindo Reserva ID {reserva_id_del}...")
    res_del = reserva_controller.remover(reserva_id_del)
    print(f"  Resultado da exclusão: {res_del['message']}")
    
    # Verificar que foi deletada
    res_verify_del = reserva_controller.buscar_por_id(reserva_id_del)
    print(f"  Tentativa de busca da Reserva {reserva_id_del} após exclusão: success={res_verify_del['success']} | {res_verify_del['message']}")
    
    print("\n=========================================================")
    print(" DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=========================================================")


if __name__ == "__main__":
    run_demonstration()
