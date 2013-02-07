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