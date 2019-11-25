ymaps.ready(init);

function init() {
    // Создаем карту.
    var myMap = new ymaps.Map("map", {
            center: [57.151293, 65.537817],
            zoom: 15
        }, {
            searchControlProvider: 'yandex#search'
        });

    // Запрос к нашей api для получения остановок
    const Http = new XMLHttpRequest();
    const url='http://127.0.0.1:5000/checkpoints';
    Http.onreadystatechange = (e) => {
        if (Http.status == 200)
        {
            values = JSON.parse(Http.responseText);
            values = values.slice(0, 100);
            values.forEach(x => AddCheckpoint(x));
        }
    }

    function AddCheckpoint(value) {
        myMap.geoObjects
            .add(new ymaps.Placemark([value.projected_lat, value.projected_lon], {
                balloonContent: value.name + '<br>' + value.description
            }, {
                preset: 'islands#icon',
                iconColor: '#0095b6'
            }))
        console.log(value);
    }

    Http.open('GET', url);
    Http.send('');
}
