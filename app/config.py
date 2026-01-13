"""
Модуль описывает настройки для формирования URL-адреса
для подключения к БД из переменных окружения файла .env
"""

from pathlib import Path


def load_and_read_env_file(path: Path) -> dict:
    """Функция загружает и читает файл .env с переменными окружения"""
    environments = {}
    try:
        if not path.exists():
            print(f'Файл .env не найден по пути: {path}')
            return {}
        with open(path, 'r', encoding='utf-8') as env_file:
            for line in env_file:
                if not line:
                    continue

                if line.startswith('#'):
                    continue

                line = line.strip()
                line_list = line.split("=")
                environments[line_list[0]] = line_list[1]
    except FileNotFoundError:
        environments = {}
    return environments


class Settings:
    """Класс настроек, в котором формируется URL-адрес для подключения в БД"""


    env_file_path = Path(__file__).parent.parent / '.env'
    environments = load_and_read_env_file(env_file_path)
    server = environments.get('DB_SERVER')
    db_name = environments.get('DB_NAME')
    db_driver = environments.get('DB_DRIVER')

    @property
    def database_url(self):
        """Метод формирования строки подключения к БД"""

        connection_string = (
            f"mssql+pyodbc://@{self.server}/{self.db_name}"
            f"?driver={self.db_driver}"
            "&trusted_connection=yes"
        )

        return connection_string



settings = Settings()




