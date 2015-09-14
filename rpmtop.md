# About #

Штука для тех, кто хочет видеть свою rpm-based-систему стройную, как серна ;-)
Т.е. – ни пакета лишнего.
Программы для вычисления лишних пакетов называют их "orphan" - т.е. "сироты". Я называю "верхними" по 2-м причинам:
  * ну какой же openoffice.org-calc сирота? Сирота - он никому не нужен. А этот - очень нужный пакет. Мне, по крайней мере.
  * когда снимаешь "верхние" пакеты - всплывают следующие (зависимые от убитых).
Есть наработки для Alt Linux и FC5/6/7/8/9, но работают не идеально:
  * показывают «верхними» (т.е. теми, от которых никто не зависит) пакеты, от которых таки кто-то зависит.
  * не показывают никому не нужные пакеты.
Не очень много, но всё равно неприятно :-(.

# Аналоги #
  * [RpmOrphan](http://rpmorphan.sourceforge.net/) - Хорошая штука, написана на Perl, но неторопливая. В основном – потому что использует не прямой досутп к базе rpm, а считывает результат “rpm -qa ...» (15” из 20).
    * DebOrphan - для deb.

# Функции #
  * показать все пакеты (быстрее, чем rpm -qa)
  * показать "верхние" пакеты
  * рекурсивный показ верхних пакетов
  * показать схему зависимостей пакетов (graphviz)

# Опции #
| Short | Long | Description |
|:------|:-----|:------------|
| -r    | --recuring 

&lt;level&gt;

 | Recursive tops (w/o level - max) |
| -a    | --all | List all rpms (or -[r0](https://code.google.com/p/uprojects/source/detail?r=0)) |
| -t    | --top | List top rpms (or [r1](https://code.google.com/p/uprojects/source/detail?r=1)+) |
| -x    | --exclude | Excluding rpms (in recuring tops) |
| -X    |      | Excluding rpms (in recuring tops) - from file |
| -o    | --output | Output filename |
| -t    | --dot | Graphiz output |
| -s    | --summary | List w/ rpm summary |
| -d    | --debug | Debug       |
| -h    | --help | Print help and exit |
| -V    | --version | Print version and exit |
| -v    | --verbose | Enable verbose mode |

надо будет добавить --use-cache

# ToDo #
  * 2-pass
  * python app to explore rpms
  * grpah:
```
digraph rpm {
        rankdir=LR;
        node [shape = box]; rpm1 rpm2 rpm3;
        node [shape = ellipse] svc1 svc2 svc3;
        subgraph sg1 {
                edge[style=dotted,dir=none];
                rpm1 -> svc1;
        }
}
```

# Bugs #
  * не все top-пакеты показывает

# Тесты #
  * P4-1.7, пакетов - 1061, Показать все пакеты и все их provides/requires
    * python-rpm: 11.5"
    * bash: 5'27.5"
  * PIII-1000, пакетов - 1087, показать все пакеты (rpm -qa):
    * py+BDB - 0.15"
    * py+rpm: 13.15"
    * c+rpm: 1.15"
    * bash+rpm: 13.56"

# Thoughts #
## Shortcuts ##
  * rpm: package
    * RS: Required Services – services, required by pkg (rpm -q --requires rpm | grep -v ^/ | gawk '{print $1}')
    * RF: Required Files – files, required by pkg (rpm -q --requires rpm | grep ^/)
    * PS: Provided Service – services, provided by pkg (rpm -q --provides rpm | gawk '{print $1}')
    * PF: Provided Files – files, provided by pkg (rpm -q --provides rpm | gawk '{print $1}')
    * 1, ?, +, 