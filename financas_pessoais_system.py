import requests
import json
from api import conexao_banco_dados, encerramento_conexao

# CORPO DO SCRIPT
response2 = True
while response2 == True:

    print("\n")
    print("|++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|")
    print("|--------------------------|INÍCIO|--------------------------|")
    print("|++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|")
    print("                                                             ")
    print("|------------------------------------------------------------|")
    print("|-----------------FUNCIONALIDADES DISPONÍVEIS----------------|")
    print("|------------------------------------------------------------|")
    print("\n")
    print("1 = Listar contas disponíveis no sistema")
    print("2 = Adicionar conta no sistema")
    print("3 = Remover conta do sistema")
    print("4 = Editar conta")
    print("5 = Saldo total de todas as contas")
    print("6 = Consultar receitas")
    print("7 = Consultar despesas")
    print("8 = Transferir saldo entre contas")
    print("\n")
    resposta1 = str(input("Digite o número correspondente ao seu interesse: "))
    print("\n")

    # Funções

    def continuacao():
        print("\n")
        test1 = True
        while test1 == True:
            response3 = input("Gostaria de fazer algo mais ? (S/N): ").lower()
            if response3 == "s":
                test1 = False
                print("\n")
            elif response3 == "n":
                test1 = False
                global response2
                response2 = False
            else:
                print("Opção inválida!")
        
    def invalido():
        print("\n")
        test1 = True
        while test1 == True:
            response3 = input("Opção inválida! Gostaria de iniciar novamente? (S/N): ").lower()
            if response3 == "s":
                test1 = False
                print("\n")
            elif response3 == "n":
                test1 = False
                global response2
                response2 = False
            else:
                print("Opção inválida!")
            
    # FUNCIONALIDADES DO PROGRAMA

    if resposta1 == "1":
        request = requests.get("http://localhost:5000/conta")
        response = json.loads(request.text)
        if str(response) != "Nao foi possível fazer conexao com o MySQL":
            print("(*) Ordem das listas: ID DA CONTA, TIPO, INSTITUIÇÃO FINANCEIRA E SALDO")
            print("(*) Observação: NULL para valores inexistentes")
            print("=======================================================================")
            for i in response:
                print(f"{i}, {response[i]['tipo']}, {response[i]['instituicao_financeira']}, {response[i]['saldo']}")
            continuacao()
        else:
            print(response)
        
    elif resposta1 == "2":
        con, cursor = conexao_banco_dados()
        try:
            tipo_conta = input("Qual o tipo da conta? CARTEIRA, CONTA CORRENTE OU POUPANÇA? ").lower()
            inst_fin = input("Qual é a Instituição Financeira da conta? ")
            saldo = input("Qual é o saldo da conta? Digite em números: ")
            cursor.execute(f"INSERT INTO CONTA VALUES(NULL, '{tipo_conta}', '{inst_fin}', {saldo});")
            con.commit()
            encerramento_conexao(con, cursor)
        except Exception as e:
            encerramento_conexao(con, cursor)
            print("Ocorreu o seguinte erro: ")
            print(e)
        finally:
            continuacao()

    elif resposta1 == "3":
        con, cursor = conexao_banco_dados()
        try:
            idconta_remover = input("Qual é o ID da conta que deseja remover? ")
            cursor.execute(f"DELETE FROM CONTA WHERE IDCONTA = {idconta_remover};")
            con.commit()
            encerramento_conexao(con, cursor)
        except Exception as e:
            encerramento_conexao(con, cursor)
            print("Ocorreu o seguinte erro: ")
            print(e)
        finally:
            continuacao()

    elif resposta1 == "4":
        con, cursor = conexao_banco_dados()
        try:
            alteracao = input("O que você deseja alterar na conta? O TIPO, INSTITUICAO FINANCEIRA OU SALDO? ").lower()
            if alteracao == "tipo":
                tipo_alteracao = input("Para qual tipo você deseja alterar? CARTEIRA, CONTA CORRENTE OU POUPANÇA? ").lower()
                idconta_alterar = input("Qual é o ID da conta que deseja alterar? ")
                cursor.execute(f"UPDATE CONTA SET TIPO = '{tipo_alteracao}' WHERE IDCONTA = {idconta_alterar};")
                con.commit()
                encerramento_conexao(con, cursor)
            elif alteracao == "instituicao financeira":
                inst_fin_alteracao = input("Para qual Instituição Financeira deseja alterar? ")
                idconta_alterar = input("Qual é o ID da conta que deseja alterar? ")
                cursor.execute(f"UPDATE CONTA SET INSTITUICAO_FINANCEIRA = '{inst_fin_alteracao}' WHERE IDCONTA = {idconta_alterar};")
                con.commit()
                encerramento_conexao(con, cursor)
            elif alteracao == "saldo":
                saldo_alteracao = input("Para qual saldo deseja alterar? ")
                idconta_alterar = input("Qual é o ID da conta que deseja alterar? ")
                cursor.execute(f"UPDATE CONTA SET SALDO = {saldo_alteracao} WHERE IDCONTA = {idconta_alterar};")
                con.commit()
                encerramento_conexao(con, cursor)
            else:
                encerramento_conexao(con, cursor)
                print("Requisição de alteração incorreta! Por favor, tente novamente.")
        except Exception as e:
            encerramento_conexao(con, cursor)
            print("Ocorreu o seguinte erro: ")
            print(e)
        finally:
            continuacao()
            
    elif resposta1 == "5":
        request = requests.get("http://localhost:5000/saldo/soma")
        response = str(request.text)
        if response != "Nao foi possível fazer conexao com o MySQL":
            print(f"O saldo de todas as suas contas é: {response}")
            continuacao()
        else:
            print(response)

    elif resposta1 == "6":
        idconta_receita = input("Você gostaria de acessar a(s) receita(s) de qual conta? Digite seu ID: ")
        print("\n")
        print("-------------------------------------------------------------")
        print("-----------FUNCIONALIDADES DE RECEITAS DISPONÍVEIS-----------")
        print("--------------------------RECEITAS---------------------------")
        print("-------------------------------------------------------------")
        print("\n")
        print("1 = Cadastrar novas receitas")
        print("2 = Remover receitas do sistema")
        print("3 = Alterar receitas no sistema")
        print("4 = Listar receitas cadastradas")
        print("\n")
        resposta2 = str(input("Digite o número correspondente ao seu interesse: "))

        if resposta2 == "1":
            con, cursor = conexao_banco_dados()
            try:
                tipo_receita = input("Qual o tipo de receita? SALÁRIO, PRESENTE, PRÊMIO OU OUTROS? ").lower()
                valor_receita = input("Qual é o valor da receita? Digite em números: ")
                data_recebimento_esperado = input("Qual é a data de recebimento esperado? Escreva no formato '0000-00-00': ")
                data_recebimento = input("Qual foi a data de recebimento? Escreva no formato '0000-00-00': ")
                descricao = input("Escreva uma descrição para a sua receita: ")
                cursor.execute(f"INSERT INTO RECEITA VALUES(NULL, '{tipo_receita}', {valor_receita}, '{data_recebimento_esperado}', '{data_recebimento}', '{descricao}', {idconta_receita});")
                con.commit()
                encerramento_conexao(con, cursor)
            except Exception as e:
                encerramento_conexao(con, cursor)
                print("Ocorreu o seguinte erro: ")
                print(e)
            finally:
                continuacao()
        elif resposta2 == "2":
            con, cursor = conexao_banco_dados()
            try:
                idreceita_remover = input("Digite o ID da receita que deseja remover: ")
                cursor.execute(f"DELETE FROM RECEITA WHERE IDRECEITA = {idreceita_remover};")
                con.commit()
                encerramento_conexao(con, cursor)
            except Exception as e:
                encerramento_conexao(con, cursor)
                print("Ocorreu o seguinte erro: ")
                print(e)
            finally:
                continuacao()
        elif resposta2 == "3":
            con, cursor = conexao_banco_dados()
            try:
                idreceita_alterar = input("Digite o ID da receita que deseja alterar: ")
                alteracao_receita = input("O que você deseja alterar na receita? O TIPO, VALOR_EM_REAIS, DATA_RECEBIMENTO_ESPERADO, DATA_RECEBIMENTO, DESCRICAO OU ID_CONTA? ").lower()
                
                if alteracao_receita == "tipo":
                    receita_tipo_alterar = input("Para qual tipo você deseja alterar? SALÁRIO, PRESENTE, PRÊMIO OU OUTROS? ")
                    cursor.execute(f"UPDATE RECEITA SET TIPO = '{receita_tipo_alterar}' WHERE IDRECEITA = {idreceita_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                elif alteracao_receita == "valor_em_reais":
                    receita_valor_alterar = input("Digite para qual valor deseja alterar: ")
                    cursor.execute(f"UPDATE RECEITA SET VALOR_EM_REAIS = {receita_valor_alterar} WHERE IDRECEITA = {idreceita_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                elif alteracao_receita == "data_recebimento_esperado":
                    receita_data_esperada_alterar = input("Digite para qual data deseja alterar no formato '0000-00-00': ")
                    cursor.execute(f"UPDATE RECEITA SET DATA_RECEBIMENTO_ESPERADO = '{receita_data_esperada_alterar}' WHERE IDRECEITA = {idreceita_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                elif alteracao_receita == "data_recebimento":
                    receita_data_alterar = input("Digite para qual data deseja alterar no formato '0000-00-00': ")
                    cursor.execute(f"UPDATE RECEITA SET DATA_RECEBIMENTO = '{receita_data_alterar}' WHERE IDRECEITA = {idreceita_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                elif alteracao_receita == "descricao":
                    receita_descricao_alterar = input("Digite para qual descrição deseja alterar: ")
                    cursor.execute(f"UPDATE RECEITA SET DESCRICAO = '{receita_descricao_alterar}' WHERE IDRECEITA = {idreceita_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                elif alteracao_receita == "id_conta":
                    receita_id_conta_alterar = input("Digite o ID da conta que gostaria de agregar essa receita: ")
                    cursor.execute(f"UPDATE RECEITA SET ID_CONTA = {receita_id_conta_alterar} WHERE IDRECEITA = {idreceita_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                else:
                    encerramento_conexao(con, cursor)
                    invalido()
            except Exception as e:
                encerramento_conexao(con, cursor)
                print("Ocorreu o seguinte erro: ")
                print(e)
            finally:
                continuacao()
        elif resposta2 == "4":
            receita_tipo_listagem = str(input("Como você gostaria de visualizar suas receitas? Por período(1), tipo(2) ou apenas visualizar tudo(3)? Digite o número de sua preferência: "))
            print("\n")

            if receita_tipo_listagem == "1":
                request = requests.get("http://localhost:5000/receita/periodo")
                response = json.loads(request.text)
                if str(response) != "Nao foi possível fazer conexao com o MySQL":
                    print("(*) Ordem das listas: DATA DE RECEBIMENTO, DATA RECEBIMENTO ESPERADO, TIPO, VALOR EM REAIS, ID RECEITA, ID CONTA E DESCRICAO.")
                    print("========================================================================================================================================================")
                    print("\n")
                    for i in response:
                        print(f"{i}, {response[i]['data_recebimento_esperado']}, {response[i]['tipo']}, {response[i]['valor_em_reais']}, {response[i]['data_recebimento']}, {response[i]['id_conta']}, {response[i]['descricao']}")
                    continuacao()
                else:
                    print(response)
        
            elif receita_tipo_listagem == "2":
                request = requests.get("http://localhost:5000/receita/tipo")
                response = json.loads(request.text)
                if str(response) != "Nao foi possível fazer conexao com o MySQL":
                    print("(*) Ordem das listas: TIPO, ID RECEITA, VALOR EM REAIS, DATA DE RECEBIMENTO ESPERADO, DATA DE RECEBIMENTO, DESCRIÇÃO E O ID DA CONTA A QUE SE REFERE.")
                    print("========================================================================================================================================================")
                    print("\n")
                    for i in response:
                        print(f"{i}, {response[i]['tipo']}, {response[i]['valor_em_reais']}, {response[i]['data_recebimento_esperado']}, {response[i]['data_recebimento']}, {response[i]['descricao']}, {response[i]['id_conta']}")
                    continuacao()
                else:
                    print(response)

            elif receita_tipo_listagem == "3":
                request = requests.get("http://localhost:5000/receita/tudo")
                response = json.loads(request.text)
                if str(response) != "Nao foi possível fazer conexao com o MySQL":
                    print("(*) Ordem das listas: ID DA RECEITA, TIPO, VALOR EM REAIS, DATA DE RECEBIMENTO ESPERADO, DATA DE RECEBIMENTO, DESCRIÇÃO E O ID DA CONTA A QUE SE REFERE.")
                    print("========================================================================================================================================================")
                    print("\n")
                    for i in response:
                        print(f"{i}, {response[i]['tipo']}, {response[i]['valor_em_reais']}, {response[i]['data_recebimento_esperado']}, {response[i]['data_recebimento']}, {response[i]['descricao']}, {response[i]['id_conta']}")
                    continuacao()
                else:
                    print(response)
            
            else:
                invalido()
        else:
            encerramento_conexao(con, cursor)
            invalido()   

    elif resposta1 == "7":
        idconta_despesa = input("Você gostaria de acessar a(s) despesa(s) de qual conta? Digite seu ID: ")
        print("\n")
        print("-------------------------------------------------------------")
        print("-----------FUNCIONALIDADES DE DESPESAS DISPONÍVEIS-----------")
        print("--------------------------DESPESAS---------------------------")
        print("-------------------------------------------------------------")
        print("\n")
        print("1 = Cadastrar novas despesas")
        print("2 = Remover despesas do sistema")
        print("3 = Alterar despesas no sistema")
        print("4 = Listar despesas cadastradas")
        print("\n")
        resposta3 = str(input("Digite o número correspondente ao seu interesse: "))

        if resposta3 == "1":
            con, cursor = conexao_banco_dados()
            try:
                tipo_despesa = input("Qual o tipo de despesa? ALIMENTAÇÃO, EDUCAÇÃO, LAZER, MORADIA, ROUPA, SAÚDE, TRANSPORTE ou OUTROS? ").lower()
                valor_despesa = input("Qual é o valor da despesa? Digite em números: ")
                data_pagamento_esperado = input("Qual é a data de pagamento esperado? Escreva no formato '0000-00-00': ")
                data_pagamento = input("Qual foi a data de pagamento? Escreva no formato '0000-00-00': ")
                cursor.execute(f"INSERT INTO DESPESA VALUES(NULL, '{tipo_despesa}', {valor_despesa}, '{data_pagamento_esperado}', '{data_pagamento}', {idconta_despesa});")
                con.commit()
                encerramento_conexao(con, cursor)
            except Exception as e:
                encerramento_conexao(con, cursor)
                print("Ocorreu o seguinte erro: ")
                print(e)
            finally:
                continuacao()
        elif resposta3 == "2":
            con, cursor = conexao_banco_dados()
            try:
                iddespesa_remover = input("Digite o ID da despesa que deseja remover: ")
                cursor.execute(f"DELETE FROM DESPESA WHERE IDDESPESA = {iddespesa_remover};")
                con.commit()
                encerramento_conexao(con, cursor)
            except Exception as e:
                encerramento_conexao(con, cursor)
                print("Ocorreu o seguinte erro: ")
                print(e)
            finally:
                continuacao()
        elif resposta3 == "3":
            con, cursor = conexao_banco_dados()
            try:
                iddespesa_alterar = input("Digite o ID da despesa que deseja alterar: ")
                alteracao_despesa = input("O que você deseja alterar na despesa? O TIPO, VALOR_EM_REAIS, DATA_PAGAMENTO_ESPERADO, DATA_PAGAMENTO OU ID_CONTA? ").lower()
                
                if alteracao_despesa == "tipo":
                    despesa_tipo_alterar = input("Para qual tipo você deseja alterar? ALIMENTAÇÃO, EDUCAÇÃO, LAZER, MORADIA, ROUPA, SAÚDE, TRANSPORTE ou OUTROS? ").lower()
                    cursor.execute(f"UPDATE DESPESA SET TIPO = '{despesa_tipo_alterar}' WHERE IDDESPESA = {iddespesa_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                elif alteracao_despesa == "valor_em_reais":
                    despesa_valor_alterar = input("Digite para qual valor deseja alterar: ")
                    cursor.execute(f"UPDATE DESPESA SET VALOR_EM_REAIS = {despesa_valor_alterar} WHERE IDDESPESA = {iddespesa_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                elif alteracao_despesa == "data_pagamento_esperado":
                    despesa_data_esperada_alterar = input("Digite para qual data deseja alterar no formato '0000-00-00': ")
                    cursor.execute(f"UPDATE DESPESA SET DATA_PAGAMENTO_ESPERADO = '{despesa_data_esperada_alterar}' WHERE IDDESPESA = {iddespesa_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                elif alteracao_despesa == "data_pagamento":
                    despesa_data_alterar = input("Digite para qual data deseja alterar no formato '0000-00-00': ")
                    cursor.execute(f"UPDATE DESPESA SET DATA_PAGAMENTO = '{despesa_data_alterar}' WHERE IDDESPESA = {iddespesa_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                elif alteracao_despesa == "id_conta":
                    despesa_id_conta_alterar = input("Digite o ID da conta que gostaria de agregar essa despesa: ")
                    cursor.execute(f"UPDATE DESPESA SET ID_CONTA = {despesa_id_conta_alterar} WHERE IDDESPESA = {iddespesa_alterar};")
                    con.commit()
                    encerramento_conexao(con, cursor)
                
                else:
                    encerramento_conexao(con, cursor)
                    invalido()
            except Exception as e:
                encerramento_conexao(con, cursor)
                print("Ocorreu o seguinte erro: ")
                print(e)
            finally:
                continuacao()
        elif resposta3 == "4":
            despesa_tipo_listagem = str(input("Como você gostaria de visualizar suas despesas? Por período(1), tipo(2) ou apenas visualizar tudo(3)? Digite o número de sua preferência: "))
            print("\n")

            if despesa_tipo_listagem == "1":
                request = requests.get("http://localhost:5000/despesa/periodo")
                response = json.loads(request.text)
                if str(response) != "Nao foi possível fazer conexao com o MySQL":
                    print("(*) Ordem das listas: ID DA DESPESA, DATA DE PAGAMENTO, DATA DE PAGAMENTO ESPERADO, TIPO, VALOR EM REAIS E O ID DA CONTA A QUE SE REFERE.")
                    print("=========================================================================================================================================")
                    print("\n")
                    for i in response:
                        print(f"{i}, {response[i]['data_pagamento']}, {response[i]['data_pagamento_esperado']}, {response[i]['tipo']}, {response[i]['valor_em_reais']}, {response[i]['id_conta']}")
                    continuacao()
                else:
                    print(response)
        
            elif despesa_tipo_listagem == "2":
                request = requests.get("http://localhost:5000/despesa/tipo")
                response = json.loads(request.text)
                if str(response) != "Nao foi possível fazer conexao com o MySQL":
                    print("(*) Ordem das listas: ID DA DESPESA, TIPO, VALOR EM REAIS, DATA DE PAGAMENTO ESPERADO, DATA DE PAGAMENTO E O ID DA CONTA A QUE SE REFERE.")
                    print("=========================================================================================================================================")
                    print("\n")
                    for i in response:
                        print(f"{i}, {response[i]['tipo']}, {response[i]['valor_em_reais']}, {response[i]['data_pagamento_esperado']}, {response[i]['data_pagamento']}, {response[i]['id_conta']}")
                    continuacao()
                else:
                    print(response)

            elif despesa_tipo_listagem == "3":
                request = requests.get("http://localhost:5000/despesa/tudo")
                response = json.loads(request.text)
                if str(response) != "Nao foi possível fazer conexao com o MySQL":
                    print("(*) Ordem das listas: ID DA DESPESA, TIPO, VALOR EM REAIS, DATA DE PAGAMENTO ESPERADO, DATA DE PAGAMENTO E O ID DA CONTA A QUE SE REFERE.")
                    print("=========================================================================================================================================")
                    print("\n")
                    for i in response:
                        print(f"{i}, {response[i]['tipo']}, {response[i]['valor_em_reais']}, {response[i]['data_pagamento_esperado']}, {response[i]['data_pagamento']}, {response[i]['id_conta']}")
                    continuacao()
                else:
                    print(response)
            
            else:
                invalido()
        else:
            invalido()
    
    elif resposta1 == "8":
        con, cursor = conexao_banco_dados()
        id_conta_origem = input("Digite o ID da conta de origem que deseja transferir o saldo: ")
        id_conta_destino = input("Digite o ID da conta de destino para onde deseja transferir o saldo: ")
        transferencia = input("Qual o valor que deseja tranferir entre as contas? ")

        # Conta de origem
        cursor.execute(f"SELECT SALDO FROM CONTA WHERE IDCONTA = {id_conta_origem};")
        saldo_origem = cursor.fetchall()
        saldo_origem_f = saldo_origem[0][0]

        # Conta de destino
        cursor.execute(f"SELECT SALDO FROM CONTA WHERE IDCONTA = {id_conta_destino};")
        saldo_destino = cursor.fetchall()
        saldo_destino_f = saldo_destino[0][0]
        
        # Transferindo o saldo
        alteracao_saldo_origem = float(saldo_origem_f) - float(transferencia)
        
        if saldo_origem_f == 0:
            status_transferencia = False
            print("\n")
            print("Sua conta de origem não possui nenhum saldo. Escolha outra para fazer a transferência ou deposite nesta.")
            continuacao()
        else:
            status_transferencia = True
        
        if alteracao_saldo_origem < 0:
            status_transferencia = False
            print("\n")
            print("Sua conta de origem não possui saldo suficiente. Escolha outra para fazer a transferência ou deposite nesta.")
            continuacao()
        else:
            if status_transferencia == True:
                pass
        
        if status_transferencia == True:
            cursor.execute(f"UPDATE CONTA SET SALDO = {alteracao_saldo_origem} WHERE IDCONTA = {id_conta_origem};")
            con.commit()
            alteracao_saldo_destino = saldo_destino_f + float(transferencia)
            cursor.execute(f"UPDATE CONTA SET SALDO = {alteracao_saldo_destino} WHERE IDCONTA = {id_conta_destino};")
            con.commit()
            
            encerramento_conexao(con, cursor)
            continuacao()

    else:
        invalido()

input("\nAperte ENTER para sair do aplicativo.")