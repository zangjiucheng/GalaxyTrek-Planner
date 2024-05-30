import folium

class foliumMap:
    def __init__(self, latitute: float = 0.0, longitude: float = 0.0):
        self.latitute = latitute
        self.longitude = longitude
        self.map = self.init_map()

    def init_map(self) -> folium.Map:
        m = folium.Map([self.latitute, self.longitude], zoom_start=12)
        return m

    def reset_marker() -> None:
        map.fit_bounds(map.get_bounds(), padding=(30, 30))

    def add_marker(self, marker: folium.Marker) -> None:
        marker.add_to(self.map)

    def write_html(self):
        self.map.save("index.html")
