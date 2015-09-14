[^](hrmgr.md)
# Назначение #

Обработка резюме и вакансий на рекрутинговых сайтах - обработка вакансий и соискателей на сайтах:
  * [job.ru](http://www.job.ru/)
  * [supejob.ru](http://www.superjob.ru/)
  * [hh.ru](http://hh.ru/)
  * [zarplata.ru](http://www.zarplata.ru/)
  * [joblist.ru](http://joblist.ru/)
  * [rabota.ru](http://www.rabota.ru/)
  * [rabota.mail.ru](http://rabota.mail.ru/)

# Потребители #
  * Кадровые агентства (заполнение вакансий, поиск резюме)
  * Частные лица - соискатели (заполнение резюме, поиск вакансий)

# Возможности #
  * CRUD (Create, Read, Update, Delete - Создание, Чтение, Изменение, Удаление) вакансий и резюме;
  * работа одновременно со всеми сайтами;
  * работа через несколько протоколов - веб, почта, RSS;
  * кеширование изменений - все изменения, сделанные локально, применяются к сайтам за раз;
  * многопользовательский режим;
  * разделение полномочий;
  * журналирование операций;
  * фиксирование дублей - как в пределах сайта, так и между сайтами;
  * анонимный/обычный (с логином-паролем к сайтам) режимы;

# Особенности #
  * Автоматическое обдирание сайтов;
  * Адаптеры CRUD сайтов - для каждого - свой;
  * Асинхронный кеширующий режим:
    * вся работа - с локальной базой;
    * которая периодически и/или по запросу синхронизируется с сайтами;

# Реализация #
  * Единый формат передачи и хранения, основанный на [HR-XML](http://www.hr-xml.org);
  * Адаптеры: логин/логаут, CRUD, html2hrxml, hrxml2html, form fill;
  * у каждой записи, кроме резюмно/вакансных, есть атрибуты (поля):
    * для работы (коментарии, важность, просмотрено и т.д.);
    * синхронности (синхронизировано или как);
    * журнал изменений (когда, кто, что, как изменил);
    * как вариант - ест некий 1 сайт, который централизованно работает со всеми сайтами и со всеми клиентами;

# Use cases #
## Вакансии ##
### Чтение ###
#### HTTP ####
  * login (fill forms)
  * select categories/records (query/form)
  * get pages
  * logout
  * render pages into site-specific objects
  * convert lasts into common objects
  * write:
    * check:
      * duplicates
      * changed
    * write locally

### Обработка ###
  * Отбор:
    * группировка
    * сортировка
    * фильтр
  * обработка записи:
    * комментарии
    * отметка (по типу mail - прочтено. важно, спам и т.д.)

### Создание ###
  * create common obkect
  * select - where distribute to
  * save locally
  * synced = False

### Изменение ###
  * изменить содержание
  * изменить размещение
  * changed flag == True
  * synced = False

### Удаление ###
  * deleted flag = True
  * synced = False

### Синхронизация ###
  * Read new records
  * set New = True
  * Write:
    * delete deleted
    * update changed
    * add created
    * on success = synced = True

## Резюме ##

# Возможные засады #
  * javascript (webkit/xullrunner)

# Vocabulary #

# Ход работы #
Нам понадобятся объекты Candidate, PositionOpening, Resume и NewHire из кинофильма [HR-XML 3.0](http://ns.hr-xml.org/schemas/org_hr-xml/3_0/Documentation/indexes/index.php).

# Анализ сайтов #
[Job.Ru](HrmgrJobru.md)