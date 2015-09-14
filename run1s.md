# Введение #

Данный продукт предназначен для централизованного управления базами 1С.
Аналоги - [run1c](http://pioner-kum.1gb.ru/apxi/).
Отличия:
1. работа в локальной сети;
2. указание видимости баз для различных пользователей.


# Подробности #

Система построена по клиент-серверной технологии.
Все базы и пользователи списка баз описываются на веб-сервере (серверная часть).
Этот же веб-сервер раздаёт клиентам список баз по протоколу http.
Клиентская часть - Qt4-приложение на C++.

Слайды:
## Сервер: ##
  * Users:
![http://uprojects.googlecode.com/files/run1s_s1.png](http://uprojects.googlecode.com/files/run1s_s1.png)
  * Database types:
![http://uprojects.googlecode.com/files/run1s_s2.png](http://uprojects.googlecode.com/files/run1s_s2.png)
  * Organizations:
![http://uprojects.googlecode.com/files/run1s_s3.png](http://uprojects.googlecode.com/files/run1s_s3.png)
  * Databases:
![http://uprojects.googlecode.com/files/run1s_s4.png](http://uprojects.googlecode.com/files/run1s_s4.png)
  * ACL:
![http://uprojects.googlecode.com/files/run1s_s5.png](http://uprojects.googlecode.com/files/run1s_s5.png)
## Клиент ##
  * Configuring:
![http://uprojects.googlecode.com/files/run1s_c1.png](http://uprojects.googlecode.com/files/run1s_c1.png)
  * Base list:
![http://uprojects.googlecode.com/files/run1s_c2.png](http://uprojects.googlecode.com/files/run1s_c2.png)

---

And - the Subj: [win binary](http://uprojects.googlecode.com/files/run1s.exe)