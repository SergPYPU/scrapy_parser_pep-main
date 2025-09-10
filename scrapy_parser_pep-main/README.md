# scrapy\_parser\_pep — парсер PEP на Scrapy

Небольшой учебный проект, который парсит сайт [peps.python.org](https://peps.python.org) и сохраняет результаты в CSV:

* **список всех PEP** (номер, название, статус)
* **сводку по статусам** (статус → количество) + итоговая строка `Total`

## Возможности

* Обходит числовой индекс PEP и посещает страницы каждого документа
* Извлекает `number`, `name`, `status`
* Сохраняет список PEP через **Scrapy Feeds** в `results/pep_*.csv`
* Формирует сводную таблицу по статусам через **Pipeline** в `results/status_summary_*.csv`

## Технологии

* Python 3.9+
* Scrapy 2.5.1
* pytest (тесты из задания Яндекс Практикума)
* flake8 (проверка кода)

## Требования

* Python 3.9+
* Git

## Установка и запуск

```bash
# 1. Клонирование репозитория
git clone https://github.com/<ваш_логин>/scrapy_parser_pep.git
cd scrapy_parser_pep

# 2. Виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1

# 3. Зависимости
python -m pip install -r requirements.txt

# 4. Запуск паука
scrapy crawl pep
```

После запуска в каталоге `results/` появятся два CSV-файла с временной меткой:

* `pep_YYYY-MM-DDTHH-MM-SS.csv` — список PEP: столбцы `number,name,status`
* `status_summary_YYYY-MM-DD_HH-MM-SS.csv` — сводка: столбцы `Статус,Количество` + строка `Total`

> По условиям сдачи проекта на платформу оставьте в `results/` **ровно два** файла: один `pep_…` и один `status_summary_…` — **самые свежие**.

## Структура проекта

```
scrapy_parser_pep/
├─ pep_parse/
│  ├─ items.py                # описание Items (number, name, status)
│  ├─ pipelines.py            # Pipeline: формирование status_summary_*.csv
│  ├─ settings.py             # FEEDS, ITEM_PIPELINES, RESULTS_DIR
│  └─ spiders/
│     └─ pep.py               # паук: сбор ссылок и парсинг страниц PEP
├─ results/                   # сюда сохраняются CSV
├─ tests/                     # тесты Практикума
├─ requirements.txt
└─ README.md
```

## Конфигурация

Ключевые настройки в `pep_parse/settings.py`:

```python
FEEDS = {
    "results/pep_%(time)s.csv": {
        "format": "csv",
        "encoding": "utf-8",
        "fields": ["number", "name", "status"],
    }
}

ITEM_PIPELINES = {
    "pep_parse.pipelines.PepParsePipeline": 300,
}

RESULTS_DIR = "results"
```

Pipeline автоматически определяет директорию из `FEEDS` и пишет туда `status_summary_*.csv`.

## Тестирование

```bash
python -m pytest
```

Все тесты должны проходить. Если упал тест `test_files.py::test_csv_files`, проверьте, что в `results/` оставлены **ровно два** актуальных CSV.

## Полезные команды

```bash
# Показать самые свежие CSV
ls -t results/*.csv | head -n 2

# Оставить только два последних CSV в results/
ls -t results/*.csv | tail -n +3 | xargs rm
```

## Автор

**Valeriy Borovikov**
