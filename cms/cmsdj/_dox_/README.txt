Apps:
    + Patient (Поциенты) => ЭМК => История => => Посещение => МедЗапись
    + Employee (Сотрудники)
	+ Core (Person w/ deps)
    * Ref (Справочники):
        * Address
        * MKB-10
        * МедУслуги
        * Справочник лекарств
    + Enum
== fixtures ==
./manage.py dumpdata --format=json --indent=2 enum > enum.json
or

= try =
django-popup-forms
django-ajax-selects
python-django-dajax
python-django-dajaxice

= predefined person =
* disable - отсутствует в POST
* hidden - ok, но не скрывает заголовок
* exclude() - не проверяет валидность формы по person
? disabled + required=False
? Лучше всего - filter

= ОК СПМУ =
XX.YYY.ZZ
Т.к. YYY повторяется - лучше сделать 3 таблицы

= ОК ПМУ =
то же самое
XX.YY.ZZZ

= мкб-10 =
C##.#+
но:
    рим - классы
    в него входят рубрики с блоками рубрик.
    рубрика - C##