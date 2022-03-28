from datetime import timezone


def utc_to_local_time(utc_datetime):
    return utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)


def datetime_to_local_string(dt) -> str:
    return dt.strftime("%d. %m. %Y %H:%M:%S")


def datetime_to_iso_string(dt) -> str:
    return dt.isoformat()
