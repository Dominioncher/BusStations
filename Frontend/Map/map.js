ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
            center: [57.158820, 65.522632],
            zoom: 12
        }, {
            searchControlProvider: 'yandex#search'
        });

    myMap.geoObjects
        .add(new ymaps.Placemark([57.158820, 65.522632], {
            balloonContent: 'ИМИКН'
        }, {
            preset: 'islands#governmentCircleIcon',
            iconColor: '#0095b6'
        }))        ;
}
