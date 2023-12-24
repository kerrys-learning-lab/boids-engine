import datetime
import flask
import json
import json.encoder
import random
from .event_bus import *

COMPACT_SEPARATORS = (",", ":")


def to_json(obj, **kwargs):
    try:
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, set):
            return json.dumps(list(obj), separators=COMPACT_SEPARATORS, default=to_json)
        if isinstance(obj, dict):
            return json.dumps(obj, separators=COMPACT_SEPARATORS, default=to_json)

        return obj.to_json()
    except AttributeError:
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )


class CustomJSON(flask.json.provider.JSONProvider):
    def __init__(self, app):
        super().__init__(app)

    def dumps(self, obj, **kwargs):
        return to_json(obj, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s)


class Range:
    def __init__(self, **kwargs):
        self._min = kwargs["min"]
        self._max = kwargs["max"]

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Range):
            return self.min == other.min and self.max == other.max
        return False

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as ex:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(key)

    def __iter__(self):
        return self.__dict__.__iter__()

    def random(self, allow_negative=False):
        return random.randint(-self.min if allow_negative else self.min, self.max)

    def to_json(self):
        return {"min": self._min, "max": self._max}
