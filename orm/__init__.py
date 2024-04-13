import os
import logging
from typing import Optional


import dacite.dataclasses
import redis
import dacite
import dacite.exceptions
from dotenv import load_dotenv

from commons.models import Config


class RedOrm:
    debug = True

    # def __init__(self, addr=None, password=None, port=6379, db=0) -> None:
    def __init__(self, conf: dict = {}) -> None:
        print(self.cred)
        try:
            self.config = dacite.from_dict(Config, conf)

        except dacite.exceptions.MissingValueError as e:
            logging.info("credential infos are not completed, returning to default")
            self.config = dacite.from_dict(Config, self.cred)

        except dacite.dataclasses.DefaultValueNotFoundError as e:
            logging.info("credential infos are not completed, returning to default")
            self.config = dacite.from_dict(Config, self.cred)

        print("init before", self.config)

        # self.config.addr = f"{self.config.host}:{self.config.port}"

        # print('init after', self.config)

    def execute(self, cmd: str, key: str = None, val: str = None):
        print(cmd, key, val)
        try:
            if not key:
                return self.rdb.keys()

            if cmd.upper() == "SET" and key and val:
                response = self.rdb.execute_command("SET", key, val)
                if response == b"OK":
                    print("resp", response)
                    return True

            if cmd.upper() == "GET" and key:
                print("in GET key:", key)
                value = self.rdb.execute_command("GET", key)
                print("value from get", value)
                assert val == value.decode("utf-8")
                return value
        except Exception as e:
            print(e)

    def get(self, key: Optional[str] = None, _type: str = "utf8"):
        if not key:
            key = "*"

        val = self.rdb.get(key)
        if _type == "utf8":
            return val.decode("utf-8")
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
            print("conf in rdb", self.config)
            rdb = redis.Redis(
                host=self.config.host, password=self.config.password, db=self.config.db
            )
            print("connected")
        except Exception as e:
            logging.error("unable to connect redis", exc_info=e)

        # ping
        try:
            p = rdb.ping()
            logging.info("pingged", p)
            print("pingged", p)
        except BaseException:
            logging.error("unable to ping redis")

        return rdb

    @property
    def cred(self) -> dict:
        if self.debug:
            return self._default_env()
        return self._read_env()

    def _read_env(self):
        load_dotenv()
        return {
            "host": os.getenv("DB_HOST"),
            "password": os.getenv("DB_PASSWORD"),
            "db": 0,
            "port": 6379,
        }

    def _default_env(self):
        return {"host": "localhost", "password": "", "db": 0, "port": 6379}
