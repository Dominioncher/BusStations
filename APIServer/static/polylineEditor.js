ymaps.ready(init);

function init() {
    // Создаем карту.
    var myMap = new ymaps.Map("map", {
        center: [57.151293, 65.537817],
        zoom: 15
    }, {
        searchControlProvider: 'yandex#search'
    });
    objectManager = new ymaps.ObjectManager({
        // Чтобы метки начали кластеризоваться, выставляем опцию.
        clusterize: true,
        // ObjectManager принимает те же опции, что и кластеризатор.
        gridSize: 100,
        clusterDisableClickZoom: true
    });

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    objectManager.objects.options.set('preset', 'islands#blueDotIcon');
    objectManager.clusters.options.set('preset', 'islands#blueClusterIcons');
    myMap.geoObjects.add(objectManager);

    // Запрос к нашей api для получения остановок
    const Http = new XMLHttpRequest();
    const url = '/checkpoints';
    Http.onreadystatechange = (e) => {
        if (Http.status == 200) {
            values = JSON.parse(Http.responseText);
            features = []
            values.forEach(x => features.push(AddCheckpoint(x)))
            values = {
                type: 'FeatureCollection',
                features: features
            }
            objectManager.add(values)
        }
    }

    function AddCheckpoint(value) {
        return {
            type: "Feature",
            id: value.id,
            geometry: {
                type: "Point",
                coordinates: [value.projected_lat, value.projected_lon]
            },
            properties: {
                balloonContentHeader: value.name + '<br>' + value.description
            }
        }
    }

    Http.open('GET', url);
    Http.send('');
}
