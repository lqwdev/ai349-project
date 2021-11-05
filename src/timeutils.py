from datetime import datetime

def to_timestamp(dt: datetime) -> float:
    return datetime.timestamp(dt)

def to_datetime(ts: float) -> datetime:
    return datetime.fromtimestamp(ts).replace(tzinfo=timezoneinfo())

def timezoneinfo():
    return datetime.now().astimezone().tzinfo
