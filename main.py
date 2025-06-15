import sys
from PySide6.QtWidgets import QApplication
from database.connection import DatabaseConnection
from controllers.campeonato_controller import CampeonatoController
from ui.main_window import MainWindow

if __name__ == "__main__":
    db = DatabaseConnection("C:/Users/jessi/OneDrive/Documentos/Faculdade/Banco de dados/Campeonato/campeonato_final_dupla.db")
    conn = db.connect()
    cursor = db.get_cursor()

    controller = CampeonatoController(cursor)

    app = QApplication(sys.argv)
    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec())
