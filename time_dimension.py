def calculate_columns(time_key):
    return (
        time_key,
        full_time(time_key),
        time_string(time_key),
        time_12_full_string(time_key),
        time_12_short_string(time_key),
        time_zone(time_key),
        hour(time_key),
        hour_string(time_key),
        hour_12(time_key),
        hour_12_string(time_key),
        meridiem(time_key),
        half_hour(time_key),
        minute(time_key),
        minute_string(time_key),
        minute_code(time_key),
        minute_full_string(time_key),
        second(time_key),
        second_string(time_key),
    )


def hms_int(k):
    """
    Takes a time_key k in format HHMMSS and returns the hour, minute and seconds as integers.
    """
    k_string = str(k)
    h = int(k_string[:2])
    m = int(k_string[2:4])
    s = int(k_string[4:])

    return h, m, s


def hms_str(k):
    """
    Takes a time_key k in format HHMMSS and returns the hour, minute and seconds as strings.
    """
    k_string = str(k)
    h = k_string[:2]
    m = k_string[2:4]
    s = k_string[4:]

    return h, m, s


def full_time(k):
    """
    Formatted time | Datatype: time | Format: HH:MM:SS (10:33:00)
    """
    h, m, s = hms_str(k)
    return f"{h}:{m}:{s}"  # TODO datatype 'time'


def time_string(k):
    """
    String format of the time | Datatype: str | Format: HH:MM:SS (10:38:00)
    """
    h, m, s = hms_str(k)
    return f"{h}:{m}:{s}"


def time_12_full_string(k):
    """
    12-hour format including seconds | Datatype: str | Format: HH:MM:SS PM (10:39:00 AM)
    """
    am_pm = meridiem(k)
    h, m, s = hms_int(k)
    h_zero = ""
    m_zero = ""
    s_zero = ""
    if h > 12:
        h -= 12

    if h < 10:
        h_zero = "0"
    if m < 10:
        m_zero = "0"
    if s < 10:
        s_zero = "0"

    return f"{h_zero}{h}:{m_zero}{m}:{s_zero}{s} {am_pm}"


def time_12_short_string(k):
    """
    12-hour format | Datatype: str | Format: HH:MM PM (10:42 AM)
    """
    am_pm = meridiem(k)
    h, m, _ = hms_int(k)
    h_zero = ""
    m_zero = ""
    if h == 0:
        h = 12
    if h > 12:
        h -= 12

    if h < 10:
        h_zero = "0"
    if m < 10:
        m_zero = "0"

    return f"{h_zero}{h}:{m_zero}{m} {am_pm}"


def time_zone(k):
    """
    Time zone (Default: UTC) | Datatype: str | Format: UTC (MST)
    """
    return "UTC"


def hour(k):
    """
    Hour as a number | Datatype: int | Format: 0..23 (10)
    """
    h, _, _ = hms_int(k)
    return h


def hour_string(k):
    """
    Hour as text | Datatype: str | Format: 00..23 (10)
    """
    h, _, _ = hms_str(k)
    return h


def hour_12(k):
    """
    12-hour as a number | Datatype: int | Format: 0..12 (10)
    """
    h = hour(k)
    if h == 0:
        return 12
    if h > 12:
        return h - 12
    return h


def hour_12_string(k):
    """
    12-hour as text | Datatype: str | Format: 00..12 (10)
    """
    h_zero = ""
    h = hour_12(k)
    if h < 10:
        h_zero = "0"
    return f"{h_zero}{h}"


def meridiem(k):
    """
    AM or PM | Datatype: str | Format: AM..PM (AM)
    """
    h = hour(k)
    if h < 12:
        return "AM"
    else:
        return "PM"


def half_hour(k):
    """
    In the first 30-minutes => 1 or the second 30-minutes => 2 | Datatype: int | Format: 1..2 (2)
    """
    m = minute(k)
    if m >= 30:
        return 2
    else:
        return 1


def minute(k):
    """
    Minute as a number | Datatype: int | Format: 0..59 (53)
    """
    _, m, _ = hms_int(k)
    return m


def minute_string(k):
    """
    Minute as text | Datatype: str | Format: 00..59 (54)
    """
    _, m, _ = hms_str(k)
    return m


def minute_code(k):
    """
    Hour and minute format | Datatype: int | Format: HHMM (1055)
    """
    return int(str(k)[:4])
