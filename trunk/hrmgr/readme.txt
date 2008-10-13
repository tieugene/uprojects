= Job.ru =

== Account ==

=== Employer ===

Note: бесплатный account даёт возможность размещать 5 вакансий за 30 дней.

- e-mail:email
- password:string
- Contact:
-- FirstName:string
-- [MidName:string]
-- LastName:string
-- JobRole:enum <jobrole>
- Company:
-- Название:string
-- Тип:enum <employertype>
-- Отрасль:enum <branch>
-- Кол-во сотрудников:enum <emploqty>
-- Страна:enum <country>
-- Регион:enum <region>
-- Город/район:enum <city>
-- Адрес:string
-- [Индекс:int]
-- Телефон:phone
-- [Телефон 2:phone]
-- [Факс:phone]
-- [E-mail для соискателей:email]
-- [Корпортативный сайт:URL]
-- [Год основания:enum 1990, 1991, ..., 2007, очень давно]
-- [Logo:image (gif, jpg, bmp, png)]
-- Профиль компании:text
-- [История компании:text]
-- [Руководство компании:text]
-- [Структура компании:text]
-- [Филиалы:text]
-- Предпочтительный способ связи:enum <communication>

== Вакансия ==

=== Аноним ===

==== Мини ====

- наименование:string
- [код:auto]
- текст:text
- [зарплата:]
-- [.от:int]
-- [.до:int]
-- [.валюта:enum <currency>]
-- [.в:enum <freq>]
- [занятость:enum <duration>]
- [уровень позиции:enum <poslevel>]
- отрасль:enum <branch>
- специализация:enum:spec -in-отрасль [todo]
- Страна:enum <country>
- регион:enum <region>
- [город/район:enum <city>]
- контактное лицо:
	- должность:enum <jobrole>
	- имя:string
	- фамилия:string
	- e-mail:string
	- телефон:phone

=== Registered ===

==== Мини ====

<anon.mini>
- Вакансия будет видна:bool (Всем посетителям сайта, Только мне)
- Опубликовать вакансию:bool Сейчас, с указанной даты:date
- Я хочу разместить эту вакансию в разделе "Вакансии дня"?:bool
- Создать анонимную вакансию?:bool; if True:
-- E-mail для откликов:email
-- Компания (напр., Крупнейший банк):string
- Да, я хочу опубликовать эту вакансию в газете "Работа Сегодня" (только московский выпуск):bool
- Логотип компании в результатах поиска - Заказать:bool
- Комментарии к вакансии:text

=== Подробная ===
<anon.mini>
- [Опыт работы:enum <experience>]
- [Образование:enum <education>]
- [Возраст:]
-- .от:int
-- .до:int
- [Пол:enum <sex>]
- Профессиональные навыки: []
-- Сфера:enum-in-отрасль
-- Навыки:enum-in-Сфера
-- минимальный уровень:enum <minlevel>
- Водительские права:bool; if True: enum <driverlic>
- Знание языков: []
-- Язык:enum <language>
-- Минимальный уровень:enum <langlevel>
<reg.mini>

== Соискатель ==

== Резюме ==

== Поиск резюме ==

== мини ==
- Регион
- Отрасль (сфера деятельности)
- опыт работы:enum <experience>
- Специализация:text
- Образование:enum <education>
