import json
from typing import Any

class Config(object):
    _config = {
        'mail_host': None,
        'mail_port': None,
        'mail_user': None,
        'mail_pass': None,
        'mail_subject': 'V2Ray Traffic Report',
        'database': 'v2ray_stats.sqlite3',
        'server': '127.0.0.1:2335',
        'interval': 5,
        'debug': False
    }

    @classmethod
    def load_config(cls, config_path: str):
        """
        Load config
        :param config_path: Config path.
        """
        with open(config_path, 'r') as f:
            cls._config.update(json.load(f))


    @classmethod
    def get(cls, item):
        return cls._config[item]

    @classmethod
    def set(cls, key: str, value: Any, ignore_check: bool=False):
        """
        Set config.
        :param key: Config key
        :param value: Config value
        :param ignore_check: Set value even if value is None
        :return:
        """
        if ignore_check:
            cls._config[key] = value
        elif value is not None and key in cls._config.keys():
            cls._config[key] = value

    def __getitem__(self, item):
        return self._config[item]
