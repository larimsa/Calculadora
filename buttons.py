from PySide6.QtCore import Slot  
from PySide6.QtWidgets import QPushButton, QGridLayout
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber
import math  

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display  
    from info import Info  
    from main_window import MainWindow 

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['Clear', '◂', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['Neg',  '0', '.', '='],
        ]

        self.display = display
        self.info = info
        self.window =  window
        
        #variáveis para rastrear o estado da calculadora
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        #Atualiza a equação exibida na Info
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        #Conecta os sinais dos botões às funções correspondentes
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for rowNumber, rowData in enumerate(self._gridMask):
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)
                
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)
                
                #Adiciona o botão ao layout da grade na posição correspondente
                self.addWidget(button, rowNumber, colNumber)

                #Cria um slot específico para o botão e conecta ao sinal clicked
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        #Conecta o sinal clicked do botão ao slot fornecido
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        #Configurações especiais para botões com funcionalidades específicas
        text = button.text()
        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)
        
        if text in '+-/*^':
            self._connectButtonClicked(button, self._makeSlot(self._configLeftOp, text))

        if text == '=':
            self._connectButtonClicked(button, self._eq)

        if text == '◂':
            self._connectButtonClicked(button, self.display.backspace)

    def _makeSlot(self, func, *args, **kwargs):
         #Função para criar slots com argumentos específicos
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot
    
    @Slot()
    def _invertNumber(self):
        #Inverte o número exibido no display
        displayText = self.display.text()
        if not isValidNumber(displayText):
            return
        
        newNumber = -float(displayText)
        self.display.setText(str(newNumber))
    
    @Slot()
    def _insertToDisplay(self, text):
        #Insere texto no display conforme a interação do usuário
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return
        
        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        #Limpa todos os dados e reseta a calculadora para o estado inicial
        self._left = None
        self._right = None
        self.op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self, text):
        #Configura o operador esquerdo e inicia a construção da equação
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Conta incompleta')
            return
        
        if self._left is None:
            self._left = float(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op}'

    @Slot()
    def _eq(self):
        #Calcula o resultado da equação e atualiza o display e a info
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta incompleta')
            return
        
        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Divisão por zero')
        except OverflowError:
            self._showError('Essa conta não pode ser realizada')

        #Limpa o display e exibe o resultado na info
        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        self.display.setFocus()

        if result == 'error':
            self._left = None
        
    @Slot()
    def _backspace(self):
        #Função para remover o último caractere do display
        self.display.backspace()
        self.display.setFocus()

    def _showError(self, text):
        #Exibe uma caixa de mensagem de erro
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.exec()
        self.display.setFocus()
