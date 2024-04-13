import os
import logging
from typing import Optional


import redis
import dacite
import dacite.exceptions
from dotenv import load_dotenv

from commons.models import Config


class RedOrm:
    # def __init__(self, addr=None, password=None, port=6379, db=0) -> None:
    def __init__(self, conf: dict = {}) -> None:
        try:
            self.config = dacite.from_dict(Config, conf)
        except dacite.exceptions.MissingValueError as e:
            logging.info("credential infos are not completed, returning to default")
            self.config = dacite.from_dict(Config, self.cred)

        self.config.addr = f"{self.config.host}:{self.conf.port}"

    def get(self, key: Optional[str] = None, _type: str = 'utf8'):
        if not key:
            key = "*"
        
        val = self.rdb.get(key)
        if _type == 'utf8':
            return val.decode('utf-8')
        else:
            return val

    def set(self, key: str, value: str):
        self.rdb.set(key, value)
        logging.info(f"set {key}:{value}")

    def quit(self):
        self.rdb.close()

    @property
    def rdb(self):
        try:
            rdb = redis.Redis(
                host=self.config.addr, password=self.config.password, db=self.config.db
            )
        except Exception as e:
            logging.error("unable to connect redis", exc_info=e)

        # ping
        try:
            p = rdb.ping()
            logging.info("pingged", p)
        except BaseException:
            logging.error("unable to ping redis")

        return rdb

    @property
    def cred(self) -> dict:
        return self._read_env() or self._default_config

    def _read_env(self):
        load_dotenv()
        return {
            "Addr": os.getenv("DB_HOST"),
            "Password": os.getenv("DB_PASSWORD"),
            "DB": 0,
            "PORT": 6379,
        }

    def _default_env():
        return {"Addr": "localhost", "Password": "", "DB": 0, "PORT": 6379}
