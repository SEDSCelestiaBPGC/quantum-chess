
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from PySide2.QtCore import QFile, QTextStream
from PySide2.QtGui import QPixmap
import sys
import chess
from functools import partial

from PySide2.QtCore import Qt
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui

sys.path.append('hichess-mod\examples\BoardWidgetExample') 
sys.path.append('hichess-mod\hichess') 
import hichess
from context import resources
from Quant import *

from hichess import CellWidget, _PromotionDialog, IllegalMove

class BoardWidget_new(hichess.BoardWidget):

    moveMade = QtCore.Signal(chess.Move)

    def _push(self, move: chess.Move) -> None:
        self._updateJustMovedCells(False)

        turn = self.board.turn

        if self._isCellAccessible(self.cellWidgetAtSquare(move.from_square)) \
                and move.promotion is None and self.isPseudoLegalPromotion(move):
            w = self.cellWidgetAtSquare(move.to_square)

            promotionDialog = _PromotionDialog(parent=self, color=turn, order=self._flipped)
            if not self._flipped and turn:
                promotionDialog.move(self.mapToGlobal(w.pos()))
            else:
                promotionDialog.move(self.mapToGlobal(QtCore.QPoint(w.x(), w.y() - 3 * w.height())))
            promotionDialog.setFixedWidth(w.width())
            promotionDialog.setFixedHeight(4 * w.height())

            exitCode = promotionDialog.exec_()
            if exitCode == _PromotionDialog.Accepted:
                move.promotion = promotionDialog.chosenPiece
            elif exitCode == _PromotionDialog.Rejected:
                self.foreachCells(CellWidget.unhighlight, lambda w: w.setChecked(False))
                return

        if not self.board.is_legal(move) or move.null():
            raise IllegalMove(f"illegal move {move} by ")
        # logging.debug(f"\n{self.board.lan(move)} ({move.from_square} -> {move.to_square})")

        san = self.board.san(move)
        self.board.push(move)
        # logging.debug(f"\n{self.board}\n")

        self._updateJustMovedCells(True)
        self.popStack.clear()

        self.foreachCells(CellWidget.unmark, CellWidget.unhighlight)
        self.synchronizeAndUpdateStyles()

        self.moveMade.emit(move)
        self.movePushed.emit(san)


    @QtCore.Slot()
    def _onCellWidgetClicked(self, w):
        self.cellWidgetClickedSig.emit(w)
        if w.highlighted:
            self.pushPiece(self.squareOf(w), self.lastCheckedCellWidget)
            self.unmarkCells()
        elif not w.piece:
            self.foreachCells(hichess.CellWidget.unhighlight, hichess.CellWidget.unmark,
                              lambda w: w.setChecked(False))
        else:
            self.unmarkCells()
    cellWidgetClickedSig = QtCore.Signal(hichess.CellWidget)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.quantum_mode = False
        self.split_turn = False

        self.centralWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # Initialize board
        self.boardWidget = BoardWidget_new()
        #quant stuff here plis
        self.Qpieces = []
        self.boardWidget.foreachCells(self.setQboard)

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

        self.boardWidget.moveMade.connect(self.checkQmove)
    
    def setQboard(self, cellWid):
        q_pc = quantum_obj(self.boardWidget.squareOf(cellWid), cellWid.getPiece())
        self.Qpieces.append(q_pc)


    def checkQmove(self, move):
        qObj, qObj_State = self.findQobj(move.from_square)
        print(qObj.piece, qObj.qnum[qObj_State][1])
        if(self.quantum_mode):
            self.boardWidget.board.turn = not self.boardWidget.board.turn
            self.boardWidget.setPieceAt(move.from_square, qObj.piece)
            self.split_turn = True

        qObj.qnum[qObj_State][0] = move.to_square


    def split_move(self, qObj, qObj_State, square1, square2):
        qObj.split(qObj.qnum[qObj_State])
        pass

    def findQobj(self, square):
        for pc in self.Qpieces:
            for state in pc.qnum.keys():
                if(pc.qnum[state][0] == square):
                    return pc, state

    def keyPressEvent(self, event): # press shift to toggle quantum mode
        if(event.key()==Qt.Key_Shift):
            self.quantum_mode = not self.quantum_mode
            # self.split_turn = True




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    # mainWindow.boardWidget.setPieceAt(chess.D4,chess.Piece(chess.PAWN,chess.WHITE))    
    # mainWindow.boardWidget.moveMade.connect(mainWindow.sayHi)
    # mainWindow.boardWidget.cellWidgetClickedSig.connect(mainWindow.on_click_rel)

    
    sys.exit(app.exec_())
