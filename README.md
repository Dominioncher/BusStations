# BusStations

Задача оптимизации автобусных остановок

Канбан: https://app.zenhub.com/workspaces/busstations-5d8b36eb1165610001735c1c/board?repos=210808405

Heroku: https://bus-station.herokuapp.com

Production окружение: http://104.197.28.13

Pre-release окружение: http://104.155.169.12

Dev окружение : http://34.70.209.167

Кушинр.А:
1. Создание каркаса проекта
2. Объединение данных и запись в базу
3. Формальная постановка задачи

Ромашин.А:
1. Граф
2. Решение задачи оптимизации

Дзябенко.Е:
1. Данные
2. Интерфейс карты

Описание проекта:

Наложение данных по транспорту г.Тюмени с сайта Гортранс на модель графа.
Решение оптимизационной задачи по оптимальному распределению маршрутов с учетом перекрытых участков дорог и рядом других ограничений.
Возможность в визуальном интерфейсе перекрывать участки дорог и добавлять временные остановки с целью пересчета оптимальных маршрутов с учетом новых остановок.
Язык разработки Python
Данные о маршрутах и остановках будут браться с сайта гортранса
В качестве базы данных будет использоваться mongoDB
Для построения графа igraph или networkX
Интерфейс Яндекс.Карты или Google maps
Проект предназначен для муниципальной среды с целью выбора наиболее удачных переносов остановок с целью уменьшения загруженности транспортного потока
