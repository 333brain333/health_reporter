HealthReporter - класс для отправки сообщений об ошибках подсистемами посредствам Redis, которые будут обработаны мастер-службой HealthMonitor.


## Установка


1. добавьте `PyPI Index` в `pip` конфиг:
    ```bash
    pip config set global.extra-index-url \
     'https://gitlab.cognitivepilot.com/api/v4/projects/347/packages/pypi/simple'
    ```


2. Установите `cpilot-health-reporter`:
    ```bash
    pip install --upgrade cpilot-health-reporter
    ```
