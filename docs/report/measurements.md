# Измерения

Данные собираются автоматически workflow `Measure build times`:
3 прогона cold и 3 прогона warm, агрегируются в медиану.

## Установка зависимостей (pip install)

| Сценарий | Прогон 1 | Прогон 2 | Прогон 3 | Медиана | Ст. откл. |
|---|---|---|---|---|---|
| Cold (без кэша) | {{ measurements.cold_pip.raw[0] }} | {{ measurements.cold_pip.raw[1] }} | {{ measurements.cold_pip.raw[2] }} | {{ measurements.cold_pip.median }} | {{ measurements.cold_pip.stdev }} |
| Warm (с кэшем) | {{ measurements.warm_pip.raw[0] }} | {{ measurements.warm_pip.raw[1] }} | {{ measurements.warm_pip.raw[2] }} | {{ measurements.warm_pip.median }} | {{ measurements.warm_pip.stdev }} |

**Выигрыш:** {{ measurements.cold_pip.median - measurements.warm_pip.median }} сек
({{ measurements.cold_pip.median | percent_saved(measurements.warm_pip.median) }}%).

## Сборка сайта (mkdocs build --strict)

| Сценарий | Прогон 1 | Прогон 2 | Прогон 3 | Медиана | Ст. откл. |
|---|---|---|---|---|---|
| Cold | {{ measurements.cold_build.raw[0] }} | {{ measurements.cold_build.raw[1] }} | {{ measurements.cold_build.raw[2] }} | {{ measurements.cold_build.median }} | {{ measurements.cold_build.stdev }} |
| Warm | {{ measurements.warm_build.raw[0] }} | {{ measurements.warm_build.raw[1] }} | {{ measurements.warm_build.raw[2] }} | {{ measurements.warm_build.median }} | {{ measurements.warm_build.stdev }} |

## Размер сайта

| Метрика | Значение |
|---|---|
| Размер `site/` | {{ measurements.site_size_kb.median }} КБ |
| Количество файлов | {{ measurements.site_files.median }} |