ymaps.ready(init);

var myMap;
var objectManager;

function init() {
    createMap();
    clickEvent();
    loadStations();
    addButtons();
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
        gridSize: 100,
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
        var coords = e.get('coords');
        console.log('lat=',coords[0].toPrecision(7),',lon=', coords[1].toPrecision(7),',name=1');
        if (addMode){
            addNewStation(coords);
            console.log('Добавили точку');
            loadStations()
        }
    });

}

// Ручное добавление новой остановки
function addNewStation(coords) {
    var Http = new XMLHttpRequest();
    Http.open('GET', `/addCheckpoint?lat=${coords[0]}&lon=${coords[1]}`);
    Http.send('');
}

// Запрос к нашей api для получения остановок
function loadStations() {
    var Http = new XMLHttpRequest();
    Http.onreadystatechange = (e) => {
        if (Http.status === 200) {
            var values = JSON.parse(Http.responseText);
            var features = [];
            values.forEach(x => features.push(AddCheckpoint(x)));
            values = {
                type: 'FeatureCollection',
                features: features
            };
            objectManager.removeAll();
            objectManager.add(values);
            //addBusLine(features)
        }
    };
    Http.open('GET', '/checkpoints');
    Http.send('');
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
            balloonContentHeader: value.name + '<br>'
                + value.description + '<br>' +
                ''
        }
    }
}

// Соединяем остановки
function addBusLine(features) {
    var dots = [];
    features.forEach(x => dots.push(x.geometry.coordinates));
    var myPolyline = new ymaps.Polyline(dots, {
        // Описываем свойства геообъекта.
        // Содержимое балуна.
        balloonContent: "Ломаная линия"
    }, {
        // Задаем опции геообъекта.
        // Отключаем кнопку закрытия балуна.
        balloonCloseButton: false,
        // Цвет линии.
        strokeColor: "#000000",
        // Ширина линии.
        strokeWidth: 4,
        // Коэффициент прозрачности.
        strokeOpacity: 0.5
    });
    myMap.geoObjects.add(myPolyline)
}

// Текуший режим карты
var editMode = false;
var addMode = false;
var removeMode = false;

// Добавление кнопок редактировать, добавить, удалить
function addButtons() {
    var button1 = new ymaps.control.Button("Редактировать");
    button1.events.add(['press'], function (sender) {
       editMode= addMode = removeMode = false;
       editMode = !sender.originalEvent.target.isSelected();
    });
    var button2 = new ymaps.control.Button("Добавить");
    button2.events.add(['press'], function (sender) {
        editMode= addMode = removeMode = false;
        addMode = !sender.originalEvent.target.isSelected();
    });
    var button3 = new ymaps.control.Button("Удалить");
    button3.events.add(['press'], function (sender) {
        editMode= addMode = removeMode = false;
        removeMode = !sender.originalEvent.target.isSelected();
    });

    myMap.controls.add(button1, {float: 'right'});
    myMap.controls.add(button2, {float: 'right'});
    myMap.controls.add(button3, {float: 'right'});
}