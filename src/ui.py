import io
from typing import Tuple

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
    QTextEdit,
    QGridLayout,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt
import qtawesome as qta

from src.utils import address_to_coordinate, current_location, get_details
from src.Marker import Marker
from src.settings import ICON_LABEL_PAIRS
from src.folium_map import foliumMap

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.latitute, self.longitude = current_location()
        self.setWindowTitle("Folium Map")
        self.setGeometry(100, 100, 2000, 2000)
        self.mapObject = foliumMap(latitute=self.latitute, longitude=self.longitude)

        self.tempMarker = None
        self.marker_list = []
        self.marker_uuid_dict = {}

        self.buttons = []
        self.selected_button = None

        self.init_UI()

    def init_UI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.browser = QWebEngineView()

        menus = QVBoxLayout()
        menus.setAlignment(Qt.AlignTop)

        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Enter your address here...")
        self.address_input.setMaximumHeight(70)  # Set the maximum height in pixels
        menus.addWidget(self.address_input)

        search_button = QPushButton("Search")
        menus.addWidget(search_button)
        search_button.clicked.connect(self.handle_search_address)

        information = QVBoxLayout()

        self.address_label = QLabel("Address:")
        self.address_label.setWordWrap(True)
        self.latitute_label = QLabel("Latitude:")
        self.latitute_label.setWordWrap(True)
        self.longitude_label = QLabel("Longitude:")
        self.longitude_label.setWordWrap(True)

        information.addWidget(self.address_label, 0)
        information.addWidget(self.latitute_label, 0)
        information.addWidget(self.longitude_label, 0)

        menus.addLayout(information)

        name_input_widget = QHBoxLayout()
        name_input_widget.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_input_widget.addWidget(self.name_input)

        icon_input_widget = QHBoxLayout()
        icon_input_widget.addWidget(QLabel("Icon:"))

        self.gridLayout = QGridLayout()

        # Create a 3x4 grid of buttons
        for i in range(3):
            for j in range(4):
                index = i * 4 + j
                icon, label = ICON_LABEL_PAIRS[index]
                icon = qta.icon(icon)
                button = QPushButton(icon, label)
                button.setCheckable(True)
                button.clicked.connect(self.button_clicked)
                self.gridLayout.addWidget(button, i, j)
                self.buttons.append(button)

        icon_input_widget.addLayout(self.gridLayout)

        menus.addLayout(name_input_widget)
        menus.addLayout(icon_input_widget)

        self.add_marker_button = QPushButton("Add Marker")
        self.add_marker_button.clicked.connect(self.handle_add_marker)
        menus.addWidget(self.add_marker_button)

        layout.addLayout(menus)

        layout.addWidget(self.browser)

        marker_manage = QVBoxLayout()
        marker_manage.setAlignment(Qt.AlignTop)

        center_marker_button = QPushButton("Reset Center Marker")
        center_marker_button.clicked.connect(self.refresh_map)

        marker_manage.addWidget(center_marker_button)

        self.marker_list_widget = QListWidget()
        marker_manage.addWidget(self.marker_list_widget)

        self.delete_bar = QHBoxLayout()

        self.check_select_button = QPushButton("Check Selected Item")
        self.check_select_button.clicked.connect(self.handle_check_selected_item)
        self.delete_bar.addWidget(self.check_select_button)

        self.delete_button = QPushButton("Delete Selected Item")
        self.delete_button.clicked.connect(self.handle_delete_selected_item)

        self.delete_bar.addWidget(self.delete_button)

        marker_manage.addLayout(self.delete_bar)

        self.save_button = QPushButton("Save HTML")
        self.save_button.clicked.connect(self.handle_save_html)

        marker_manage.addWidget(self.save_button)

        layout.addLayout(marker_manage)

        self.refresh_map()

    def button_clicked(self):
        button = self.sender()
        if self.selected_button and self.selected_button != button:
            self.selected_button.setChecked(False)
            self.selected_button.setStyleSheet("")

        if button.isChecked():
            button.setStyleSheet("background-color: lightblue")
            self.selected_button = button
        else:
            button.setStyleSheet("")
            self.selected_button = None

    def reset_map(self) -> None:
        self.mapObject = foliumMap(latitute=self.latitute, longitude=self.longitude)
        self.add_marker_list()
        # self.refresh_map()

    def refresh_map(self) -> None:
        map = self.mapObject.map
        map.fit_bounds(map.get_bounds(), padding=(30, 30))
        data = io.BytesIO()
        map.save(data, close_file=False)
        self.browser.setHtml(data.getvalue().decode())

    def handle_search_address(self) -> Tuple[float, float]:
        # address = "35 Albert St, Waterloo, ON N2L 5E2, CA"
        address = self.address_input.toPlainText()
        self.address_label.setText("Address:\n" + get_details(address))
        latitute, longitude = address_to_coordinate(address)
        self.latitute_label.setText("Latitude: " + str(latitute))
        self.longitude_label.setText("Longitude: " + str(longitude))
        self.set_temp_marker(latitute, longitude, address)
        return latitute, longitude

    def handle_add_marker(self) -> None:
        latitute, longitude = self.handle_search_address()
        name = self.name_input.text()
        icon = self.get_selected_items()
        self.add_marker_map(latitute, longitude, name, icon)

    def handle_check_selected_item(self) -> None:
        selected_items = self.marker_list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            uuid = uuid = self.marker_uuid_dict[self.marker_list_widget.row(item)]
            self.highlight_marker(uuid)
        print("UUID: ", self.marker_uuid_dict)
        self.refresh_map()

    def handle_save_html(self) -> None:
        self.mapObject.write_html()

    def get_selected_items(self):
        selected_text = self.selected_button.text()
        return selected_text

    def handle_delete_selected_item(self) -> None:
        selected_items = self.marker_list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            uuid = self.marker_uuid_dict[self.marker_list_widget.row(item)]
            self.delete_marker(uuid)
            self.marker_list_widget.takeItem(self.marker_list_widget.row(item))

        self.marker_uuid_dict = {
            index: marker.uuid for index, marker in enumerate(self.marker_list)
        }

        self.refresh_map()

    def set_temp_marker(self, latitute: float, longitude: float, name: str) -> None:
        new_marker = Marker(
            latitute=latitute,
            longitude=longitude,
            tip=name,
            icon="map-pin",
            color="blue",
        )
        self.reset_map()
        self.mapObject.add_marker(new_marker.marker)
        print("temp marker added")
        self.refresh_map()

    def add_marker_list(self) -> None:
        for marker in self.marker_list:
            self.mapObject.add_marker(marker.marker)

    def add_marker_map(
        self, latitute: float, longitude: float, name: str, icon: str
    ) -> None:
        new_marker = Marker(
            latitute=latitute, longitude=longitude, tip=name, icon=icon, color="red"
        )
        self.marker_list.append(new_marker)
        self.marker_list_widget.addItem(name)
        self.marker_uuid_dict[len(self.marker_list) - 1] = new_marker.uuid
        self.mapObject.add_marker(new_marker.marker)
        self.refresh_map()

    def highlight_marker(self, uuid: str) -> None:
        self.reset_map()
        self.refresh_map()
        for marker in self.marker_list:
            if marker.uuid == uuid:
                new_marker = Marker(
                    latitute=marker.location[0],
                    longitude=marker.location[1],
                    tip=marker.tip,
                    icon=marker.icon,
                    color="green",
                )
                self.mapObject.add_marker(new_marker.marker)
                break

    def delete_marker(self, uuid: str) -> None:
        for marker in self.marker_list:
            if marker.uuid == uuid:
                self.marker_list.remove(marker)
                break
        self.reset_map()
        self.refresh_map()
