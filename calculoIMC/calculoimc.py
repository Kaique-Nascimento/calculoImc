from conexao import conectarBanco
import sqlite3 as bd
import matplotlib.pyplot as plt
import numpy as np



print(f"{'-='*5} Calculadora de IMC {'-='*5}")
existe = ""
nomeBanco = ""
idadeBanco = 0
pesoBanco = 0.0
alturaBanco = 0.0
classificacao = ""

def listarPessoas():
    try:
        conn = bd.connect('imc.db')
        cursor = conn.cursor()
        listaPessoa = "SELECT * FROM tb01_pessoa"
        cursor.execute(listaPessoa)
        pessoas = cursor.fetchall()
        if not pessoas:
            print("Não há dados cadastrados!")
            input()
            return False
        else:
            for pessoa in pessoas:
                print(f"""Id: {pessoa[0]}, Nome: {pessoa[1]}, Idade: {pessoa[2]}, Peso: {pessoa[3]}, Altura: {pessoa[4]}, Classificação: {pessoa[5]}
                    {'=-'*10}""")
            return True
    except Exception as e:
        print("DEU ERRO: " + str(e))
        return False
    finally:
        conn.close()

        
def calculoImc(nome, idade, altura, peso):
    global classificacao
    imc = peso / (altura**2)
    if imc < 18.5:
        classificacao = "Abaixo do peso normal"
    elif 18.5 <= imc < 25:
        classificacao = "Peso normal"
    elif 25.0 <= imc < 30:
        classificacao = "Excesso de Peso"
    elif 30 <= imc < 35:
        classificacao = "Obesidade Classe I"
    elif 35 <= imc < 40:
        classificacao = "Obesidade Classe II"
    else:
        classificacao = "Obesidade Classe III"
    return f"Olá, {nome}. \nVocê tem {idade} anos, tem {altura}m e pesa {peso}kg. Seu IMC é de: {imc:.2f}. Isso indica que sua classificação é: {classificacao}"

def dadosImc():
    while True:   
        try:
            nomePessoa = input("Informe seu nome: ")
            idadePessoa = int(input("Digite sua idade: "))
            alturaPessoa = float(input("Digite sua altura em metros: "))
            pesoPessoa = float(input("Digite seu peso em kg: "))
        except ValueError:
            print("Por favor, insira os dados corretamente!")
            continue 
        except Exception as e:
            print(f"Erro inesperado: {e}")
            continue  
        else:
            print(calculoImc(nomePessoa, idadePessoa, alturaPessoa, pesoPessoa))
            cadastrarPessoa(nomePessoa, idadePessoa, alturaPessoa, pesoPessoa, classificacao)

            while True:
                outra = input("Deseja cadastrar outra pessoa? [s/n]: ").lower()
                if outra == "s":
                    break 
                elif outra == "n":
                    return 
                else:
                    print("Escolha inválida. Por favor, escolha entre 's' ou 'n'.")

def cadastrarPessoa(nome, idade, altura, peso, classificacao):
    try:
        conn = bd.connect('imc.db')
        cursor = conn.cursor()
        dadosPessoa = (nome, idade, peso, altura, classificacao)
        inserirPessoa = """
                INSERT INTO tb01_pessoa (tb01_nome, tb01_idade, tb01_peso, tb01_altura, tb01_classificacao)
                VALUES (?,?,?,?,?)"""
        cursor.execute(inserirPessoa, dadosPessoa)
        conn.commit()
    except Exception as e:
        print("Erro ao cadastrar pessoa: " + str(e))
    finally:
        conn.close()
def editarPessoas():
    if not listarPessoas():
        return
    try:
        escolhaPessoa = input("Digite o ID da pessoa que quer editar [0 para sair]: ").strip()
        if escolhaPessoa == '0':
            return
        idEscolha = int(escolhaPessoa)  
    except ValueError:
        print("Digite um número válido.")
        editarPessoas()
        return 
    else:
        pessoaEspecifica(idEscolha)  
        if existe == 'sim':
            try:
                print("Edite os dados [deixe vazio para não alterar]")

        
                novoNome = input(f"Digite o novo nome [Atual: {nomeBanco}]: ").strip()
                if novoNome == "":
                    novoNome = nomeBanco

                novaIdadeInput = input(f"Digite a nova idade [Atual: {idadeBanco}]: ").strip()
                if novaIdadeInput == "":
                    novaIdade = idadeBanco 
                else:
                    novaIdade = int(novaIdadeInput)  
                
                novaAlturaInput = input(f"Digite a nova altura [Atual: {alturaBanco}]: ").strip()
                if novaAlturaInput == "":
                    novaAltura = alturaBanco  
                else:
                    novaAltura = float(novaAlturaInput) 
                    
                novoPesoInput = input(f"Digite o novo peso [Atual: {pesoBanco}]: ").strip()
                if novoPesoInput == "":
                    novoPeso = pesoBanco 
                else:
                    novoPeso = float(novoPesoInput) 
 
                print(f"Valores atualizados: Nome: {novoNome}, Idade: {novaIdade}, Altura: {novaAltura}, Peso: {novoPeso}")
                calculoImc(novoNome, novaIdade, novaAltura, novoPeso)

                conn = bd.connect('imc.db')
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE tb01_pessoa SET tb01_nome = ?, tb01_idade = ?, tb01_peso = ?, tb01_altura = ?, tb01_classificacao = ? WHERE tb01_id = ?",(novoNome, novaIdade, novoPeso, novaAltura, classificacao, idEscolha))
                conn.commit()
                print("Dados editados com sucesso.")
            except ValueError:
                print("Erro: Digite todos os dados corretamente.")
            finally:
                if conn:
                    conn.close()
        else:
            print("Essa pessoa não existe, escolha outra.")
            editarPessoas()






