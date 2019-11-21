from Core.DataLoaders.DataLoader import get_checkpoints
from pygeoplot import api


if __name__ == '__main__':
    geo_map = api.Map()
    imikn = api.GeoPoint(57.158820, 65.522632)
    geo_map.add_placemark(imikn)