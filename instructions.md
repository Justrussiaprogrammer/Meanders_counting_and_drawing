# Программа "Покраска матрицы меандров"

## Содержание

1. [Инструкция](#инструкция-по-работе-с-программой-покраски-матрицы-меандров)
   1. [Подготовка программы](#подготовка-программы)
   2. [Начало работы](#начало-работы)
   3. [Проверка последовательности](#проверка-последовательности)
2. [Нюансы работы](#нюансы-работы-покраски)

## Инструкция по работе с программой покраски матрицы меандров

### Подготовка программы

1. Разархивируйте файл game.zip
2. Откройте получившуюся папку
3. Два рза нажмите на файл main.exe
4. Модуль активируется и откроется окно с вводом размера нужного вам меандра. Можно начинать эксперименты

### Начало работы

1. В окно ввода вбейте нужный размер меандра - целое четное число
2. Для активации работы покраски нажмите Enter или кнопку OK
3. Откроется окно с матрицей инверсий, изначально пустая. Показывается матрица выше главной диагонали, окно можно
увеличить или двигать с помощью ползунков по вертикали или горизонтали. Есть 3 кнопки - "Сгенерировать", "Завершить",
"Инверсия матрицы"
   1. При нажатии кнопки "Завершить" программа завершит свою работу

### Проверка последовательности

1. Чтобы создать инверсию, нужно нажать на соответствующую кнопку в нужном столбце и строке. Номер столбца и номер
строки совпадает с нужными номерами позиций пересечений. Каждое прожатие меняет цвет кнопки, если она белая - инверсии
нет, если черная - инверсия есть
   1. При нажатии кнопки "Инверсия матрицы" каждая кнопка меняет свое состояние 
2. После составления полной карты из нужных инверсий нужно нажать кнопку "Сгенерировать". 
   1. Если составленная матрица не является меандром, появится сообщение "Это не меандр!". В таком случае нужно нажать
   кнопку "OK" и попробовать составить меандр заново.
   2. Если составленная матрица является меандром, появится изображение размеченного меандра. Для продолжения работы
   есть 3 варианта - кнопки "Продолжить", "Начать сначала", "Завершить".
      1. Кнопка "Продолжить" запускает новое пустое окно из состояния на момент старта
      [проверки последовательности](#проверка-последовательности)
      2. Кнопка "Начать сначала" открывает окно состояния [начала работы](#начало-работы)
      3. Кнопка "Завершить" завершит работу программы

## Нюансы работы покраски

- В случае работы с большими размерами меандров программа может тратить большие объемы времени на расчеты 
- При запуске нового окна кнопки могут быть не видны, в таком случае нужно развернуть окно в полноэкранный режим