def apagarTudo():
    while True:
        escolhaApagar = input("Deseja apagar todos os dados do sistema? [s/n] ").lower()
        if escolhaApagar == 's':
            try:
                conn = bd.connect('imc.db')
                cursor = conn.cursor()
                apagar = "DELETE FROM tb01_pessoa"
                cursor.execute(apagar)
                conn.commit()
                print("Todos os dados apagados!")
            except Exception as e:
                print("Deu erro: " + str(e))
            finally:
                conn.close()
            break
        elif escolhaApagar == 'n':
            input("Ok! Operação cancelada.")
            break
        else:
            print("Digite 's' para sim ou 'n' para não.")

def pessoaEspecifica(idPessoa):
    global existe, nomeBanco, idadeBanco, pesoBanco, alturaBanco, classificacao
    conn = None
    try:
        conn = bd.connect('imc.db')
        cursor = conn.cursor()
        cursor.execute("SELECT tb01_nome, tb01_idade, tb01_peso, tb01_altura FROM tb01_pessoa WHERE tb01_id = ?", (idPessoa,))
        pessoa = cursor.fetchone()
        if pessoa:
            nomeBanco, idadeBanco, pesoBanco, alturaBanco = pessoa
            existe = "sim"
        else:
            existe = "não"
            nomeBanco = idadeBanco = pesoBanco = alturaBanco = None 
    finally:
        if conn:
            conn.close()

def mostrarGrafico():
    try:
        conn = bd.connect('imc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT tb01_classificacao, count(*) as quantidade from tb01_pessoa group by tb01_classificacao')
        pessoas = cursor.fetchall()
        if not pessoas:
            print("Não há dados cadastrados!")
            input()
            return
        classificacoes = []
        quantidades = []
        for pessoa in pessoas:
            classificacoes.append(pessoa[0])
            quantidades.append(pessoa[1])
        x = np.array(classificacoes)
        y = np.array(quantidades)
        plt.xlabel("Classificação")
        plt.ylabel("Quantidade")
        plt.title("Pessoas")
        plt.gca().yaxis.get_major_locator().set_params(integer=True)
        plt.bar(x,y)
        #Se estiver usando o Google Shell Cloud, não será mostrado o gráfico
        plt.show()

    except Exception as e:
        print("Deu erro: "+e)
            
def apagarPessoa():
    if not listarPessoas():  
        return
    escolhaPessoa = input("Qual pessoa você quer apagar? (Digite o ID ou 0 para sair): ").strip()
    if escolhaPessoa == '0':
        return  

    try:
        idEscolha = int(escolhaPessoa)  
        pessoaEspecifica(idEscolha)
        
        if existe == 'sim':
            while True:
                escolha = input("Tem certeza? [s/n]").strip().lower()
                if escolha == 's':
                    try:
                        conn = bd.connect('imc.db')
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM tb01_pessoa WHERE tb01_id = ?", (idEscolha,))
                        conn.commit()
                        print("Pessoa apagada com sucesso.")
                    except Exception as e:
                        print("Deu erro: " + str(e))
                    finally:
                        if conn:
                            conn.close()
                    break
                elif escolha == 'n':
                    print("Ok! Operação cancelada")
                    return
                else:
                    print("Escolha entre s ou n: ")

        else:
            print("Essa pessoa não existe.")
            apagarPessoa() 
            
    except ValueError:
        print("ID inválido. Por favor, insira um número inteiro válido.")
        apagarPessoa()  

def obterEscolha():
    conectarBanco()
    while True:
        try:
            escolha = int(input("""O que você deseja fazer?
                        1 - Cadastrar uma nova pessoa
                        2 - Listar as pessoas cadastradas
                        3 - Editar os dados de alguma pessoa
                        4 - Apagar alguma pessoa
                        5 - Apagar todos os dados cadastrados
                        6 - Gerar Gráfico
                        0 - Sair do programa
                            
                        : """))
            return escolha
        except ValueError:
            print("Por favor, digite um número válido.")

while True:
    escolha = obterEscolha()
    if escolha == 0:
        print("Tudo bem, até mais!")
        break
    elif escolha == 1:
        dadosImc()  
    elif escolha == 2:
        listarPessoas()
    elif escolha == 3:
        editarPessoas()
    elif escolha == 4:
        apagarPessoa()
    elif escolha == 5:
        apagarTudo()
    elif escolha == 6:
        mostrarGrafico()
    else:
        print("Escolha inválida. Tente novamente.")

#v4 
# opções: 1✓, 2✓, 3✓, 4✓ ,5✓, 6✓