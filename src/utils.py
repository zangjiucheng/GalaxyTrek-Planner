import subprocess
from typing import Tuple
from geopy.geocoders import Nominatim

from src.my_uuid import UUIDManager


def run_bash_command(command) -> str:
    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr


def current_location() -> Tuple[float, float]:  # latitude, longitude
    command = "curl ipinfo.io/loc"
    output = run_bash_command(command)
    output = output.strip().split(",")
    return float(output[0]), float(output[1])


def address_to_coordinate(address: str) -> Tuple[float, float]:
    geolocator = Nominatim(user_agent="GetLoc")
    # address = "35 Albert St, Waterloo, ON N2L 5E2, CA"
    location = geolocator.geocode(address)
    return location.latitude, location.longitude


def coordinate_to_address(latitude: float, longitude: float) -> str:
    geolocator = Nominatim(user_agent="myGeocodingApp")
    location = geolocator.reverse((latitude, longitude))
    if location:
        return location.address
    else:
        raise Exception("Address not found.")


def get_details(address: str) -> str:
    geolocator = Nominatim(user_agent="myGeocodingApp")
    location = geolocator.geocode(address, addressdetails=True)
    if location:
        return location.address
    else:
        raise Exception("Address not found.")


def get_uuid() -> str:
    uuidmanager = UUIDManager(version=1)
    return uuidmanager.generate()


if __name__ == "__main__":
    # lat,loc = current_location()
    address = "35 Albert St, Waterloo, ON N2L 5E2, CA"
    lat, loc = address_to_coordinate(address)
    new_address = coordinate_to_address(lat, loc)
    print(lat,loc)
    print(new_address)
    print(get_details(address))
