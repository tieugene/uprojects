# Intro #
Описание данных на сайте [Job.Ru](http://www.job.ru)

# Объекты #

## Employer ##
### CommonEmployer ###
| Mandatory | Name | Field | Type | Default | Comments |
|:----------|:-----|:------|:-----|:--------|:---------|
| Company   | | | | | |
| +         | Название | Name  | string | NULL    |          |
| +         | Тип  | EmployerType | enum:[employertype](HrmgrJobruEnumEmployertype.md) | NULL    |          |
| +         | Отрасль | Branch | enum:[branch](HrmgrJobruEnumBranch.md) | NULL    |          |
| +         | Страна | Country | enum:[country](HrmgrJobruEnumCountry.md) | NULL    |          |
| +         | Регион | Region | enum:[region](HrmgrJobruEnumRegion.md) | NULL    | dep. on Country |
| ...       | Город/район | Place | enum:[place](HrmgrJobruEnumPlace.md) | NULL    | dep. on Region |
|           | Индекс | Index | int  | NULL    |          |
|           | Адрес | Address | string | NULL    |          |
| +         | Телефон | Phone | phone | NULL    |          |
|           | Телефон 2 | Phone2 | phone | NULL    |          |
|           | Факс | Fax   | phone | NULL    |          |
|           | Общий E-mail | CandidateEmail | email | NULL    |          |
|           | Корпоративный сайт | WWW   | www  | NULL    |          |
|           | Логотип | Logo  | image | NULL    | gif, jpg, bmp, png |
|           | Кол-во сотрудников | EmployersQty | [empqty](HrmgrJobruEnumEmpqty.md) | NULL    |          |
|           | Год основания | YearFounded | enum:[yearfound](HrmgrJobruEnumYearfound.md) | NULL    |          |
|           | Краткое описание компании | CompanyProfile | text | NULL    |          |
|           | История компании | CompanyHistory | text | NULL    |          |
|           | Руководство компании | CompanyAdm | text |         |          |
|           | Филиалы | Company | CompanyOffices | text    | NULL     |
|           | Структура компании | CompanyStructure | text | NULL    |          |
| Auth      | | | | | |
| +         | E-Mail | Email | email | NULL    |          |
| +         | Пароль | Password | string | NULL    |          |
| Contact   | | | | | |
| +         | Имя  | FirstName | string | NULL    |          |
| +         | Фамилия | LastName | string | NULL    |          |
|           | Должность | JobRole | enum:[jobrole](HrmgrJobruEnumJobrole.md) | NULL    |          |
|           | Телефон | Phone | phone | NULL    |          |
| +         | Предпочтительный способ связи | PreferedCommunication | enum:[prefcommunication](HrmgrJobruEnumPrefcommunication.md) | NULL    |          |

## AnonEmployer ##
| Mandatory | Name | Field | Type | Default | Comments |
|:----------|:-----|:------|:-----|:--------|:---------|
| 

&lt;AnonEmployer&gt;

 | | | | | |
| +         | Юр.Адрес | Address | string | NULL    |          |

## RegisteredEmployer ##

Note: Бесплатный account дает возможность публиковать 5 бесплатных вакансий за 30 дней.

| Mandatory | Name | Field | Type | Default | Comments |
|:----------|:-----|:------|:-----|:--------|:---------|
| 

&lt;AnonEmployer&gt;

 | | | | | |
|           | Отчество | MidName | string | NULL    |          |
| +         | Должность | JobRole | enum:[jobrole](HrmgrJobruEnumJobrole.md) | NULL    |          |
| Company   | | | | | |
| +         | Кол-во сотрудников | EmployersQty | [empqty](HrmgrJobruEnumEmpqty.md) | NULL    |          |
| +         | Адрес | Address | string | NULL    |          |
|           | E-mail для соискателей | CandidateEmail | email | NULL    |          |
| +         | Профиль компании | CompanyProfile | text | NULL    |          |

# Вакансия #
## Mini ##

Для анонимных юзверей.

| Mandatory | Name | Field | Type | Default | Comments |
|:----------|:-----|:------|:-----|:--------|:---------|
| Описание вакансии | | | | | |
| +         | Наименование | Name  | string | NULL    |          |
|           | Код  | ID    | string | NULL    |          |
| +         | Текст | Description | text | NULL    |          |
|           | Зарплата.От | PayMin | int  | NULL    |          |
|           | Зарплата.До | PayMax | int  | NULL    |          |
| +if       | Зарплата.Валюта | PayCurrency | enum:[currency](HrmgrJobruEnumCurrency.md) | NULL    | Need if PayMin or PayMax |
| +if       | Зарплата.За | PayFreq | enum:[freq](HrmgrJobruEnumFreq.md) | NULL    | Need if PayMin or PayMax |
|           | Занятость | Duration | enum:[freq](HrmgrJobruEnumFreq.md) | NULL    |          |
|           | Уровень позиции | PosLevel | enum:[poslevel](HrmgrJobruEnumPoslevel.md) | NULL    |          |
| Месторасположение, проф. область | | | | | |
| +         | Отрасль | Branch | enum:[branch](HrmgrJobruEnumBranch.md) | NULL    |          |
| +         | Специализация | Spec  | enum:[spec](HrmgrJobruEnumSpec.md) | NULL    | Sub of Branch |
| +         | Страна | Country | enum:[country](HrmgrJobruEnumCountry.md) | NULL    |          |
| +         | Регион | Region | enum:[region](HrmgrJobruEnumRegion.md) | NULL    | Sub of Country |
| +if       | Город/район | Place | enum:[place](HrmgrJobruEnumPlace.md) | NULL    | Sub of Region |
| Контактное лицо | | | | | |
|           | Должность | ContactRole | enum:[role](HrmgrJobruEnumRole.md) | NULL    |          |
|           | Имя  | ContactFirstName | string | NULL    |          |
|           | Фамилия | ContactLastName | string | NULL    |          |
|           | E-mail | ContactEmail | email | NULL    |          |
|           | Телефон | ContactPhone | phone | NULL    |          |
| "Видимость" вакансии | | | | | |
| +         | Вакансия будет видна всем | Visible | bool | Всем посетителям сайта |          |
| +if       | Опубликовать вакансию | PubDate | date | NOW()   | need if Всем  |
| Создать анонимную вакансию | | | | | |
| +         | Создать анонимную вакансию | VacAnon | bool | False   |          |
|           | E-mail для откликов | FakeEmail | email | NULL    | if VacAnon = True |
| +if       | Компания | FakeCompany | string | NULL    | if VacAnon = True |
| +if       | Комментарии к вакансии | Comments | text | NULL    |          |

После заполнения - надо указать свой логина/пароль - или надо заполнить информацию о компании AnonEmployer.
В последнем случае - указать контакт

## RegMini ##

Тоже мини, но для зарегистрированных работодателей.

| Mandatory | Name | Field | Type | Default | Comments |
|:----------|:-----|:------|:-----|:--------|:---------|
| 

&lt;Mini&gt;

 | | | | | |
| | Я хочу разместить эту вакансию в разделе "Вакансии дня" | VacOfDay | bool |         |          |
|           | Да, я хочу опубликовать эту вакансию в газете "Работа Сегодня" | PubDayJob | bool |         |          |
|           | Логотип компании в результатах поиска | LogoInSearch | bool |         |          |

## RegFull ##

Подробная.

| Mandatory | Name | Field | Type | Default | Comments |
|:----------|:-----|:------|:-----|:--------|:---------|
| 

&lt;Mini&gt;

 | | | | | |
|           | Опыт работы | Experience | enum:[experience](experience.md) |         |          |
|           | Образование | Educationb | enum:[education](education.md) |         |          |
|           | Возраст.От | AgeMin | int  | NULL    |          |
|           | Возраст.До | AgeMax | int  | NULL    |          |
|           | Пол  | Sex   | enum:sex |         |          |
|           | Водительские права | DriverLic | enum:[driverlic](driverlic.md) | NULL    |          |
| 

&lt;RegMini&gt;

 | | | | | |

RegFull.Acquirement
| Mandatory | Name | Field | Type | Default | Comments |
|:----------|:-----|:------|:-----|:--------|:---------|
| | Сфера | BranchSphere | enum:[branchsphere](branchsphere.md) |         |          |
| | Навыки | SphereAcquire | enum:[sphereaquire](sphereaquire.md) |         |          |
| | Минимальный уровень | AquireLevel | enum:[equirelevel](equirelevel.md) |         |          |

| Mandatory | Name | Field | Type | Default | Comments |
|:----------|:-----|:------|:-----|:--------|:---------|
| | Язык | Lang  | enum:[lang](lang.md) |         |          |
| | Минимальный уровень | LangLevel | enum:[langlevel](langlevel.md) |         |          |


| Mandatory | Name | Field | Type | Default | Comments |
|:----------|:-----|:------|:-----|:--------|:---------|
|           |      |       |      |         |          |

и тут:
> это - блоквота
> и это - блоквота

Это - `код`
это - `отже
какой-то
код`