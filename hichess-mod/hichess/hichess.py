# -*- coding: utf-8 -*-
#
# This file is part of the hichesslib project.
# Copyright (C) 2019-2020 Haik Sargsian <haiksargsian6@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it In the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
from collections import deque
from enum import Enum
from functools import partial
from typing import Optional, Mapping, Generator, Callable, Any, Deque, Coroutine

import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui

import chess
import chess.engine

import asyncio


class NotAKingError(Exception):
    pass


class IllegalMove(Exception):
    pass


class CellWidget(QtWidgets.QPushButton):
    """ A `QPushButton` representing a single cell of chess board.
    CellWidget can be either a chess piece or an empty cell of the
    board. It can be marked with different colors.

    `CellWidget` by default represents an empty cell.
    """

    designated = QtCore.Signal(bool)
    """ Indicates that the setter of `marked` property has been called. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._piece = None
        self._isInCheck = False
        self._isHighlighted = False
        self._isMarked = False
        self._justMoved = False

        self.setMouseTracking(True)
        self.setObjectName("cell_plain")
        self.setCheckable(False)

    def getPiece(self) -> Optional[chess.Piece]:
        return self._piece

    def isPiece(self) -> bool:
        """ Indicates the type of the cell.
        It is True if the cell is a chess piece
        and False if it is an empty cell.
        """
        return self._piece is not None

    def setPiece(self, piece: Optional[chess.Piece]) -> None:
        """ Sets the content of the cell.

        Parameters
        ----------
        piece : Optional[chess.Piece]
            The piece that will occupy this cell.

            The cell is emptied if the piece is None otherwise its
            object name is set to ``cell_`` + the name of the piece or ``plain``.
            For example the object name of an empty cell will be ``cell_plain`` and
            the object name of a cell occupied by a white pawn will be ``cell_white_pawn``

            Cells containing a piece are checkable, whereas those empty ones are not.
        """

        self._piece = piece

        if self._piece:
            self.setObjectName(
                f"cell_{chess.COLOR_NAMES[piece.color]}_{chess.PIECE_NAMES[piece.piece_type]}")
            self.setCheckable(True)
        else:
            self.setObjectName("cell_plain")
            self.setCheckable(False)

        self.style().unpolish(self)
        self.style().polish(self)

    def isPlain(self) -> bool:
        """ A convenience property indicating if the cell is empty or not. """
        return not self._piece

    def toPlain(self) -> None:
        """ Empties the cell. """
        self.setPiece(None)

    @staticmethod
    def makePiece(piece: chess.Piece) -> "CellWidget":
        """ A static method that creates a `CellWidget` from the given piece.

        Parameters
        ----------
        piece : `chess.Piece`
            The piece that will occupy the cell. Note that the type of
            the piece cannot be NoneType as in the definition of the
            method `setPiece`, because by default cells are created empty.
         """

        assert isinstance(piece, chess.Piece)

        w = CellWidget()
        w.setPiece(piece)
        return w

    def isInCheck(self) -> bool:
        """ Indicates if the cell contains a king in check.

        Warnings
        --------
        Cells that aren't occupied by a king cannot be in check.

        Raises
        -------
        `NotAKingError`
            It is raised when the property is set to True for
            a cell not being occupied by a king.
        """
        return self._isInCheck

    def setInCheck(self, ck: bool) -> None:
        if self._piece and self._piece.piece_type == chess.KING:
            self._isInCheck = ck
            self.style().unpolish(self)
            self.style().polish(self)
        else:
            raise NotAKingError("Trying to (un)check a cell that does not hold a king.")

    def check(self) -> None:
        """ A convenience method that sets the property `isInCheck` to True. """
        self.setInCheck(True)

    def uncheck(self) -> None:
        """ A convenience method that sets the property `isInCheck` to False. """
        self.setInCheck(False)

    def isHighlighted(self) -> bool:
        """ Indicates if the cell is highlighted.
        Highlighted cells are special cells that are used to indicate
        legal moves on the board.
        Highlighted cells are not checkable.
        """
        return self._isHighlighted

    def setHighlighted(self, highlighted: bool) -> None:
        if self._isHighlighted != highlighted:
            self._isHighlighted = highlighted

            if self._isHighlighted:
                self.setCheckable(False)
            else:
                self.setCheckable(bool(self._piece))
            self.style().unpolish(self)
            self.style().polish(self)

    def highlight(self) -> None:
        """ A convenience method that sets the property `highlighted` to True. """
        self.setHighlighted(True)

    def unhighlight(self) -> None:
        """ A convenience method that sets the property `highlighted` to False. """
        self.setHighlighted(False)

    def isMarked(self) -> bool:
        """ Indicates if a cell is marked.
        Marked cells can have a different stylesheet which will visually distinguish
        them from other cells.
        The `designated` signal is emitted when this property's setter is called.
        """
        return self._isMarked

    def setMarked(self, marked: bool) -> None:
        self._isMarked = marked
        self.designated.emit(self._isMarked)
        self.style().unpolish(self)
        self.style().polish(self)

    def mark(self):
        """ A convenience method that sets the property `marked` to True. """
        self.setMarked(True)

    def unmark(self):
        """ A convenience method that sets the property `marked` to False. """
        self.setMarked(False)

    def justMoved(self) -> bool:
        """ Indicates if the piece occupying this cell was just moved from/to this
        cell. """
        return self._justMoved

    def setJustMoved(self, jm: bool):
        self._justMoved = jm
        self.style().unpolish(self)
        self.style().polish(self)

    def mouseMoveEvent(self, e):
        e.ignore()

    piece = QtCore.Property(bool, isPiece, setPiece)
    plain = QtCore.Property(bool, isPlain)
    inCheck = QtCore.Property(bool, isInCheck, setInCheck)
    highlighted = QtCore.Property(bool, isHighlighted, setHighlighted)
    marked = QtCore.Property(bool, isMarked, setMarked, notify=designated)
    justMoved = QtCore.Property(bool, justMoved, setJustMoved)


class AccessibleSides(Enum):
    NONE = 0
    ONLY_WHITE = 1
    ONLY_BLACK = 2
    BOTH = 3


NO_SIDE = AccessibleSides.NONE
ONLY_WHITE_SIDE = AccessibleSides.ONLY_WHITE
ONLY_BLACK_SIDE = AccessibleSides.ONLY_BLACK
BOTH_SIDES = AccessibleSides.BOTH


class EngineWrapper:
    """ This class is a wrapper around `engine`.
    The class is used to ease interactions with the engine and simplifies debugging.
    An `EngineWrapper` with no engine is called a null `EngineWrapper`.

    Attributes
    ----------
    engine : Optional[`chess.engine.UciProtocol`]
        Represents the engine. By default there is no engine, thus, the engine is None.
    """

    def __init__(self):
        self.engine: Optional[chess.engine.UciProtocol] = None

    def null(self) -> bool:
        """ Identifies if the wrapper has an engine. """
        return self.engine is None

    def start(self, path: str, options: dict = {}) -> bool:
        """ Starts an engine on the given path and configures it with the given options.

        Warnings
        --------
        Before starting a new engine, quit the current one.
        It is not possible to start an engine when there is another running, in other words, when
        the wrapper is not null. The caller will be warned about it if  this function is called when
        the wrapper is not null. The caller will also be informed if the engine was successfully
        started.

        Returns
        -------
        bool
            Returns True if the engine was started successfully, and False if not.
        """
        if not self.null():
            logging.warning("Cannot start a new engine, as there is another running.")
            return False

        async def main():
            transport, self.engine = await chess.engine.popen_uci(path)
            logging.info(f"Engine at {path} successfully started.")

            await self.engine.configure(options)

        asyncio.get_event_loop().run_until_complete(main())
        return True

    def playMove(self, board: chess.Board, limit: chess.engine.Limit, ponder: bool) -> Coroutine[Any, Any, chess.engine.PlayResult]:
        """ Finds the best move on the `board`. Returns a coroutine. """
        return asyncio.get_event_loop().run_until_complete(self.engine.play(board=board, limit=limit, ponder=ponder))

    def quit(self) -> bool:
        """ Quits the curent running engine.

        Warnings
        --------
        This function should be called when there is a running engine. Otherwise the caller will be warned
        about it.

        Returns
        -------
        True if the engine was quit successfully and False if not.
        """

        if self.null():
            logging.warning("No engine is running.")
            return False

        asyncio.get_event_loop().run_until_complete(self.engine.quit())
        self.engine = None

        return True


class _PromotionDialog(QtWidgets.QDialog):
    OptionOrder = bool
    QUEEN_ON_BOTTOM, QUEEN_ON_TOP = [True, False]

    def __init__(self, parent=None, color: bool = chess.WHITE,
                 order: OptionOrder = QUEEN_ON_TOP):
        super().__init__(parent)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        self.chosenPiece = chess.QUEEN

        def makePiece(pieceType):
            w = CellWidget.makePiece(chess.Piece(pieceType, color))
            w.setFocusPolicy(QtCore.Qt.NoFocus)
            w.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                            QtWidgets.QSizePolicy.MinimumExpanding)
            w.clicked.connect(partial(self.onPieceChosen, pieceType))
            return w

        layout = QtWidgets.QVBoxLayout()
        options = [chess.QUEEN, chess.KNIGHT, chess.ROOK, chess.BISHOP]

        if order == self.QUEEN_ON_TOP:
            [layout.addWidget(makePiece(option))
             for option in options]
        else:
            [layout.addWidget(makePiece(option))
             for option in options[::-1]]

        self.setLayout(layout)

    @QtCore.Slot()
    def onPieceChosen(self, pieceType):
        self.chosenPiece = pieceType
        self.accept()


class _DragWidget(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(_DragWidget, self).__init__(parent)

    def event(self, e: QtCore.QEvent) -> bool:
        if e.type() == QtGui.QMouseEvent:
            e.ignore()
            return False
        return super(_DragWidget, self).event(e)


def _DefaultPredicate(w: CellWidget) -> bool:
    return True


class BoardWidget(QtWidgets.QLabel):
    """ Represents a customizable graphical chess board.
    It inherits `QtWidgets.QLabel` and has a `QtWidgets.QGridLayout` with 64
    `CellWidget` instances that can be moved. It also supports all the
    chess rules, drag and drop and chess engines.

    Attributes
    ----------
    board : `chess.Board`
        Represents the actual board. Moves and their validation are
        conducted through this object.

    popStack : Deque[`chess.Move`]
        The moves that are popped from the `board.move_stack` through the functions
        `goToMove`, `pop` are stored in this deque.

    blockBoardOnPop : bool
        If this attribute is True, the board can't be interacted with unless `popStack`
        is empty.

    defaultPixmap : `QtGui.QPixmap`
        The pixmap that the board will have when the property `flipped` is False.

    flippedPixmap : `QtGui.QPixmap`
        The pixmap that the board will have when the property `flipped` is True.

    lastCheckedCellWidget : Optional[`CellWidget`]
        Holds the last CellWidget that was checked through
        `QtWidgets.QPushButton.setChecked(True)`.
        Its value is None in case no CellWidget has been checked.

    dragAndDrop : bool
        This is used to enable or disable drag and drop.
        When it is True, cell widgets can be dragged, by pressing on them
        with the mouse left button and moving the mouse cursor. They
        can be dropped by releasing the mouse left button during the drag. Whereever
        the cell is dropped, the board acts as if the same point were clicked with
        the mouse.

    engineWrapper : `EngineWrapper`
        This attribute is used to start an engine and find the best moves on the board.
    """

    moveMade = QtCore.Signal(str)
    """ Indicates that a move on the board has been made either with `BoardWidget.makeMove`
    or any other function that calls makes a move on `board` (e.g `chess.Board.push`). The signal accepts the move in
    form of `str` as a parameter. Particularly, the library always emits the signal with the move in form of san as a
    parameter. If it is a `checkmate`, a `draw` or a `stalemate` the respective signal is emitted together with `gameOver`.
    """
    movePushed = QtCore.Signal(str)
    """ This is nearly the same as `moveMade`, with the exception that it's emit only by those functions that
    contain the word 'push' in the name.
    """
    checkmate = QtCore.Signal(bool)
    """ This is emitted when it is checkmate on the board. It accepts the color of the winning side as a parameter.
    """
    draw = QtCore.Signal()
    """ This is emitted when it is drag on the board. """
    stalemate = QtCore.Signal()
    """ This is emitted when it is stalemate on the board. """
    gameOver = QtCore.Signal()
    """ This is emitted when the game is over. """

    def __init__(self, parent=None,
                 fen: Optional[str] = chess.STARTING_FEN,
                 flipped: bool = False,
                 sides: AccessibleSides = NO_SIDE,
                 dnd: bool = False):
        super().__init__(parent=parent)

        self.board = chess.Board(fen)
        self.popStack = deque()

        self._flipped = flipped
        self._accessibleSides = sides

        self.blockBoardOnPop = False

        self.defaultPixmap = self.pixmap()
        self.flippedPixmap = QtGui.QPixmap(self.pixmap())
        self.lastCheckedCellWidget = None

        self.dragAndDrop = dnd
        self._dragWidget: Optional[QtWidgets.QWidget] = None

        self.engineWrapper = EngineWrapper()

        self._boardLayout = QtWidgets.QGridLayout()
        self._boardLayout.setContentsMargins(0, 0, 0, 0)
        self._boardLayout.setSpacing(0)

        def newCellWidget():
            cellWidget = CellWidget()
            cellWidget.setFocusPolicy(QtCore.Qt.NoFocus)
            cellWidget.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                     QtWidgets.QSizePolicy.MinimumExpanding)

            cellWidget.clicked.connect(partial(self._onCellWidgetClicked, cellWidget))
            cellWidget.toggled.connect(partial(self._onCellWidgetToggled, cellWidget))
            cellWidget.designated.connect(self._onCellWidgetMarked)
            cellWidget.installEventFilter(self)
            return cellWidget

        for i in range(8):
            for j in range(8):
                self._boardLayout.addWidget(newCellWidget(), i, j)
        self.setLayout(self._boardLayout)

        self.setFen(self.board.fen())

        self.moveMade.connect(self._onMoveMade)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        self.setScaledContents(True)

    def eventFilter(self, watched, event: QtGui.QMouseEvent) -> bool:
        if isinstance(watched, CellWidget):
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.buttons() == QtCore.Qt.LeftButton:
                    # start drag if it is possible
                    if self.dragAndDrop and watched.getPiece() \
                            and watched.getPiece().color == self.board.turn:
                        self._dragWidget = _DragWidget(self)
                        self._dragWidget.setAutoFillBackground(True)
                        self._dragWidget.setFixedSize(watched.size())
                        self._dragWidget.setScaledContents(True)
                        self._dragWidget.setStyleSheet("background: transparent;")
                        self._dragWidget.setPixmap(QtGui.QPixmap(
                            f":/images/{'_'.join(watched.objectName().split('_')[1:])}.png"))

                        rect = self._dragWidget.geometry()
                        rect.moveCenter(QtGui.QCursor.pos())
                        self._dragWidget.setGeometry(rect)

                        watched.setChecked(not watched.isChecked())
                        return True

                elif event.buttons() == QtCore.Qt.RightButton:
                    # mark cell if it is possible
                    if self.accessibleSides != NO_SIDE:
                        watched.setMarked(not watched.marked)

        return watched.event(event)

    def mousePressEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton and self._dragWidget:
            self._dragWidget.deleteLater()
            self._dragWidget = None
            self.foreachCells(CellWidget.unhighlight, CellWidget.unmark,
                              lambda w: w.setChecked(False))

    def mouseMoveEvent(self, e):
        if self._dragWidget:
            # if drag has started, show the drag widget if it is not visible
            # and move its center to the mouse cursor.
            if not self._dragWidget.isVisible():
                self._dragWidget.show()
            rect = self._dragWidget.geometry()
            rect.moveCenter(e.pos())
            self._dragWidget.setGeometry(rect)
        super(BoardWidget, self).mouseMoveEvent(e)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # end drag and drop
            if self._dragWidget:
                self._dragWidget.deleteLater()
                self._dragWidget = None

                for w in self.cellWidgets(lambda w: w.geometry().contains(self.mapFromGlobal(event.globalPos()))):
                    self._onCellWidgetClicked(w)

    def cellWidgets(self, predicate: Callable[[CellWidget], bool] = _DefaultPredicate) -> \
            Generator[CellWidget, None, None]:
        """
        Yields
        ------
        Generator[`CellWidget`, None, None]
            All the cell widgets in the board's layout
            that fulfill the predicate's condition.
        """

        for i in range(self._boardLayout.count()):
            w = self._boardLayout.itemAt(i).widget()
            if predicate(w):
                yield w

    def foreachCells(self, *args: Callable[[CellWidget], Any],
                     predicate: Callable[[CellWidget], bool] = _DefaultPredicate):
        """ Iterates over all the cell widgets that fulfill the condition of `predicate`
        and calls the callbacks passed through *args one by one in the given order.

        Parameters
        ----------
        *args : Callable[[`CellWidget`], Any]
            The callbacks that will be called on the cell widgets.
        predicate : Callable[[`CellWidget`], bool]
        """

        for w in self.cellWidgets():
            if predicate(w):
                for callback in args:
                    callback(w)

    def cellIndexOfSquare(self, square: chess.Square) -> Optional[chess.Square]:
        """
        Returns
        -------
        Optional[`chess.Square`]
            The index of the widget at the given square number if we started counting from the top left
            corner of the board.
        """

        if not self._flipped:
            return chess.square_mirror(square)
        return chess.square(7 - chess.square_file(square), chess.square_rank(square))

    def squareOf(self, w: CellWidget) -> chess.Square:
        """
        Returns
        -------
        chess.Square
            The square number corresponding to the given cell widget.
        """

        i = self._boardLayout.indexOf(w)
        if not self.flipped:
            return chess.square_mirror(i)
        return chess.square(7 - chess.square_file(i), chess.square_rank(i))

    def cellWidgetAtSquare(self, square: chess.Square) -> Optional[CellWidget]:
        """
        Returns
        -------
        Optional[`CellWidget`]
            The cell widget at the given square if there is one, otherwise
            it returns None.
        """

        item = self._boardLayout.itemAt(self.cellIndexOfSquare(square))
        if item is not None:
            return item.widget()
        return None

    def pieceCanBePushedTo(self, w: CellWidget):
        """ Yields the numbers of squares that the piece on the cell widget can be legally pushed
        to. """

        for move in self.board.legal_moves:
            if move.from_square == self.squareOf(w):
                yield move.to_square

    def isPseudoLegalPromotion(self, move: chess.Move) -> bool:
        """ This method indicates if the given move can be a promotion. So would be if the piece
        being moved were a pawn, and if it were being moved to the corresponding end of the board.

        Warnings
        --------
        The result of this method is pseudo-true, as it doesn't do any move validation. It is the
        caller's responsibility to validate the move.
        """

        piece = self.board.piece_at(move.from_square)

        if piece is not None and piece.piece_type == chess.PAWN:
            if piece.color == chess.WHITE:
                return chess.A8 <= move.to_square <= chess.H8
            elif piece.color == chess.BLACK:
                return chess.A1 <= move.to_square <= chess.H1
        return False

    def king(self, color: chess.Color) -> Optional[CellWidget]:
        """
        Returns
        -------
        Optional[`CellWidget`]
            The cell widget that holds the king of the given color or None if there is no
            king.
        """

        kingSquare = self.board.king(color)
        if kingSquare is not None:
            return self.cellWidgetAtSquare(kingSquare)
        return None

    def setBoardPixmap(self, defaultPixmap, flippedPixmap) -> None:
        """ Sets the default and flipped pixmaps and updates the board's pixmap
        according to them.
        """

        self.defaultPixmap = defaultPixmap
        self.flippedPixmap = flippedPixmap
        self._updatePixmap()

    def setPieceAt(self, square: chess.Square, piece: chess.Piece) -> CellWidget:
        """ Sets the given piece at the given square of the board.

        Returns
        -------
        CellWidget
            The cell widget where the piece was set.
        """
        return self._setPieceAt(square, piece)

    def removePieceAt(self, square: chess.Square) -> CellWidget:
        """ Removes the piece from the given square of the board.
        The cell at the given square is turned into a plain cell.

        Raises
        ------
        ValueError
            If the cell at the given square does not hold a chess piece.

        Returns
        -------
        CellWidget
            The cell widget at the given square.
        """

        w = self.cellWidgetAtSquare(square)

        if w.isPlain():
            raise ValueError(f"Cell widget at {square} is not a piece")

        self.board.remove_piece_at(square)
        w.toPlain()

        return w

    def addPieceAt(self, square: chess.Square, piece: chess.Piece) -> CellWidget:
        """ This method is the safer version of `setPieceAt`.

        Raises
        ------
        ValueError
            If the given square is already occupied.

        Returns
        -------
        CellWidget
            The created cell widget.
        """

        if self.board.piece_at(square) is not None:
            raise ValueError("Square {} is occupied")
        return self._setPieceAt(square, piece)

    def synchronize(self) -> None:
        """ Synchronizes the widget with the contents of `board`.
        This method makes all the cells plain and then sets their pieces on by one.
        """
        self._synchronize()

    def synchronizeAndUpdateStyles(self) -> None:
        """ Synchronizes the widget with the contents of `board` and updates
        the just moved cells and the king in check.
        """

        self._synchronize()

        self._updateJustMovedCells(False)
        self._updateJustMovedCells(True)

        if self.board.is_check():
            self.king(self.board.turn).check()
        else:
            self.king(self.board.turn).uncheck()
            self.king(not self.board.turn).uncheck()

    def setPieceMap(self, pieces: Mapping[int, chess.Piece]) -> None:
        """ Sets the board's piece map and synchronizes the board widget.
        The highlighted cells are also unhighlighted, because the positions of
        the pieces change after the change of piece map.
        """

        self.board.set_piece_map(pieces)
        self.unhighlightCells()
        self.synchronize()

    def setFen(self, fen: Optional[str]) -> None:
        """ Sets the board's fen and synchronizes the board widget.
        The highlighted cells are also unhighlighted, because the positions of
        the pieces change after the fen.
        """

        self.board = chess.Board(fen)
        self.unhighlightCells()
        self.synchronize()

    def clear(self) -> None:
        """ Clears the board widget and resets the properties of the cells. """

        self._updateJustMovedCells(False)

        self.king(chess.WHITE).uncheck()
        self.king(chess.BLACK).uncheck()

        self.board.clear()
        self.popStack.clear()
        self.foreachCells(CellWidget.unhighlight, CellWidget.unmark, lambda w: w.setChecked(False))
        self.synchronize()

    def reset(self) -> None:
        """ Resets the pieces to their standard positions and resets the
        properties of the board widget and all the pieces inside of its layout.
        """

        self._updateJustMovedCells(False)

        self.king(chess.WHITE).uncheck()
        self.king(chess.BLACK).uncheck()

        self._flipped = False
        self._updatePixmap()

        self.board.reset()
        self.popStack.clear()
        self.foreachCells(CellWidget.unhighlight, CellWidget.unmark,
                          lambda w: w.setChecked(False))
        self.synchronize()

    def makeMove(self, move: chess.Move) -> None:
        """ Makes a move without move validation.
        The move, though, should be pseudo-legal. Otherwise `chess.Board.push`
        will raise an exception. Can be useful when you don't need a promotion dialog
        or notifications about the game state. Emits moveMade signal, with move's san as
        parameter.
        """

        self._updateJustMovedCells(False)
        san = self.board.san(move)
        self.board.push(move)
        self._updateJustMovedCells(True)
        self.synchronizeAndUpdateStyles()
        self.moveMade.emit(san)

    def pushPiece(self, toSquare: chess.Square, w: CellWidget) -> None:
        """ Pushes the piece on the given cell widget to the given square.
        If there is a promotion a dialog will appear with 4 pieces to choose.
        Emits moveMade and movePushed signals, with move's san as parameter.
        If the it is a draw/stalemate/checkmate the corresponding signal will be
        emitted.

        Raises
        ------
        IllegalMove
            If the move is illegal.
        """
        self._push(chess.Move(self.squareOf(w), toSquare))

    def push(self, move: chess.Move) -> None:
        """ Pushes the given move.
        For further reference see `pushPiece`.

        Raises
        ------
        IllegalMove
            If the move is illegal or null.
        """
        self._push(move)

    def pop(self, n=1) -> str:
        """ Pops the move `n` times.
        Removes `marked` and `highlighted` properties from cells.
        Updates just moved properties.

        Returns
        --------
        str
            Last poped move in form of uci.
        """

        self._updateJustMovedCells(False)
        lastMove = None
        for i in range(n):
            lastMove = self.board.pop()
            self.popStack.append(lastMove)

        self.foreachCells(CellWidget.unmark, CellWidget.unhighlight)
        self.synchronizeAndUpdateStyles()

        return lastMove.uci()

    def unpop(self, n=1) -> str:
        """ Unpops moves `n` times.
        This method works in the same way as `pop`.
        For further reference see the latter's documentation.
        """

        self._updateJustMovedCells(False)

        lastMove = None
        for i in range(n):
            lastMove = self.popStack.pop()
            self.board.push(lastMove)

        self.foreachCells(CellWidget.unmark, CellWidget.unhighlight)
        self.synchronizeAndUpdateStyles()

        return lastMove.uci()

    def goToMove(self, n: int) -> bool:
        """ Goes to the move with the given `id`.

        Returns
        -------
        bool
            True if a move with the given `id` exists. Otherwise returns False.
        """

        if n >= 0:
            moveStackLen = len(self.board.move_stack)
            if n <= (moveStackLen + len(self.popStack)):
                if moveStackLen < n:
                    self.unpop(n - moveStackLen)
                    return True
                if moveStackLen > n:
                    self.pop(moveStackLen - n)
                    return True
        return False

    def highlightLegalMoveCellsFor(self, w: CellWidget) -> int:
        """ Highlights the legal moves for the given cell widget.

        Returns
        -------
        int
            The number of highlighted cells as a result of this method's call.
        """

        counter = 0
        for square in self.pieceCanBePushedTo(w):
            self.cellWidgetAtSquare(square).highlight()
            counter += 1
        return counter

    def uncheckCells(self, exceptFor: Optional[CellWidget] = None) -> None:
        """ Calls QtWidgets.QPushButton.setChecked(False) for all the cells except for the
        specified one. If you want to set checked to False for all the cells, then pass None as
        an argument to this method instead.
        """

        def callback(w: CellWidget):
            if w != exceptFor:
                w.setChecked(False)

        self.foreachCells(callback)

    def unhighlightCells(self) -> None:
        """ Calls `CellWidget.unhighlight` for each cell. """
        self.foreachCells(CellWidget.unhighlight)

    def unmarkCells(self) -> None:
        """ Calls `CellWidget.unmark` for each cell. """
        self.foreachCells(CellWidget.unmark)

    @property
    def flipped(self) -> bool:
        """ Indicates if the board is flipped.
        If its value is changed, the board pixmap and piece positions
        change in a way as if the board were flipped. """
        return self._flipped

    @flipped.setter
    def flipped(self, flipped: bool) -> None:
        self._setFlipped(flipped)

    def flip(self) -> None:
        """ A convenience method that sets the property `flipped` to True. """
        self._setFlipped(not self.flipped)

    @property
    def accessibleSides(self) -> AccessibleSides:
        """ Indicates pieces of which color
        can be interacted with.
        """
        return self._accessibleSides

    @accessibleSides.setter
    def accessibleSides(self, accessibleSides: AccessibleSides) -> None:
        self._accessibleSides = accessibleSides
        self.foreachCells(CellWidget.unhighlight, CellWidget.unmark, lambda w: w.setChecked(False))
        self.synchronize()

    @QtCore.Slot()
    def _onMoveMade(self):
        if self.board.is_checkmate():
            self.checkmate.emit(not self.board.turn)
            self.gameOver.emit()
        elif self.board.is_insufficient_material():
            self.draw.emit()
            self.gameOver.emit()
        elif self.board.is_stalemate():
            self.stalemate.emit()
            self.gameOver.emit()

    @QtCore.Slot()
    def _onCellWidgetClicked(self, w):
        if w.highlighted:
            self.pushPiece(self.squareOf(w), self.lastCheckedCellWidget)
            self.unmarkCells()
        elif not w.piece:
            self.foreachCells(CellWidget.unhighlight, CellWidget.unmark,
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

            def callback(_w: CellWidget):
                if _w != w:
                    _w.setChecked(False)

            self.foreachCells(CellWidget.unmark, CellWidget.unhighlight, callback)
            if not self.highlightLegalMoveCellsFor(w):
                w.setChecked(False)
            self.lastCheckedCellWidget = w
        else:
            self.unhighlightCells()

    @QtCore.Slot()
    def _onCellWidgetMarked(self, marked: bool):
        if marked:
            def callback(w):
                if w.isChecked():
                    w.setChecked(False)

            self.foreachCells(callback, CellWidget.unhighlight)

    def _isCellAccessible(self, w):
        if self.accessibleSides == NO_SIDE:
            return False
        if self.accessibleSides == BOTH_SIDES:
            return True

        if w.piece:
            color = w.getPiece().color

            if color == chess.WHITE:
                return self.accessibleSides == ONLY_WHITE_SIDE
            if color == chess.BLACK:
                return self.accessibleSides == ONLY_BLACK_SIDE

    def _setPieceAt(self, square: chess.Square, piece: chess.Piece) -> CellWidget:
        self.board.set_piece_at(square, piece)

        w = self.cellWidgetAtSquare(square)
        w.setPiece(piece)

        return w

    def _updatePixmap(self) -> None:
        if not self._flipped:
            if self.defaultPixmap:
                self.setPixmap(self.defaultPixmap.scaled(self.size(),
                               QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        elif self.flippedPixmap:
            self.setPixmap(self.flippedPixmap.scaled(self.size(),
                           QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def _synchronize(self) -> None:
        def callback(w):
            w.unhighlight()
            if not w.isPlain():
                w.toPlain()

        boardCopy = self.board.copy()
        self.foreachCells(callback)
        for square, piece in self.board.piece_map().items():
            self._setPieceAt(square, piece)
        self.board = boardCopy

    def _updateJustMovedCells(self, justMoved: bool):
        if self.board.move_stack:
            lastMove = self.board.move_stack[-1]
            self.cellWidgetAtSquare(lastMove.from_square).justMoved = justMoved
            self.cellWidgetAtSquare(lastMove.to_square).justMoved = justMoved

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
        logging.debug(f"\n{self.board.lan(move)} ({move.from_square} -> {move.to_square})")

        san = self.board.san(move)
        self.board.push(move)
        logging.debug(f"\n{self.board}\n")

        self._updateJustMovedCells(True)
        self.popStack.clear()

        self.foreachCells(CellWidget.unmark, CellWidget.unhighlight)
        self.synchronizeAndUpdateStyles()

        self.moveMade.emit(san)
        self.movePushed.emit(san)

    def _setFlipped(self, flipped: bool):
        if self._flipped != flipped:
            self._updateJustMovedCells(False)

            markedWidgets = list(self.cellWidgets(CellWidget.isMarked))
            for w in markedWidgets:
                w.unmark()
                self.cellWidgetAtSquare(63 - self.squareOf(w)).mark()

            self._flipped = flipped
            self.synchronizeAndUpdateStyles()
            self._updatePixmap()
