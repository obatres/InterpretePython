from PyQt5.QtGui import *
from PyQt5.QtGui import QColor, QSyntaxHighlighter, QTextFormat, QColor, QTextCharFormat, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import copy
import os
import sys
import uuid

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
IMAGE_EXTENSIONS = ['.jpg','.png','.bmp']
HTML_EXTENSIONS = ['.htm', '.html']


def format(colorizar):
    color_letra = QColor()

    HighLight_texto = QTextCharFormat()

    color_letra.setNamedColor(colorizar)

    HighLight_texto.setForeground(color_letra)

    return HighLight_texto

def hexuuid():
    return uuid.uuid4().hex

def splitext(p):
    return os.path.splitext(p)[1].lower()

class Resaltado(QSyntaxHighlighter):
    
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
    
        patrones = []

        patrones += [
                (r'\d+(\.\d+)?',0, format('darkBlue')), 
                (r'[a-zA-Z_][a-zA-Z_0-9]*',0, format('darkRed')),
                ('if',0,format('darkMagenta')),
                ('else' ,0,format('darkMagenta')),
                ('main',0,format('darkMagenta')),
                ('goto',0,format('darkMagenta')),
                ('unset',0,format('darkMagenta')),
                ('print',0,format('darkMagenta')),
                ('read',0,format('darkMagenta')),
                ('exit',0,format('darkMagenta')),
                ('int',0,format('darkMagenta')),
                ('float',0,format('darkMagenta')),
                ('char',0,format('darkMagenta')),
                ('array',0,format('darkMagenta')),
                ('abs',0,format('darkMagenta')),
                ('xor',0,format('darkMagenta')),

                (r'!',0,format('darkGray')),
                (r'&&',0,format('darkGray')),
                (r'\|\|',0,format('darkGray')),
                (r'~',0,format('darkGray')),
                (r'&',0,format('darkGray')),
                (r'\|',0,format('darkGray')),
                ( r'\^',0,format('darkGray')),
                ( r'<<',0,format('darkGray')),
                ( r'>>',0,format('darkGray')),
                ( r'\$(t[0-9]+)',0,format('darkCyan')),
                ( r'\&\$(t[0-9]+)',0,format('darkCyan')),
                ( r'\$[a][0-9]+',0,format('darkCyan')),
                ( r'\$[v][0-9]+',0,format('darkCyan')),
                ( r'\$[r][a]',0,format('darkCyan')),
                ( r'\$[s][0-9]+',0,format('darkCyan')),             
                ( r'\$[s][p]',0,format('darkCyan')),  
                ( r'[r][0-9]+',0,format('darkCyan')),  
                ( r'\'.*?\'',0,format('darkYellow')), 
                ( r'\".*?\"',0,format('darkYellow')),

                (r'\#.*\n',0,format('darkGreen')),
            ]

        self.patrones = [(QRegExp(patron), indice,estilo)
            for (patron, indice, estilo) in patrones]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for exp, pos, estilo in self.patrones:
            i = exp.indexIn(text, 0)
            while i >= 0:

                i = exp.pos(pos)
                length = len(exp.cap(pos))
                self.setFormat(i, length, estilo)
                i = exp.indexIn(text, i + length)

        self.setCurrentBlockState(0)

class TextEdit(QTextEdit):

    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():

            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())

                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break

            else:
                # If all were valid images, finish here.
                return


        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return

        super(TextEdit, self).insertFromMimeData(source)

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class PlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()

        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.i = 0
        layout = QVBoxLayout()
        self.editor = PlainTextEdit()
        self.consola = QPlainTextEdit()

        self.consola.setReadOnly(True)
        self.entrada = ''
        # Setup the QTextEdit editor configuration
        
        #self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)
        # Initialize default font size.
        font = QFont('Times', 10)
        self.editor.setFont(font)
        
        # We need to repeat the size to init the current format.
        #self.editor.setFontPointSize(12)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        
        
        
        #self.consola.setTextBackgroundColor("grey")

        layout.addWidget(self.editor)
        layout.addWidget(self.consola)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)
#File
        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")
#Open File
        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)
