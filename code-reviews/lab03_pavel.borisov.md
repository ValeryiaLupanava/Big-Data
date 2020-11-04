## Запуск фильтрации данных и перекладка их в hive в hdfs
```shell
$ hadoop fs -cat /labs/lab03data/* | python3 cleaner.py |  hadoop fs -put - /user/dmitry.pyshkin/tmp/00000_0.txt
```

## Скрипт фильтрации cleaner.py

```python
#!/usr/bin/env python
from urllib.parse import urlparse, unquote
import re
import sys

def url2domain(url):
   try:
       a = urlparse(unquote(url.strip()))
       if (a.scheme in ['http','https']):
           b = re.search("(?:www\.)?(.*)",a.netloc).group(1)
           if b is not None:
               return str(b).strip()
           else:
               return ''
       else:
           return ''
   except:
       return ''

arr = None
uid = None 
tmstmp None
url = None
for row in sys.stdin:

        arr = row.split('\t')

        if (len(arr) != 3):
                continue

        uid, tmstmp, url = arr

        if uid == "" or url == "":
                continue

        if uid in ['_', '-'] or url in ['_', '-']:
                continue

        url = url2domain(url)

        if url == '':
        		continue

        print('{}\t{}\t{}'.format(uid,tmstmp,url))
```

## Создание таблицы для хранения фильтрованных данных

```sql
create external table dmitry_pyshkin ( uid bigint, ts float, url string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '/user/dmitry.pyshkin/dmitry_pyshkin/';
```
## Select для подсчета данных
```sql
INSERT OVERWRITE DIRECTORY 'hdfs://bd-master.newprolab.com:8020/user/dmitry.pyshkin/lab03result'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select result.uid,
       case when result.g1 > 10 then 1 else 0 end,
       case when result.g2 > 10 then 1 else 0 end,
       case when result.g3 > 10 then 1 else 0 end,
       case when result.g4 > 10 then 1 else 0 end
from
(
   select dp.uid, coalesce(c1.cnt, 0) as g1,
                  coalesce(c2.cnt, 0) as g2,
                  coalesce(c3.cnt, 0) as g3,
                  coalesce(c4.cnt, 0) as g4
   from dmitry_pyshkin dp
            left join
        (select c1.uid, count(1) as cnt
         from dmitry_pyshkin c1
         where c1.url in ('cars.ru', 'avto-russia.ru', 'bmwclub.ru')
         group by c1.uid) c1 on (dp.uid = c1.uid)
            left join
        (select c2.uid, count(1) as cnt
         from dmitry_pyshkin c2
         where c2.url in ('fastpic.ru', 'fotoshkola.net', 'bigpicture.ru')
         group by c2.uid) c2 on (dp.uid = c2.uid)
            left join
        (select c3.uid, count(1) as cnt
         from dmitry_pyshkin c3
         where c3.url in ('nirvana.fm', 'rusradio.ru', 'pop-music.ru')
         group by c3.uid) c3 on (dp.uid = c3.uid)
            left join
        (select c4.uid, count(1) as cnt
         from dmitry_pyshkin c4
         where c4.url in ('snowmobile.ru', 'nastroisam.ru', 'mobyware.ru')
         group by c4.uid) c4 on (dp.uid = c4.uid)
   group by dp.uid, coalesce(c1.cnt, 0), coalesce(c2.cnt, 0), coalesce(c3.cnt, 0), coalesce(c4.cnt, 0)
   sort by dp.uid asc
) result;
```

## Затем переносим с hdfs в локальную файловую систему
```shell
$ cat ~/lab03_users_commas.txt | tr ',' '\t' > ~/lab03_users.txt
```

### Code review by Pavel Borisov

Дмитрий, благодарю за интересное решение. Узнал для себя несколько полезных моментов. Ниже мои комменты/вопросы:  
1. Немного поменял форматирование в этом markdown документе. Обратите, пожалуйста, внимание, как можно выделять куски с кодом через, так они удобнее читаются.
2. Хотя явное определение переменных является хорошим тоном, но в python так не принято, поэтому можно опустить эту часть в коде для очистке через MR
    ```python
    arr = None
    uid = None 
    tmstmp None
    url = None
    ```
3. Также так как в python нет явных символов для разделения кода на блоки, то лучше не использовать слишком часто разделители пустые строки, особенно это не следует делать перед первой строкой после объяления блокаб например как в этом коде:
    ```python
    for row in sys.stdin:

            arr = row.split('\t')

    # Лучше так

    for row in sys.stdin:
        arr = row.split('\t')
    ```
4. Хотя мою лабу проверка тоже изначально приняла с условием `>10`, но по заданию все-таки следует использовать `>=10`
5. Мне очень понравлся Ваш SQL код, так как он выглядит лаконичнее и чище моего :). Тут пожалуй только один вопрос, почему вы использовали `coalesce()`, а не `nvl()`.