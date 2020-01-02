ymaps.ready(init);

let myMap;
let objectManager;

function init() {
    createMap();
    clickEvent();
    addButtons();
    load();
    loadStations();
}


// Создаем карту.
function createMap() {
    myMap = new ymaps.Map("map", {
        center: [57.151293, 65.537817],
        zoom: 15
    }, {
        searchControlProvider: 'yandex#search'
    });

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
    myMap.geoObjects.add(objectManager);
}

// Узнаем по клику координаты
function clickEvent() {
    myMap.events.add('click', function (e) {
        const coords = e.get('coords');
        console.log('lat=',coords[0].toPrecision(7),',lon=', coords[1].toPrecision(7),',name=1');
        if (addMode){
            addNewStation(coords);
            console.log('Добавили точку');
        }
    });

}

// Ручное добавление новой остановки
function addNewStation(coords) {
    let Http = new XMLHttpRequest();
    Http.onload = (e) => {
        if (Http.status === 200) {
            let value = JSON.parse(Http.responseText);
            value = AddNewCheckpoint(value)
            myMap.geoObjects.add(value)
        }
    };
    Http.open('GET', `/addCheckpoint?lat=${coords[0]}&lon=${coords[1]}`);
    Http.send('');
}

// Инициализация графа
function load() {
    const Http = new XMLHttpRequest();
    Http.open('GET', '/loadData', false);
    Http.send('');
}

// Запрос к нашей api для получения остановок
function loadStations() {
    const Http = new XMLHttpRequest();
    Http.onload = (e) => {
        if (Http.status === 200) {

            console.log('load stations');
            let values = JSON.parse(Http.responseText);
            const features = [];
            values.forEach(x => features.push(AddCheckpoint(x)));
            values = {
                type: 'FeatureCollection',
                features: features
            };
            objectManager.removeAll();
            objectManager.add(values);
            addBusLine(features)
        }
    };
    Http.open('GET', '/checkpoints');
    Http.send('');
}

// Добавить новую остановку
function AddNewCheckpoint(value) {
    return new ymaps.Placemark([value.lat, value.lon], {
        balloonContent: value.name + '<br>' + value.description,
    }, {
        preset: 'islands#greenDotIcon'
    });
}

// Добавить метку остановки на карту
function AddCheckpoint(value) {
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

// Соединяем остановки
function addBusLine(features) {
    let dots = [];
    console.log('lines');
    features.forEach(x => dots.push(x.geometry.coordinates));
    var multiRoute = new ymaps.multiRouter.MultiRoute({
        // Описание опорных точек мультимаршрута.
        referencePoints: dots,
    }, {
        wayPointVisible: false
    });
    myMap.geoObjects.add(multiRoute)
}

// Текуший режим карты
let editMode = false;
var addMode = false;
let removeMode = false;

// Добавление кнопок редактировать, добавить, удалить
function addButtons() {
    const button1 = new ymaps.control.Button("Редактировать");
    button1.events.add(['press'], function (sender) {
       editMode= addMode = removeMode = false;
       editMode = !sender.originalEvent.target.isSelected();
    });
    const button2 = new ymaps.control.Button("Добавить");
    button2.events.add(['press'], function (sender) {
        editMode= addMode = removeMode = false;
        addMode = !sender.originalEvent.target.isSelected();
    });
    const button3 = new ymaps.control.Button("Удалить");
    button3.events.add(['press'], function (sender) {
        editMode= addMode = removeMode = false;
        removeMode = !sender.originalEvent.target.isSelected();
    });

    myMap.controls.add(button1, {float: 'right'});
    myMap.controls.add(button2, {float: 'right'});
    myMap.controls.add(button3, {float: 'right'});
}