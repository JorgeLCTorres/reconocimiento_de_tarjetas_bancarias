import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image

class ImageViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.image_path = ""
        self.rectangles = []

    def init_ui(self):
        self.setWindowTitle("Visor de Imágenes")
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        open_button = QPushButton("Abrir Imagen", self)
        open_button.clicked.connect(self.open_image)

        label_button = QPushButton("Etiquetar Nombre", self)
        label_button.clicked.connect(self.label_name)

        layout = QVBoxLayout()
        layout.addWidget(open_button)
        layout.addWidget(label_button)
        layout.addWidget(self.image_label)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Imagen", "", "Imágenes (*.png *.jpg *.bmp *.gif *.jpeg);;Todos los archivos (*)", options=options)

        if file_path:
            self.image_path = file_path
            self.rectangles = []
            self.show_image(file_path)

    def show_image(self, file_path):
        image = Image.open(file_path)
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def label_name(self):
        if self.image_path:
            label_dialog = LabelDialog(self.image_path, self.rectangles, self)
            if label_dialog.exec_():
                self.rectangles = label_dialog.get_rectangles()
                self.show_image(self.image_path)
        else:
            self.show_popup_message("Error", "Abre una imagen primero.")

    def show_popup_message(self, title, message):
        popup = QMessageBox(self)
        popup.setWindowTitle(title)
        popup.setText(message)
        popup.setIcon(QMessageBox.Information)
        popup.setStandardButtons(QMessageBox.Ok)
        popup.exec_()

class LabelDialog(QDialog):
    def __init__(self, image_path, rectangles, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.rectangles = rectangles
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Etiquetar Nombre del Titular")
        self.setGeometry(200, 200, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.rectangles_label = QLabel(self)
        self.rectangles_label.setAlignment(Qt.AlignCenter)

        self.save_button = QPushButton("Guardar Etiquetas", self)
        self.save_button.clicked.connect(self.save_rectangles)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.rectangles_label)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_image()

    def load_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
        self.draw_rectangles()

    def draw_rectangles(self):
        if self.rectangles:
            image = Image.open(self.image_path)
            painter = QPainter(image)
            pen = QPen(Qt.red, 2)
            painter.setPen(pen)

            for rect in self.rectangles:
                x, y, w, h = rect
                painter.drawRect(x, y, w, h)

            painter.end()

            image_qt = QImage(image.tobytes(), image.size[0], image.size[1], QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(image_qt)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def save_rectangles(self):
        self.accept()

    def get_rectangles(self):
        return self.rectangles

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewerApp()
    window.show()
    sys.exit(app.exec_())
