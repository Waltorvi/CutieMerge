@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

set "FFMPEG_PATH=C:\Program Files (x86)\FFmpeg\bin"
cd /d "D:\Поняший архив"

:: Выбор файлов
call :choose_file "видео" ".webm" "video_file"
call :choose_file "аудио" ".opus" "audio_file"
call :choose_file "субтитры" ".ass" "subtitle_file"

goto after_selection

:: Функция для выбора файла
:choose_file
set "file_type=%~1"
set "file_ext=%~2"
set "var_name=%~3"

echo Выберите %file_type% файл:
set "index=1"
set "file_count=0"
for %%f in (*%file_ext%) do (
    set /a file_count+=1
    set "file[!file_count!]=%%f"
    echo !file_count!: %%f
)

if %file_count% equ 0 (
    echo Файлы с расширением %file_ext% не найдены.
    pause
    exit /b 1
)

:choose_again
set /p choice="Выберите номер %file_type% файла: "
if !choice! lss 1 set "choice=0"
if !choice! gtr %file_count% set "choice=0"
if "!file[%choice%]!"=="" (
    echo Неверный выбор. Попробуйте снова.
    goto choose_again
)
set "%var_name%=!file[%choice%]!"
echo.
goto :eof

:after_selection
:: Устанавливаем имя выходного файла (меняем расширение на mkv)
for %%f in ("%video_file%") do (
    set "base_name=%%~nf"
)
set "output_file=%base_name%_SEURKA.mkv"

:: Вывод информации о выбранных файлах и запрос подтверждения
echo.
echo Выбранные файлы:
:: Видео
echo Видео: %video_file%
:: Аудио
echo Аудио: %audio_file%
:: Субтитры
echo Субтитры: %subtitle_file%
:: Выходной файл
echo Выходной файл: %output_file%
echo.
set /p confirm="Подтвердите склеивание этих файлов (Да/Нет) [y/n]: "
if /i "%confirm%" neq "y" (
    echo Операция отменена пользователем.
    pause
    exit /b 0
)

:: Объединяем видео, аудио и (при наличии) субтитры
echo.
echo Начинаем склеивание файлов...

if defined subtitle_file (
    "%FFMPEG_PATH%\ffmpeg" -i "%video_file%" -i "%audio_file%" -i "%subtitle_file%" -c:v copy -c:a libvorbis -c:s copy -map 0:v -map 1:a -map 2 -y "%output_file%"
) else (
    "%FFMPEG_PATH%\ffmpeg" -i "%video_file%" -i "%audio_file%" -c:v copy -c:a libvorbis -y "%output_file%"
)

if %errorlevel% neq 0 (
    echo Произошла ошибка при объединении файлов.
    pause
    exit /b 1
)

echo Файлы успешно объединены.

:: Запрос на удаление исходных файлов
set /p delete_files="Удалить исходные файлы после склеивания? [y/n]: "
if /i "%delete_files%"=="y" (
    echo Удаление исходных файлов...
    del "%video_file%" "%audio_file%" "%subtitle_file%"
    if %errorlevel% neq 0 (
        echo Не удалось удалить некоторые исходные файлы.
    ) else (
        echo Исходные файлы удалены.
    )
) else (
    echo Исходные файлы сохранены.
)

pause
exit /b 0