#Save File
        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        cut_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        cut_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        cut_action.setShortcut(QKeySequence.SelectAll)
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join('images', 'arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

#-----------------------------------------------------------------------------BOTON PARA EJECUTAR ANALISIS
        Ejec_toolbar = QToolBar("Ejecutar")
        Ejec_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(Ejec_toolbar)
        Ejecutar_menu = self.menuBar().addMenu("&Ejecutar")
        

        EjecutarPLY = QAction(QIcon(os.path.join('images', 'application-run.png')), "Ascendente", self)  
        EjecutarPLY.setStatusTip("Ejecutar Asc")
        EjecutarPLY.triggered.connect(self.EjecutarAsc)  
        
        Ejecutar_menu.addAction(EjecutarPLY)
        Ejec_toolbar.addAction(EjecutarPLY)

        #self.toolbar.addAction(EjecutarPLY)

        EjecutarDesc = QAction(QIcon(os.path.join('images', 'Run.png')), "Descendente", self)  
        EjecutarDesc.setStatusTip("Ejecutar Desc")
        EjecutarDesc.triggered.connect(self.EjecutarDesc)  
        Ejecutar_menu.addAction(EjecutarDesc)
        Ejec_toolbar.addAction(EjecutarDesc)

        EjecutarDeb = QAction(QIcon(os.path.join('images', 'debug.png')), "Debug", self)  
        EjecutarDeb.setStatusTip("Ejecutar Debug")
        EjecutarDeb.triggered.connect(self.EjecutarDeb)  
        Ejecutar_menu.addAction(EjecutarDeb)
        Ejec_toolbar.addAction(EjecutarDeb)

#-----------------------------------------------------------------------------BOTON FORMATO
        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(format_toolbar)
        format_menu = self.menuBar().addMenu("&Format")

        # We need references to these actions/settings to update as selection changes, so attach to self.
        self.fonts = QFontComboBox()
        #self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        format_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in FONT_SIZES])

        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        self.fontsize.currentIndexChanged[str].connect(lambda s: self.editor.setFontPointSize(float(s)) )
        format_toolbar.addWidget(self.fontsize)

        self.bold_action = QAction(QIcon(os.path.join('images', 'edit-bold.png')), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(self.bold_action)
        format_menu.addAction(self.bold_action)

        self.italic_action = QAction(QIcon(os.path.join('images', 'edit-italic.png')), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        #self.italic_action.toggled.connect(self.editor.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        format_menu.addAction(self.italic_action)

        self.underline_action = QAction(QIcon(os.path.join('images', 'edit-underline.png')), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        #self.underline_action.toggled.connect(self.editor.setFontUnderline)
        format_toolbar.addAction(self.underline_action)
        format_menu.addAction(self.underline_action)

        format_menu.addSeparator()

        self.alignl_action = QAction(QIcon(os.path.join('images', 'edit-alignment.png')), "Align left", self)
        self.alignl_action.setStatusTip("Align text left")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        format_toolbar.addAction(self.alignl_action)
        format_menu.addAction(self.alignl_action)

        self.alignc_action = QAction(QIcon(os.path.join('images', 'edit-alignment-center.png')), "Align center", self)
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        format_toolbar.addAction(self.alignc_action)
        format_menu.addAction(self.alignc_action)

        self.alignr_action = QAction(QIcon(os.path.join('images', 'edit-alignment-right.png')), "Align right", self)
        self.alignr_action.setStatusTip("Align text right")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        format_toolbar.addAction(self.alignr_action)
        format_menu.addAction(self.alignr_action)

        self.alignj_action = QAction(QIcon(os.path.join('images', 'edit-alignment-justify.png')), "Justify", self)
        self.alignj_action.setStatusTip("Justify text")
        self.alignj_action.setCheckable(True)
        self.alignj_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        format_toolbar.addAction(self.alignj_action)
        format_menu.addAction(self.alignj_action)

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.alignl_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.alignr_action)
        format_group.addAction(self.alignj_action)

        format_menu.addSeparator()

# A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self._format_actions = [
            self.fonts,
            self.fontsize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]

        # Initialize.
        self.update_format()
        self.update_title()
        self.show()

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)

        #self.fonts.setCurrentFont(self.editor.currentFont())
        # Nasty, but we get the font-size as a float but want it was an int
        #self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))

        #self.italic_action.setChecked(self.editor.fontItalic())
        #self.underline_action.setChecked(self.editor.fontUnderline())
        #self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)

        #self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        #self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        #self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        #self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)

        self.block_signals(self._format_actions, False)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
    
    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")
        try:
            with open(path, 'rU') as f:
                text = f.read()
                self.entrada = text
                highlight = Resaltado(self.editor.document())
                highlight.highlightBlock(self.editor.toPlainText())
                self.editor.setPlainText(text)  

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            # Qt will automatically try and guess the format as txt/html
            #self.editor.setText(text)
            self.editor.setPlainText(text)
            self.update_title()

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        text = self.editor.toHtml() if splitext(self.path) in HTML_EXTENSIONS else self.editor.toPlainText()

        try:
            with open(self.path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        text = self.editor.toHtml() if splitext(path) in HTML_EXTENSIONS else self.editor.toPlainText()

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("AUGUS IDE")

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )
    
    def getInteger(self):
        text, ok = QInputDialog().getText(self, "QInputDialog().getText()",
                                     "User name:", QLineEdit.Normal,
                                     "Valor de variable:")
        if ok and text:
            return text

    def cerrar(self):
        self.close()
    
    def getTexto(self):
        return self.editor.toPlainText()

    def EjecutarAsc(self):
        import principal as f
        self.consola.clear()
        try:
            f.ejecutar_asc(self.editor.toPlainText())
            f.errores_asc()
            f.ReporteErrores()
            f.ReporteTS()
            f.ReporteGramatical()
            f.GenerarAST()
            s = f.RecibirSalida()
            self.consola.setPlainText(s)
        except:
            btn = QMessageBox.information(self, 'FIN',
                'no se puede realizar la ejecucion del ascendente',
                QMessageBox.Yes)
        return 

    def EjecutarDesc(self):
        import principal as j
        self.consola.clear()
        try:
            j.ejecutar_desc(self.editor.toPlainText())
            j.errores_desc()
            j.ReporteErrores()
            j.ReporteTS()
            j.ReporteGramatical()
            j.GenerarAST()
            s = j.RecibirSalida()
            self.consola.setPlainText(s)
        except:
            btn = QMessageBox.information(self, 'FIN',
                'no se puede realizar la ejecucion del descendente',
                QMessageBox.Yes)
    
    def EjecutarDeb(self):
        import principal as de 
        self.consola.clear()
        try:
            de.ejecutar_debug(self.editor.toPlainText(),self.i)
            de.ReporteTS()
            de.ReporteErrores()
            self.i =  self.i + 1
            s = de.RecibirSalida()
            self.consola.setPlainText(s)
        except :
            btn = QMessageBox.information(self, 'FIN',
                'no se puede realizar la ejecucion del debug',
                QMessageBox.Yes)
        
    def ReporteGramatical(self):
        import principal as l
        l.ReporteGramatical()

    def OkMessage(self):
        #buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you want to save?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        btn = QMessageBox.information(self, 'FIN',
                'Terminada la ejecucion del debug',
                QMessageBox.Yes)
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setApplicationName("AUGUS IDE")

    window = MainWindow()

    app.exec_()