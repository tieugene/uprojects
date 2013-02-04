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
