from typing import Optional
import logging


def _get(self, key: Optional[str] = None, _type: str = "utf8"):
    if not key:
        key = "*"

    val = self.rdb.get(key)
    if val and _type == "utf8":
        return val.decode("utf-8")  # type: ignore
    else:
        return val


def _set(self, key: str, value: str):
    self.rdb.set(key, value)
    logging.info(f"set {key}:{value}")


def _quit(self):
    self.rdb.close()
