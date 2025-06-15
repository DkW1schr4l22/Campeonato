class CampeonatoController:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_clubes(self):
        self.cursor.execute("SELECT id_clube, nome FROM Clubes")
        return self.cursor.fetchall()
    
    def get_clube_info(self, id_clube):
        self.cursor.execute("""
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
        info = self.cursor.fetchone()
        return info

    def get_jogadores(self, id_clube):
        self.cursor.execute("""
            SELECT j.nome, j.posicao
            FROM Jogadores j
            WHERE j.id_clube = ?
        """, (id_clube,))
        result = self.cursor.fetchall()
        return result

    def get_partidas(self, id_clube):
        self.cursor.execute("""
            SELECT 
                clube_casa.nome,
                p.gols_mandante,
                p.gols_visitante,
                clube_visitante.nome,
                e.nome,
                p.data_partida
            FROM Partidas p
            INNER JOIN Clubes clube_casa ON p.id_clube_mandante = clube_casa.id_clube
            LEFT JOIN Clubes clube_visitante ON p.id_clube_visitante = clube_visitante.id_clube
            INNER JOIN Estadios e ON e.id_estadio = p.id_estadio
            WHERE clube_casa.id_clube = ? OR clube_visitante.id_clube = ?
        """, (id_clube, id_clube,))
        result = self.cursor.fetchall()
        return result

    def get_artilharia(self):
        self.cursor.execute("""
            SELECT j.nome, c.nome, COUNT(g.id_gol) AS gols
            FROM Gols g 
            INNER JOIN Jogadores j ON j.id_jogador = g.id_jogador
            LEFT JOIN Clubes c ON c.id_clube = j.id_clube
            GROUP BY j.nome, c.nome
            ORDER BY gols DESC
        """)
        return self.cursor.fetchall()

    def get_assistencias(self):
        self.cursor.execute("""
            SELECT j.nome, c.nome, COUNT(g.id_gol) AS assistencias
            FROM Gols g 
            INNER JOIN Jogadores j ON j.id_jogador = g.id_jogador_assistencia
            LEFT JOIN Clubes c ON c.id_clube = j.id_clube
            GROUP BY j.nome, c.nome
            ORDER BY assistencias DESC
        """)
        return self.cursor.fetchall()

    def get_cartoes(self, tipo):
        self.cursor.execute(f"""
            SELECT j.nome, c.nome, COUNT(ca.id_cartao) AS total
            FROM Cartoes ca
            INNER JOIN Jogadores j ON j.id_jogador = ca.id_jogador
            INNER JOIN Clubes c ON c.id_clube = j.id_clube
            WHERE ca.tipo = '{tipo}'
            GROUP BY j.nome
            ORDER BY total DESC
        """)
        return self.cursor.fetchall()

    def get_classificacao(self):
        self.cursor.execute("""
            SELECT 
                c.nome AS clube,
                cl.pontos,
                cl.partidas,
                cl.vitorias,
                cl.empates,
                cl.derrotas,
                cl.gols_pro,
                cl.gols_contra,
                cl.saldo_gols,
                COALESCE(ca.amarelos, 0) AS cartoes_amarelos,
                COALESCE(cv.vermelhos, 0) AS cartoes_vermelhos
            FROM Classificacao cl
            JOIN Clubes c ON cl.id_clube = c.id_clube

            LEFT JOIN (
                SELECT 
                    j.id_clube,
                    COUNT(CASE WHEN ca.tipo = 'Amarelo' THEN 1 END) AS amarelos
                FROM Cartoes ca
                JOIN Jogadores j ON ca.id_jogador = j.id_jogador
                GROUP BY j.id_clube
            ) ca ON ca.id_clube = c.id_clube

            LEFT JOIN (
                SELECT 
                    t.id_clube,
                    COUNT(CASE WHEN ca.tipo = 'Vermelho' THEN 1 END) AS vermelhos
                FROM Cartoes ca
                JOIN Treinadores t ON ca.id_treinador = t.id_treinador
                GROUP BY t.id_clube
            ) cv ON cv.id_clube = c.id_clube

            ORDER BY 
                cl.pontos DESC,
                cl.vitorias DESC,
                cl.saldo_gols DESC,
                cl.gols_pro DESC,
                cartoes_vermelhos ASC,
                cartoes_amarelos ASC;

        """)
        return self.cursor.fetchall()
