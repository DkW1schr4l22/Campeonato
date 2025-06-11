import sqlite3

conn = sqlite3.connect("C:/Users/comer/OneDrive/Área de Trabalho/Faculdade/Prog/sqlite-tools-win-x64-3490100/campeonato.db")
cursor = conn.cursor()

def menu():
    print("Menu:")
    print("0. Sair")
    print("1. Informações de um time")
    print("2. Artilaria")
    print("3. Assistência")
    print("4. Cartões amarelos")
    print("5. Cartões vermelhos")
    print("6. Classificação")
    opcao = input("Escolha uma opção: ")
    return opcao

def listar_gols(id_clube: int):
    cursor.execute("""
        SELECT 
            g.id_gol,
            g.minuto, 
            g.id_partida, 
            autor.nome AS autor_nome, 
            assistente.nome AS assistente_nome
        FROM Gols g
        INNER JOIN Jogadores autor ON g.id_jogador = autor.id_jogador
        LEFT JOIN Jogadores assistente ON g.id_jogador_assistencia = assistente.id_jogador
        WHERE autor.id_clube = ?
    """, (id_clube,))
    gols = cursor.fetchall()
    print("Lista de Gols:")
    for gol in gols:
        print(f"ID: {gol[0]}, Minuto: {gol[1]}, Autor: {gol[3]}, Assistente: {gol[4]}, Partida ID: {gol[2]}")

def clubes():
    cursor.execute("SELECT id_clube, nome FROM Clubes")
    clubes = cursor.fetchall()
    print("Lista de Clubes:")
    for clube in clubes:
        print(f"ID: {clube[0]}, Nome: {clube[1]}")

def submenu():
    print("Submenu:")
    print("0. Voltar")
    print("1. Listar Gols")
    print("2. Visualizar informações do clube")
    print("3. Listar jogadores")
    print("4. Listar jogos")
    opcao = input("Escolha uma opção: ")
    return opcao

opcao = menu()

while opcao != "0":
    if opcao == "1":
        clubes()
        print("Selecione o ID do clube:")
        id_clube = int(input("Digite o ID do clube: "))
        submenu_opcao = submenu()
        
        while submenu_opcao != "0":
            if submenu_opcao == "1":
                listar_gols(id_clube)
            elif submenu_opcao == "2":
                cursor.execute("""
                    SELECT 
                        c.nome AS clube, 
                        e.nome AS estadio, 
                        t.nome AS treinador,
                        SUM(CASE WHEN ca.tipo = 'Vermelho' THEN 1 ELSE 0 END) AS cartoes_vermelhos,
                        SUM(CASE WHEN ca.tipo = 'Amarelo' THEN 1 ELSE 0 END) AS cartoes_amarelos
                    FROM Clubes c
                    INNER JOIN Estadios e ON e.id_estadio = c.id_estadio
                    INNER JOIN Treinadores t ON t.id_clube = c.id_clube
                    LEFT JOIN Cartoes ca ON ca.id_treinador IN (
                        SELECT id_treinador FROM Treinadores WHERE id_clube = c.id_clube
                    )
                    WHERE c.id_clube = ?
                    GROUP BY c.nome, e.nome, t.nome
                """, (id_clube,))
                
                info = cursor.fetchone()
                if info:
                    print(f"Clube: {info[0]}")
                    print(f"Estádio: {info[1]}")
                    print(f"Técnico: {info[2]}")
                    print(f"Cartões Vermelhos: {info[3]}")
                    print(f"Cartões Amarelos: {info[4]}")
                else:
                    print("Nenhuma informação encontrada.")

            elif submenu_opcao == "3":
                gol_id = int(input("Digite o ID do gol a ser removido: "))
                cursor.execute("DELETE FROM Gols WHERE id = ?", (gol_id,))
                conn.commit()
                print("Gol removido com sucesso!")
            else:
                print("Opção inválida. Tente novamente.")
            
            submenu_opcao = submenu()
    
    elif opcao == "2":        
        cursor.execute("""
                        SELECT 
                            c.nome, 
                            e.nome, 
                            t.nome, 
                            count(c.cartao_vermelho) AS cartao_vermelho,
                            count(c.cartao_amarelo) AS cartao_amarelo 
                        FROM Clubes c 
                        INNER JOIN Estadios e ON e.id_estadio = c.id_clube
                        INNER JOIN Tecnicos t ON t.id_clube = c.id_clube
                        WHERE c.id_clube = ?
                        """, 
                       (id_clube,))
        conn.commit()
        print("Informações do clube visualizadas com sucesso!")

    elif opcao == "3":
        gol_id = int(input("Digite o ID do gol a ser removido: "))
        cursor.execute("DELETE FROM Gols WHERE id = ?", (gol_id,))
        conn.commit()
        print("Gol removido com sucesso!")
    
    else:
        print("Opção inválida. Tente novamente.")
    
    opcao = menu()