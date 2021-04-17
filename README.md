# hackathon
Repository for hackathon

Реализовання функциональность

- Формирование Inline клавиатуры.
- Удаление Inline клавиатуры для избежания конфликтных ситуаций.
- Формирование Reply клавиатуры.
- Формирование собственной системы хранения всех input и output данных.
- Функционал взаимодействия с пользователям по средствам состояний (State) 
- Криптографическая защита уникальных величин (например, ключ к API для FastReport Cloud)
- Возможность просмотра статусов по всем отчётам.
- Возможность скачать отчёт в удобной для пользователя форме вне зависимости от времени (Пользователь может через неделю зайти в бота, запросить историю отчётов и выбрать отчёт, который ему нужен + выбрать формат отчёт и скачать его)
- Асинхронность работы бота (быстрая обработка запросов).
- Запуск бота двойным кликом по Run.cmd.

Особенность проекта в следующем: 

- Независимость от базы данных за счёт динамического получения данных.
- Независимость от серверного хранения данных (отчётов) в FastReport Cloud
- Многообразие взаимодействия бота с пользователем.
- Наличие полного описания кода + наличие описания на html благодаря автодокументации sphinx (файл запуска можно найти по \Docs\sphinx\build\html\index.html)
- Простота в эксплуатации бота
- простота в реализации обновлений и добавлении взаимодействий с другими системами/сервисами (внутри компании, так и вне компании).
- Асинхронность работы бота (быстрая обработка запросов).
- Простота в разрорачивании и запуске (запуск происходит в два клика по Run.cmd)

Основной стек технологий:

- Python
- GitHub

Среда запуска: 

1. развёртывание бота производится на windows 10.
2. требуется установлнный язык программирования Python (версия 3.5 +)
3. требуется установленные пакеты для работы бота: 

- aiogram 
- base64
- pathlib
- urllib
- os 
- typing
- sphinx_rtd_theme

Все пакеты, за исключением aiogram и sphinx_rtd_theme являются стандартными библиотеками.

Установка: 

1. Установка пакета aiogram:

pip install aiogram

2. Установка пакета sphinx_rtd_theme: 

pip install sphinx_rtd_theme

Разработчики: 

1. Погуляй Геннадий RPA
2. Халилаева Эмине






































