## Лаба 5. Определение принадлежности текстов к заданной тематике

### Дедлайн

⏰ 09 ноября 2020 года, 23:59.

### Задача

Имея набор текстов определенной базовой тематики и набор текстов неизвестной тематики определить, относятся ли тексты к заданной тематике или нет. В личном кабинете вам предложен список id текстов (`test_***.txt` текстов), по которым вы должны подготовить ответ.

Схожесть вакансий может использоваться в рамках content-based рекомендательной системы.

#### Обработка данных на вход

Нужные вам файлы лежат в директории на master (не на HDFS): `/data/share/lab05data/`. Файлы двух типов:

- файлы `base_*.txt` - файлы с текстом одинаковой заданной тематики;
- файлы `test_*.txt` - файлы с текстом неизвестной тематики.

`*` — id текста

Содержимым всех файлов является текст (описание вакансии), содержащий html-теги.

Пример файла:

```
<p>Приглашается Бренд-менеджер в известную компанию (сеть магазинов бытовой, видео, аудио-техники). </p><p>Требования:<br />Мужчина/женщина, <br />25-40 лет, <br />образование высшее (желательно маркетинг), <br />с опытом работы от 3 лет на позиции бренд-менеджера (в компании, занимающейся бытовой техникой или в очень крупной компании). <br />Обязательно хороший уровень английского (устный и письменный), <br />сильные навыки управления проектами. <br />Сильные презентационные навыки. <br />ПК: MS Office, Power Point – обязательно. </p><p>Обязанности: <br />продвижение бренда компании, <br />маркетинговые исследования, <br />вывод собственных брендов на рынок, <br />имиджевая реклама. </p><p>Условия:<br />Офис в центре. <br />Возможны командировки. </p>
```

#### Обработка данных на выход

**Важно**: Выходной файл должен быть расположен в корне вашей директории в файле `lab05.json`. Чекер будет брать файл именно оттуда.

Пример решения:

```
{
    “defined” : [1,3,5,7,9],
    “other” : [2,4,6,8,10]
}
```

В поле defined требуется id текстов `test_***.txt` (из тех id, что представлены в Личном кабинете), которые соответствуют заданной тематике текстов `base_***.txt`.

В поле other требуется id текстов `test_***.txt` (из тех id, что представлены в Личном кабинете), которые НЕ соответствуют заданной тематике текстов `base_***.txt`.

#### Подсказки

- Использовать косинусную меру как меру сходства.
- Так как текстов заданной тематики несколько, результирующую метрику на неизвестный текст можно получить путем сложения косинусной меры этого текста со всеми эталонными текстами. При этом сумма косинусных мер может оказаться больше единицы.
- В качестве барьера лучше использовать среднее значение полученной меры: все что выше — тексты нужной тематики, все что ниже — тексты другой тематики.

### Проверка

Проверка осуществляется автоматическим скриптом из Личного кабинета.

Лабораторная будет считаться пройденной, если метрики:

`len(TrueDefined.intersection(YourDefined))/len(YourDefined)`

`len(TrueDefined.intersection(YourDefined))/len(TrueDefined)`

будут больше 0.9.

![intersection](images/image1.png)

Первая метрика означает следующее. Возьмем пересечение множеств "true" и "yours". Посчитаем количество элементов в пересечении и поделим на количество элементов в множестве "yours".

![tex1](images/lab05_tex1.svg)

Вторая метрика означает аналогичное. Только делим на количество элементов в множестве "true".

![tex2](images/lab05_tex2.svg)
