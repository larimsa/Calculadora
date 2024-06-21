import sys
from buttons import ButtonsGrid 
from display import Display
from info import Info 
from main_window import MainWindow 
from PySide6.QtWidgets import QApplication
from variables import WINDOW_ICON_PATH 

if __name__ == '__main__':
    #Inicializa a aplicação Qt
    app = QApplication(sys.argv)

    #Cria a janela principal da aplicação
    window = MainWindow()

    #Adiciona um widget de informação à vertical layout da janela
    info = Info('teste')
    window.addWidgetToVLayout(info)

    #Cria e adiciona o display à vertical layout da janela
    display = Display()
    window.addWidgetToVLayout(display)

    #Cria e adiciona a grade de botões à vertical layout da janela,
    #passando o display, info e a própria janela como parâmetros
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    #Ajusta o tamanho da janela para se adequar ao conteúdo e a exibe
    window.adjustFixedSize()
    window.show()
  
    app.exec()
