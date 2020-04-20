import cv2
import io
import requests
import numpy as np
from src import utils
from math import log, exp, tan, atan, pi, ceil

MAX_RESOLUTION = 500
EARTH_RADIUS = 6378137
EQUATOR_CIRCUMFERENCE = 2 * pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / 256.0
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0
DEFAULT_ZOOM = 19
DEFAULT_RESOLUTION = [5000, 5000]


# Map reader class #
class MapReader:
    def __init__(self):
        self.__key = utils.get_api_key()

    def __get_address_coordinates(self, address):
        """
        :param address: [str] Zone or address of the desired map
        :return: [float, float] Latitude and longitude of the found address
        """
        url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
               .format(address.replace(' ', '+'), self.__key))
        try:
            response = requests.get(url)
            resp_json_payload = response.json()
            lat = resp_json_payload['results'][0]['geometry']['location']['lat']
            lng = resp_json_payload['results'][0]['geometry']['location']['lng']
            coordinates = [lat, lng]
        except Exception as e:
            print('ERROR: {}'.format(e))
            coordinates = [0, 0]
        return coordinates

    def __latlontopixels(self, lat, lon, zoom):
        """
        :param lat: [float] Latitude coordinates
        :param lon: [float] Longitude coordinates
        :param zoom: [int] Zoom of the map
        :return: [int, int] X and Y pixel coordinates of the desired point
        """
        mx = (lon * ORIGIN_SHIFT) / 180.0
        my = log(tan((90 + lat) * pi / 360.0)) / (pi / 180.0)
        my = (my * ORIGIN_SHIFT) / 180.0
        res = INITIAL_RESOLUTION / (2 ** zoom)
        px = (mx + ORIGIN_SHIFT) / res
        py = (my + ORIGIN_SHIFT) / res
        return px, py

    def __pixelstolatlon(self, px, py, zoom):
        """
        :param px: [int] X coordinates on pixels
        :param py: [int] Y coordinates on pixels
        :param zoom: [int] Zoom of the map
        :return: [float, float] Latitude and longitude of the desired point
        """
        res = INITIAL_RESOLUTION / (2 ** zoom)
        mx = px * res - ORIGIN_SHIFT
        my = py * res - ORIGIN_SHIFT
        lat = (my / ORIGIN_SHIFT) * 180.0
        lat = 180 / pi * (2 * atan(exp(lat * pi / 180.0)) - pi / 2.0)
        lon = (mx / ORIGIN_SHIFT) * 180.0
        return lat, lon

    def get_by_coordinates(self, coordinates, resolution=DEFAULT_RESOLUTION, zoom=DEFAULT_ZOOM):
        """
        :param coordinates: [float, float] Latitude and longitude coordinates
        :param resolution: [int, int] Size in pixels of the final image (multiples of 500)
        :param zoom: [int] Zoom of the map
        :return: [np.array] Composed image using the Google Maps Static API.
        """

        lat, lon = coordinates

        # convert all these coordinates to pixels
        clx, cly = self.__latlontopixels(lat, lon, zoom)

        # calculate total pixel dimensions of final image
        ulx, uly = clx - int(ceil(resolution[0] / 2)), cly + int(ceil(resolution[0] / 2))
        lrx, lry = clx + int(ceil(resolution[1] / 2)), cly - int(ceil(resolution[1] / 2))
        dx, dy = lrx - ulx, uly - lry

        # calculate rows and columns
        cols, rows = int(ceil(dx / MAX_RESOLUTION)), int(ceil(dy / MAX_RESOLUTION))
        # calculate pixel dimensions of each small image
        w, h = [MAX_RESOLUTION, MAX_RESOLUTION]

        # assemble the image from stitched
        final = np.zeros([resolution[0], resolution[1], 3],dtype=np.uint8)
        for x in range(cols):
            for y in range(rows):
                dxn = w * (0.5 + x)
                dyn = h * (0.5 + y)
                latn, lonn = self.__pixelstolatlon(ulx + dxn, uly - dyn, zoom)
                url = 'https://maps.googleapis.com/maps/api/staticmap?center={},{}&size={}x{}&zoom={}&key={' \
                      '}&maptype=satellite&scale=1'.format(latn, lonn, w, h, zoom, self.__key)
                stream = io.BytesIO(requests.get(url).content)
                file_bytes = np.asarray(bytearray(stream.read()), dtype=np.uint8)
                im = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                # src.utils.save_image('{}{}'.format(x,y),im)
                final[int(y * h):int((y + 1) * h), int(x * w):int((x + 1) * w), :] = im
                print('Image download: {}%'.format(float(x * rows + (y + 1)) / float(rows * cols) * 100.0))
        return final

    def get_by_zone(self, zone, resolution=DEFAULT_RESOLUTION, zoom=DEFAULT_ZOOM):
        """
        :param zone: [str] Zone or address of the desired map
        :param resolution: [int, int] Size in pixels of the final image (multiples of 500)
        :param zoom: [int] Zoom of the map
        :return: [np.array] Composed image using the Google Maps Static API.
        """
        zone_coordinates = self.__get_address_coordinates(zone)
        image = self.get_by_coordinates(zone_coordinates, resolution=resolution, zoom=zoom)
        return image
