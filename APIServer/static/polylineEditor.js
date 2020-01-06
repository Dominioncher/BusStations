ymaps.ready(init);

let myMap;
let objectManager;

function init() {
    createMap();
    onMapClick();
    createMapButtons();
    loadGraph();
    loadStations();
}

// Добавленые остановки
let addedPlacemarks = []
let multiRoute;

// Кнопки
let button1;
let button2;
let button3;
let button4;

// Текуший режим карты
let editMode = false;
let addMode = false;
let removeMode = false;

// Создаем карту.
function createMap() {
    myMap = new ymaps.Map("map", {
        center: [57.151293, 65.537817],
        zoom: 15,
        controls: []
    }, {
        searchControlProvider: 'yandex#search'
    });
    myMap.events.add('click', onMapClick);

    objectManager = new ymaps.ObjectManager({
        // Чтобы метки начали кластеризоваться, выставляем опцию.
        clusterize: true,
        // ObjectManager принимает те же опции, что и кластеризатор.
        gridSize: 10,
        clusterDisableClickZoom: true
    });

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    objectManager.objects.options.set('preset', 'islands#blueDotIcon');
    objectManager.clusters.options.set('preset', 'islands#blueClusterIcons');
    objectManager.objects.events.add(['click'], onCheckpointClick);
    myMap.geoObjects.add(objectManager);
}
// Сохдать кнопоки редактировать, добавить, удалить
function createMapButtons() {
    button1 = createButton("Редактировать");
    button1.events.add(['press'], function (e) {
        editMode= addMode = removeMode = false;
        editMode = !button1.isSelected();
        button3.deselect()
        button2.deselect()
    });
    button2 = createButton("Добавить");
    button2.events.add(['press'], function (e) {
        editMode= addMode = removeMode = false;
        addMode = !button2.isSelected();
        button3.deselect()
        button1.deselect()
    });
    button3 = createButton("Удалить");
    button3.events.add(['press'], function (e) {
        editMode= addMode = removeMode = false;
        removeMode = !button3.isSelected();
        button1.deselect()
        button2.deselect()
    });
    button4 = createButton("Оптимизировать", false);
    button4.events.add(['press'], onOptimizeClick);

    myMap.controls.add(button1, {float: 'right'});
    myMap.controls.add(button2, {float: 'right'});
    myMap.controls.add(button3, {float: 'right'});
    myMap.controls.add(button4, {float: 'right'});
}
// Создать кастомную кнопку
function createButton(title, select = true) {
    return new ymaps.control.Button({
        data: {
            title: title,
            content: title
        },
        options: {
            maxWidth: 150,
            selectOnClick: select
        }
    });
}
// Создать новую остановку
function createPlacemark(value) {
    return new ymaps.Placemark([value.lat, value.lon], {
        balloonContent: value.name + '<br>' + value.description,
    }, {
        preset: 'islands#greenDotIcon'
    });
}
// Сохдать метку остановки в кластере
function createPointsCluster(value) {
    return {
        type: "Feature",
        id: value.id,
        geometry: {
            type: "Point",
            coordinates: [value.lat, value.lon]
        },
        properties: {
            balloonContentHeader: value.name + '<br>' + value.description
        }
    }
}

// Инициализация графа
function loadGraph() {
    const Http = new XMLHttpRequest();
    Http.open('GET', '/loadData', false);
    Http.send('');
}
// Запрос к нашей api для получения остановок
function loadStations() {
    objectManager.removeAll();
    myMap.geoObjects.remove(multiRoute);
    const Http = new XMLHttpRequest();
    Http.onload = (e) => {
        if (Http.status === 200) {
            let values = JSON.parse(Http.responseText);
            const features = [];
            values.forEach(x => features.push(createPointsCluster(x)));
            values = {
                type: 'FeatureCollection',
                features: features
            };
            objectManager.add(values);
            addBusLine(features)
        }
    };
    Http.open('GET', '/checkpoints');
    Http.send('');
}
// Соединяем остановки
function addBusLine(features) {
    let dots = [];
    features.forEach(x => dots.push(x.geometry.coordinates));
    multiRoute = new ymaps.multiRouter.MultiRoute({
        // Описание опорных точек мультимаршрута.
        referencePoints: dots,
    }, {
        wayPointVisible: false
    });
    myMap.geoObjects.add(multiRoute)
}

// Клик на остановку
function onCheckpointClick(e) {
    let objectId = e.get('objectId');
    if (editMode) {
        let Http = new XMLHttpRequest();
        Http.onload = (e) => {
            if (Http.status === 204) {
                objectManager.objects.setObjectOptions(objectId, {
                    preset: 'islands#yellowIcon'
                });
            }
        };
        Http.open('GET', `/modifyCheckpoints?id=${objectId}`);
        Http.send('');
    }

    if (removeMode) {
        let Http = new XMLHttpRequest();
        Http.onload = (e) => {
            if (Http.status === 200) {
                let value = JSON.parse(Http.responseText);
                if (!value){
                    return
                }

                objectManager.remove([objectId])
            }
        };
        Http.open('GET', `/removeCheckpoint?id=${objectId}`);
        Http.send('');
    }
}
// Клик по карте
function onMapClick(e) {
    if (!addMode) {
        return
    }

    const coords = e.get('coords');
    let Http = new XMLHttpRequest();
    Http.onload = (e) => {
        if (Http.status === 200) {
            let value = JSON.parse(Http.responseText);
            value = createPlacemark(value);
            addedPlacemarks.push(value);
            myMap.geoObjects.add(value)
        }
    };
    Http.open('GET', `/addCheckpoint?lat=${coords[0]}&lon=${coords[1]}`);
    Http.send('');
}
// Оптимизация маршрутов
function onOptimizeClick(e) {
    let Http = new XMLHttpRequest();
    Http.onload = (e) => {
        if (Http.status === 204) {
            removeAllPlacemarks();
            loadStations()
        }
    };
    Http.open('GET', `/optimizeCheckpoint`);
    Http.send('');
}

// Удалить все добавленные метки
function removeAllPlacemarks() {
    addedPlacemarks.forEach(x=>myMap.geoObjects.remove(x));
    addedPlacemarks = []
}