import requests


def distance_finder(lat1, lng1, lat2, lng2):
    maps_key = 'AIzaSyA2XatPXMVT8Z_s7ZabHNFjw9xYcShWuh4'
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    url = base_url + '?' + 'origins=' + str(lat1) + '%2C' + str(lng1) + '&destinations=' + str(lat2) + '%2C' \
        + str(lng2) + '&key=' + maps_key

    response = requests.get(url).json()
    res = response['rows'][0]['elements'][0]
    result = dict()
    result['dist'] = res['distance']['value']
    result['time'] = res['duration']['value']
    return result


if __name__ == '__main__':
    lat1 = 57.10812
    lng1 = 65.73392
    lat2 = 57.10484
    lng2 = 65.73185
    dist = distance_finder(lat1, lng1, lat2, lng2)
    print('Distance:', dist)
