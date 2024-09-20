# duplication_model


Решение команды **P2P team**

### Структура проекта

1. model.ipynb - основной код проекта
2. Lip_sync.ipynb - модель для создание реалистичного lip-sync
3. state - папка с видео


<a href="https://disk.yandex.ru/d/ukXG4UoCTT-Nbg">Ссылка на готовые видео<a/>

# Инструкция по работе с model.ipynb

1. запуск библиотек (возможно потребуется перезагрузка среды выполнения)

2. подгрузка моделей

3. выбор языка для перевевода
   
```prem_lang = 'en'```

5. загрузка видео, которое хотите перевести и пропишите его название

   
```upload_file = 'name_your_video.mp4' ```

6. далее запуск всех ячеек

7. готовый файл сохранится в самом конце

<br /><br />

# Инструкция по работе с Lip_sync.ipynb

1. Установка библиотек

2. подгрузка моделей

3. загрузите видео на, которое хотите наложить lip_sync

<h3>!!! Важно чтобы на каждом кадре видео присутсвовало лицо человека</h3>

```upload = 'name_your_video.mp4' ```

4. для корректной работы модели пройдите по вот этому пути:
   
```/content/video-retalking/third_part/GPEN/gpen_face_enhancer.py ```

и на 50 строчку добавте вот это -
```global mask_sharp```
(это ошибка в исходном коде библиотеки, а этим действием мы ее исправили)

# Пример работы


<h2> Исходное видео</h2>

https://github.com/vlyrdv/duplication_model/assets/95037700/8f663860-06d2-4246-b9ee-972f7a2f4666

<h2> Видео без lip-sync </h2>

https://github.com/vlyrdv/duplication_model/assets/95037700/98070cce-83be-4ee7-a1d9-cf0b070de700

<h2> Видео с lip-sync </h2>


https://github.com/vlyrdv/duplication_model/assets/95037700/818765a1-108d-45ae-82ba-d6252666acba



# Архитектура
![Group 6](https://github.com/vlyrdv/duplication_model/assets/95037700/0ce6d5da-be9c-4f01-9247-61931411e233)



<br>
<h2>В проекте участвовали </h2>
<h3><a href="https://github.com/vlyrdv">Урядов Валерий</a></h3>
<h3><a href="https://github.com/abrikosmna">Мокийчук Никита</a></h3>
<h3><a href="https://github.com/GermanKek-lab">Кек Герман</a></h3>
