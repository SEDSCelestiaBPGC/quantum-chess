import hichess
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from PySide2.QtCore import QFile, QTextStream
from PySide2.QtGui import QPixmap
import sys
import chess

from context import resources


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # Initialize board
        self.boardWidget = hichess.BoardWidget()
        # The user can interract with both colors of the board
        self.boardWidget.accessibleSides = hichess.BOTH_SIDES
        # Enable drag and drop
        self.boardWidget.dragAndDrop = True

        # background image
        self.boardWidget.setBoardPixmap(defaultPixmap=QPixmap(":/images/chessboard.png"),
                                        flippedPixmap=QPixmap(":/images/flipped_chessboard.png"))

        # qss
        qss = QFile(":/style/styles.css")
        if qss.open(QFile.ReadOnly):
            textStream = QTextStream(qss)
            self.boardWidget.setStyleSheet(textStream.readAll())

        self.flipButton = QPushButton("Flip")
        # flip the board when the button is pressed
        self.flipButton.clicked.connect(self.boardWidget.flip)

        self.mainLayout.addWidget(self.boardWidget)
        self.mainLayout.addWidget(self.flipButton)
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    mainWindow.boardWidget.setPieceAt(chess.D4,chess.Piece(chess.PAWN,chess.BLACK))    
    sys.exit(app.exec_())
