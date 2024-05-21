import sys
import qtawesome as qta
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QMessageBox

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Map Design Grid with Font Awesome Icons')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.gridLayout = QGridLayout()
        self.buttons = []
        self.selected_button = None

        # Create a 3x4 grid of buttons with useful Font Awesome icons and labels
        icon_label_pairs = [
            ('fa5s.home', 'Home'), ('fa5s.shopping-cart', 'Shop'), ('fa5s.hospital', 'Hospital'), ('fa5s.school', 'School'),
            ('fa5s.utensils', 'Restaurant'), ('fa5s.coffee', 'Cafe'), ('fa5s.bus', 'Bus Stop'), ('fa5s.tree', 'Park'),
            ('fa5s.building', 'Office'), ('fa5s.dumbbell', 'Gym'), ('fa5s.film', 'Cinema'), ('fa5s.book', 'Library')
        ]

        for i in range(3):
            for j in range(4):
                index = i * 4 + j
                icon, label = icon_label_pairs[index]
                icon = qta.icon(icon)
                button = QPushButton(icon, label)
                button.setCheckable(True)
                button.clicked.connect(self.button_clicked)
                self.gridLayout.addWidget(button, i, j)
                self.buttons.append(button)

        layout.addLayout(self.gridLayout)

        self.displayButton = QPushButton('Get Selected Items')
        self.displayButton.clicked.connect(self.get_selected_items)
        layout.addWidget(self.displayButton)

        self.setLayout(layout)

    def button_clicked(self):
        button = self.sender()
        if self.selected_button and self.selected_button != button:
            self.selected_button.setChecked(False)
            self.selected_button.setStyleSheet('')

        if button.isChecked():
            button.setStyleSheet('background-color: lightblue')
            self.selected_button = button
        else:
            button.setStyleSheet('')
            self.selected_button = None

    def get_selected_items(self):
        if not self.selected_button:
            QMessageBox.information(self, 'No Selection', 'No items selected')
        else:
            selected_text = self.selected_button.text()
            QMessageBox.information(self, 'Selected Item', selected_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())
