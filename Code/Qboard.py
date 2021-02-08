
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from PySide2.QtCore import QFile, QObject, QTextStream
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

    split_turn = False # //HACK find a way to connect this to the split_turn variable of main or vice versa
    moveMade = QtCore.Signal(chess.Move)
    cellWidgetClickedSig = QtCore.Signal(hichess.CellWidget)

    def pieceCanBePushedTo(self, w: CellWidget):
        """ Yields the numbers of squares that the piece on the cell widget can be legally pushed
        to. """

        # //TODO find a way to add legal moves for entanglement here
        for move in self.board.legal_moves:
            if move.from_square == self.squareOf(w):
                yield move.to_square

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

    def _updateJustMovedCells(self, justMoved):
        # //TODO finish this func
        pass

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

    @QtCore.Slot()
    def _onCellWidgetToggled(self, w: CellWidget, toggled: bool):
        if toggled:
            if self.board.turn != w.getPiece().color or not self._isCellAccessible(w):
                w.setChecked(False)
                return

            if self.blockBoardOnPop and self.popStack:
                w.setChecked(False)
                return
            
            if not len(self.board.move_stack) <1 and self.split_turn:
                if self.board.peek().from_square != self.squareOf(w):
                    return 
            # //FIXME this lets player check multiple pcs (check stylesheet for 'checked' variable)

            def callback(_w: CellWidget):
                if _w != w:
                    _w.setChecked(False)

            self.foreachCells(CellWidget.unmark, CellWidget.unhighlight, callback)
            if not self.highlightLegalMoveCellsFor(w):
                w.setChecked(False)
            self.lastCheckedCellWidget = w
        else:
            self.unhighlightCells()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.previous_move = chess.Move(chess.A1, chess.A2) # //HACK get previous move from board?

        self.centralWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # Initialize board
        self.boardWidget = BoardWidget_new()
        #quant stuff here plis
        self.Qpieces = []
        self.quantum_mode = False
        self.split_turn = False # for second move when split
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
        '''
        sets initial qObjs when game starts
        '''
        if cellWid.getPiece() is not None:
            q_pc = quantum_obj(self.boardWidget.squareOf(cellWid), cellWid.getPiece())
            self.Qpieces.append(q_pc)

    def updateQboard(self, turn):
        '''
        turn = True if white to play
        Updates board according to Qpieces, useful when calling measure
        '''
        self.boardWidget.board = chess.Board(fen = None) 
        for qObj in self.Qpieces:
            for state in qObj.qnum.keys():
                self.boardWidget.board.set_piece_at(qObj.qnum[state][0], qObj.piece)
        self.boardWidget.board.turn = turn
        self.boardWidget._synchronize()
        # self.boardWidget.board.move_stack.append(self.previous_move)
        # print(self.previous_move)

    def checkQmove(self, move):
        '''
        Handles all special moves for quantum chess
        '''
        print(self.boardWidget.board.move_stack, len(self.boardWidget.board.move_stack))
        qObj, qObj_state = self.findQobj(move.from_square)
        print(qObj.piece, qObj.qnum[qObj_state][1])

        # Attacking, measures if attacked/attacking has more than one state/add 
        # //HACK Should probably be another function (?)
        if self.findQobj(move.to_square) is not None:
            qObj_attacked, qObj_attacked_state = self.findQobj(move.to_square)
            self.quantum_mode = False # //HACK shouldn't disable quantum_mode if we allow shrodinger's pcs
            self.split_turn = False
            self.boardWidget.split_turn = False

            if qObj.qnum[qObj_state][1] !=1:
                qObj.meas()
                self.updateQboard(turn = not qObj.piece.symbol().isupper()) 
                if qObj.qnum['0'][0] == move.from_square: # attack*ing* piece exists
                    self.checkQmove(move)
                return

            if  qObj_attacked.qnum[qObj_attacked_state][1] !=1:
                qObj_attacked.meas()
                if qObj_attacked.qnum['0'][0] != move.to_square: # attack*ed* piece doen't exist
                    qObj.qnum[qObj_state][0] = move.to_square

                self.updateQboard(turn = not qObj.piece.symbol().isupper()) 
                self.checkQmove(move)
                return

            del qObj_attacked.qnum[qObj_attacked_state]
            qObj.qnum[qObj_state][0] = move.to_square
            self.updateQboard(turn= not qObj.piece.symbol().isupper())
            return

        if not self.split_turn:
            if(self.quantum_mode):
                self.boardWidget.board.turn = not self.boardWidget.board.turn
                self.boardWidget.setPieceAt(move.from_square, qObj.piece)
                self.split_turn = True
                self.boardWidget.split_turn = True
                self.previous_move = move
                self.boardWidget.board.move_stack.append(self.previous_move)
            else: 
                qObj.qnum[qObj_state][0] = move.to_square
        else:
            self.split_move(qObj, qObj_state, move.to_square, self.previous_move.to_square)

    def split_move(self, qObj, qObj_State, square1, square2):
        qObj.split(qObj_State, square1, square2)
        self.split_turn = False
        self.boardWidget.split_turn = False
        self.quantum_mode = False
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
