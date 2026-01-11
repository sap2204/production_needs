"""
Модуль описывает настройки для формирования URL-адреса
для подключения к БД из переменных окружения файла .env
"""

from pathlib import Path


def load_and_read_env_file(path: Path) -> dict:
    """Функция загружает и читает файл .env с переменными окружения"""
    enviroments = {}
    try:
        if not path.exists():
            print(f'Файл .env не найден по пути: {path}')
            return {}
        with open(path, 'r') as env_file:
            for line in env_file:
                if not line:
                    continue

                if line.startswith('#'):
                    continue

                line = line.strip()
                line_list = line.split("=")
                enviroments[line_list[0]] = line_list[1]
    except FileNotFoundError:
        enviroments = {}
    return enviroments


class Settings:
    """Класс настроек, в котором формируется URL-адрес для подключения в БД"""


    env_file_path = Path(__file__).parent.parent / '.env'
    enviroments = load_and_read_env_file(env_file_path)

    @property
    def database_url(self):
        return (
                f"mssql+pyodbc://"
                f"@{self.enviroments['DB_SERVER']}/"
                f"{self.enviroments['DB_DATABASE']}?"
                f"driver={self.enviroments['DB_DRIVER']}"
                f"&trusted_connection={self.enviroments['DB_TRUSTED_CONNECTION']}"
                f"&encrypt=no"
        )

settings = Settings()




