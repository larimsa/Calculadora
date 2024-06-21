from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        #Cria um QWidget central para a janela principal
        self.cw = QWidget()
  
        #Cria um QVBoxLayout para organizar os widgets verticalmente
        self.vLayout = QVBoxLayout()  
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)
        self.setWindowTitle('Calculadora')
 
    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        # Adiciona um widget ao QVBoxLayout da janela principal
        self.vLayout.addWidget(widget)

    def makeMsgBox(self):
        # Cria e retorna uma caixa de mensagem associada à janela principal
        return QMessageBox(self)
