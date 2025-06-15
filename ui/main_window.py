from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QLabel, QListWidget

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Campeonato de Futebol")
        self.setFixedSize(1150, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.setup_main_menu()
        self.tabela = QTableWidget()
        self.label = QLabel()
        
    def sair(self):
        self.close()

    def setup_main_menu(self):
        self.clear_layout()
        botoes = [
            ("Sair", self.sair),
            ("Clubes", self.show_submenu),
            ("Artilharia", self.show_artilharia),
            ("Assistências", self.show_assistencias),
            ("Cartões Amarelos", lambda: self.show_cartoes("Amarelo")),
            ("Cartões Vermelhos", lambda: self.show_cartoes("Vermelho")),
            ("Classificação", self.show_classificacao),
        ]
        for texto, acao in botoes:
            btn = QPushButton(texto)
            btn.clicked.connect(acao)
            self.layout.addWidget(btn)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def show_clubes(self):
        dados = self.controller.get_clubes()
        texto = "\n".join([f"{i+1}. {j} - {c} - {g}" for i, (j, c, g) in enumerate(dados)])
        self._msg("Artilharia", texto)

    def show_submenu(self):
        self.clear_layout()

        # Cabeçalho do submenu
        header = QPushButton("Voltar")
        header.clicked.connect(self.setup_main_menu)
        self.layout.addWidget(header)

        # Obtenha os clubes do controller
        clubes = self.controller.get_clubes()  # Retorna lista de tuplas: [(id, nome), (id, nome), ...]

        for clube_id, clube_nome in clubes:
            btn = QPushButton(clube_nome)
            btn.clicked.connect(lambda checked, id_clube=clube_id: self.show_clube_info(int(id_clube)))
            self.layout.addWidget(btn)

    def show_clube_info(self, id_clube):
        self.clear_layout()
        header = QPushButton("Voltar")
        header.clicked.connect(self.show_submenu)
        self.layout.addWidget(header)
        self.clube_list = QListWidget()
        self.info_label = QLabel("Informações do Clube")
        self.jogadores_list = QListWidget()
        self.partidas_list = QListWidget()

        self.layout.addWidget(self.info_label)
        self.layout.addWidget(QLabel("Jogadores:"))
        self.layout.addWidget(self.jogadores_list)
        self.layout.addWidget(QLabel("Partidas:"))
        self.layout.addWidget(self.partidas_list)

        info = self.controller.get_clube_info(id_clube)
        self.info_label.setText(
            f"Clube: {info[0]} | Estádio: {info[1]} | Técnico: {info[2]}\n"
            f"Cartões Vermelhos: {info[3]} | Cartões Amarelos: {info[4]}"
        )

        self.jogadores_list.clear()
        jogadores = self.controller.get_jogadores(id_clube)
        for j in jogadores:
            self.jogadores_list.addItem(f"{j[0]} - {j[1]}")

        self.partidas_list.clear()
        partidas = self.controller.get_partidas(id_clube)
        for p in partidas:
            self.partidas_list.addItem(f"{p[0]} {p[1]} x {p[2]} {p[3]} - {p[4]} ({p[5]})")

    def show_artilharia(self):
        dados = self.controller.get_artilharia()
        self.tabela.clear()
        self.tabela.setRowCount(len(dados))
        self.tabela.setColumnCount(3)
        self.tabela.setHorizontalHeaderLabels([
            "Jogador", "Clube", "Quantidade"
        ])

        for linha, row_data in enumerate(dados):
            for coluna, item in enumerate(row_data):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(str(item)))
        self.label.setText("Artilharia:")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.tabela)

    def show_assistencias(self):
        dados = self.controller.get_assistencias()
        self.tabela.clear()
        self.tabela.setRowCount(len(dados))
        self.tabela.setColumnCount(3)
        self.tabela.setHorizontalHeaderLabels([
            "Jogador", "Clube", "Quantidade"
        ])

        for linha, row_data in enumerate(dados):
            for coluna, item in enumerate(row_data):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(str(item)))
        self.label.setText("Assistências:")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.tabela)

    def show_cartoes(self, tipo):
        dados = self.controller.get_cartoes(tipo)
        self.tabela.clear()
        self.tabela.setRowCount(len(dados))
        self.tabela.setColumnCount(3)
        self.tabela.setHorizontalHeaderLabels([
            "Jogador", "Clube", "Quantidade"
        ])

        for linha, row_data in enumerate(dados):
            for coluna, item in enumerate(row_data):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(str(item)))
        self.label.setText(f"Cartões {tipo}s:")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.tabela)

    def show_classificacao(self):
        dados = self.controller.get_classificacao()
        self.tabela.clear()
        self.tabela.setRowCount(len(dados))
        self.tabela.setColumnCount(11)
        self.tabela.setHorizontalHeaderLabels([
            "Clube", "Pontos", "Partidas", "Vitórias", "Empates", "Derrotas",
            "Gols Pró", "Gols Contra", "Saldo de Gols", "Cartões Amarelos", "Cartões Vermelhos"
        ])

        for linha, row_data in enumerate(dados):
            for coluna, item in enumerate(row_data):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(str(item)))
        self.label.setText("Classificação:")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.tabela)

    def _msg(self, titulo, conteudo):
        box = QMessageBox(self)
        box.setWindowTitle(titulo)
        box.setText(conteudo)
        box.exec()
