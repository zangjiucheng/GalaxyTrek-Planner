# from folium import Marker,Icon
import folium

from src.utils import get_uuid


class Marker:
    def __init__(
        self, latitute: float, longitude: float, tip: str, icon: str, color: str
    ) -> None:
        self.uuid = get_uuid()
        self.location = [latitute, longitude]
        self.tip = tip
        self.icon = icon
        self.color = color
        self.marker = folium.Marker(
            location=self.location,
            tooltip=self.tip,
            popup=self.tip,
            icon=folium.Icon(icon=icon, prefix="fa", color=self.color),
        )

    def rewrite_marker(self) -> None:
        self.marker = folium.Marker(
            location=self.location,
            tooltip=self.tip,
            popup=self.tip,
            icon=folium.Icon(icon=self.icon, prefix="fa", color=self.color),
        )

    def set_location(self, latitute: float, longitude: float) -> None:
        self.location = [latitute, longitude]
        self.rewrite_marker()

    def set_tip(self, tip: str) -> None:
        self.tip = tip
        self.rewrite_marker()

    def set_icon(self, icon: str) -> None:
        self.icon = icon
        self.rewrite_marker()

    def set_color(self, color: str) -> None:
        self.color = color
        self.rewrite_marker()

    def set_man_uuid(self, uuid: str) -> None:
        self.uuid = uuid
