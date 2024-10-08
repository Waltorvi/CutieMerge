# CutieMerge

В данном репозитории приведены 2 версии программы, [batch](https://github.com/Waltorvi/CutieMerge/releases/tag/1.0.0) скрипт, который объединяет уже загруженные файлы, а также Python версия этого скрипта с большим количеством полезных функций.


В отличие от простого [BATCH-скрипта](https://github.com/Waltorvi/CutieMerge/releases/tag/1.0.0), [PyCutieMerge](https://github.com/Waltorvi/CutieMerge/releases) предоставляет:

- Удобный интерактивный интерфейс для выбора сезона, серии, качества видео, озвучки и субтитров.

- Автоматическую загрузку файлов с сайта.

- Возможность выбора между различными загрузчиками, включая встроенные альтернативный и многопоточный(EXP) загрузчик, а также опциональные `wget` и `aria2c`.

- Настраиваемые параметры загрузки, такие как количество потоков, таймаут, папка вывода и прочее.

- Настройки программы, которые сохраняются между запусками.

- Цветное логирование для удобного отслеживания процесса загрузки и объединения.


## Установка


### Для PyCutieMerge:


**1) Установите ffmpeg**

  - ffmpeg обязателен для работы программы. Нужен для объединения видео, аудио и субтитров в единую серию

  - Скачайте ffmpeg с официального [сайта](https://www.ffmpeg.org/)

  - Добавьте путь к папке `bin` ffmpeg в переменную окружения `Path`

**2) Скачайте [CutieMerge.exe](https://github.com/Waltorvi/CutieMerge/releases) из последнего релиза**
  
  - Перед использованием настоятельно рекомендую прочесть [инструкцию](https://github.com/Waltorvi/CutieMerge/blob/main/PyCutieMerge/README.md)

  - Перенесите CutieMerge.exe в пустую папку в любом месте вашего компьютера


#### Опционально


**3) Установите aria2**

  - Хоть и опционально, но **крайне рекомендуется**, так как этот загрузчик использует многопоточную загрузку, что ускоряет скачивание файлов, а также работает без багов.

  - Скачайте `aria2` с официального [сайта](https://github.com/aria2/aria2/releases/tag/release-1.37.0) 

    - Также можете воспользоваться консольной командой `winget install aria2.aria2`

  - Добавьте путь к `aria2` в переменную окружения `Path`

**4) Установите wget**

  - В программу уже встроен альтернативный загрзучик, не использующий многопоточную загрузку. Однако, если с ним возникают проблемы, вы можете попробовать `wget`

  - Скачайте `wget` с официального сайта

    - Также можете воспользоваться консольной командой `winget install JernejSimoncic.Wget`

  - Добавьте путь к `wget` в переменную окружения `Path`


### Для Batch скрипта:


**1) Установите ffmpeg**

  - ffmpeg обязателен для работы скрипта. Нужен для объединения видео, аудио и субтитров в единую серию

  - Скачайте ffmpeg с официального [сайта](https://www.ffmpeg.org/)

  - Добавьте путь к папке `bin` ffmpeg в переменную окружения Path. Замените путь к ffmpeg в скрипте

**2) Скачайте скрипт**

  - Скачайте CutieMerge.bat из релиза [1.0.0](https://github.com/Waltorvi/CutieMerge/releases/tag/1.0.0)

  - Также выделите под него отдлеьную папку, укажите ее в самом скрипте. В эту папку добавляйте нужные видео, аудио и субтитры
