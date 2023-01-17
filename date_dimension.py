from datetime import timedelta, date
import calendar
import isoweek
import pandas as pd
import holidays

# global variables
DAYS_PER_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
DAYS_OF_WEEK = [
    0,
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
NAME_OF_MONTH = [
    0,
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
SUPPORTED_HOLIDAYS = [
    "Black Friday",
    "Thanksgiving",
    "Christmas Day",
    "Christmas Eve",
    "New Year's Day",
    "Cyber Monday",
]


def calculate_columns(date_key):
    """
    Takes a date_key int(YYYMMDD) and returns a tuple with the different column values.
    """

    return (
        date_key,
        full_date(date_key),
        day(date_key),
        day_of_week(date_key),
        day_of_quarter(date_key),
        day_of_year_half(date_key),
        day_of_year(date_key),
        day_num_overall(date_key),
        is_last_day_in_month(date_key),
        is_weekend(date_key),
        week(date_key),
        weekday_name(date_key),
        weekday_abbrev(date_key),
        week_of_month(date_key),
        week_num_overall(date_key),
        week_begin_date(date_key),
        week_begin_date_key(date_key),
        month(date_key),
        month_name(date_key),
        month_abbrev(date_key),
        month_of_quarter(date_key),
        month_num_overall(date_key),
        quarter(date_key),
        quarter_name(date_key),
        quarter_abbrev(date_key),
        quarter_num_overall(date_key),
        year_half(date_key),
        year_half_name(date_key),
        year_half_abbrev(date_key),
        year_half_num_overall(date_key),
        year(date_key),
        year_month(date_key),
        year_month_full(date_key),
        is_leap_year(date_key),
        is_peak_week(date_key),
        is_holiday(date_key),
        holiday_name(date_key),
    )


def date_to_key(kdate):
    """
    Takes a datetime.date and returns the date_key format: int(YYYYMMDD)
    """
    month_zero = ""
    day_zero = ""
    if kdate.month < 10:
        month_zero = "0"
    if kdate.day < 10:
        day_zero = "0"
    return int(f"{kdate.year}{month_zero}{kdate.month}{day_zero}{kdate.day}")


def key_to_date(k):
    """
    Takes a date_key and returns a datetime.date
    """
    y, m, d = ymd_int(k)
    return date(y, m, d)


def ymd_str(k):
    """
    Takes date_key d in YYYYMMDD format and returns the year, month and day as strings.
    """
    dstring = str(k)
    year = dstring[:4]
    month = dstring[4:6]
    day = dstring[6:]
    return year, month, day


def ymd_int(k):
    """
    Takes date_key d in YYYYMMDD format and returns the year, month and day as integers.
    """
    dstring = str(k)
    year = int(dstring[:4])
    month = int(dstring[4:6])
    day = int(dstring[6:])
    return year, month, day


def full_date(k):
    """
    Formatted Date | Datatype: date | Format: YYYY-MM-DD (2023-01-16)
    """
    year, month, day = ymd_str(k)
    return f"{year}-{month}-{day}"  # TODO datatype must be date


def day(k):
    """
    Day | Datatype: int | Format: 1..31 (16)
    """
    _, _, day = ymd_int(k)
    return day


def day_of_week(k):
    """
    Sequential number within the week, starting on Sunday=1 | Datatype: int | Format: 1..7 (2)
    """
    year, month, day = ymd_int(k)
    cal_day = calendar.weekday(year, month, day)
    return cal_day + 1


def day_of_quarter(k):
    """
    Sequential number within the quarter, first day of the quarter is 1 | Datatype: int | Format: 1..92 (16)
    """
    _, month, day = ymd_int(k)
    q = quarter(k)
    if q == 1:
        if month == 1:
            return day
        elif month == 2:
            return day + DAYS_PER_MONTH[1]
        elif month == 3:
            doq = day + DAYS_PER_MONTH[1] + DAYS_PER_MONTH[2]
            if is_leap_year(k):
                doq += 1
            return doq
    elif q == 2:
        if month == 4:
            return day
        elif month == 5:
            return day + DAYS_PER_MONTH[4]
        elif month == 6:
            return day + DAYS_PER_MONTH[4] + DAYS_PER_MONTH[5]
    elif q == 3:
        if month == 7:
            return day
        elif month == 8:
            return day + DAYS_PER_MONTH[7]
        elif month == 9:
            return day + DAYS_PER_MONTH[7] + DAYS_PER_MONTH[8]
    elif q == 4:
        if month == 10:
            return day
        elif month == 11:
            return day + DAYS_PER_MONTH[10]
        elif month == 12:
            return day + DAYS_PER_MONTH[10] + DAYS_PER_MONTH[11]
    else:
        raise Exception(f"Something went wrong in day_of_quarter({k})")


def day_of_year_half(k):
    """
    Sequential number within the half year, starting on Jan 1st or Jul 1st | Datatype: int | Format: 1..184 (1)
    """
    _, month, day = ymd_int(k)
    doyh = 0
    if month < 7:
        for i in range(month):
            doyh += DAYS_PER_MONTH[i]
        if is_leap_year(k):
            doyh += 1
        return doyh + day
    else:
        for i in range(month):
            if i > 6:
                doyh += DAYS_PER_MONTH[i]
            return doyh + day


def day_of_year(k):
    """
    Sequential number within the year, starting on Jan 1st | Datatype: int | Format: 1..366 (1)
    """
    _, month, day = ymd_int(k)
    doy = 0
    for i in range(month):
        doy += DAYS_PER_MONTH[i]
    if month > 2 and is_leap_year(k):
        doy += 1
    return doy + day


def day_num_overall(k):
    """
    Sequential number from 01/01/2000 | Dataype: int | Format 1.. (2138)
    """
    dno = 0
    y = year(k)
    num_years = y - 2000
    for i in range(num_years):
        cyear = y - (num_years - i)
        if is_leap_year(cyear):
            dno += 366
        else:
            dno += 365

    dno += day_of_year(k)
    return dno


def is_last_day_in_month(k):
    """
    Boolean to flag the last day of the month | Datatype: bool | Format: True..False (True)
    """
    _, month, day = ymd_int(k)
    if month == 2:
        if is_leap_year(k):
            return day == 29

    return day == DAYS_PER_MONTH[month]


def is_weekend(k):
    """
    Boolean to flag the weekend days | Datatype: bool | Format: True..False (True)
    """
    return day_of_week(k) in [6, 7]


def week(k):
    """
    Week number in the year | Datatype: int | Format: 1..53 (34)
    """
    return key_to_date(k).isocalendar().week


def weekday_name(k):
    """
    Weekday name | Datatype: str | Format: Sunday..Saturday (Wednesday)
    """
    return DAYS_OF_WEEK[day_of_week(k)]


def weekday_abbrev(k):
    """
    Weekday name for short | Datatype: str | Format: Sun..Sat (Wed)
    """
    return weekday_name(k)[:3]


def week_of_month(k):
    """
    Week number in the month | Datatype: int | Format: 1..5 (1)
    """
    year, m, d = ymd_int(k)
    month_zero = ""
    if m < 10:
        month_zero = "0"
    first_day_of_month = int(f"{year}{month_zero}{m}01")

    # if it is the first day of the month, we know it is week 1.
    if k == first_day_of_month:
        return 1

    fy, fm, fd = ymd_int(first_day_of_month)

    # find the mondays (week start)
    m1 = week_begin_date_key(first_day_of_month)
    m2 = week_begin_date_key(
        date_to_key(key_to_date(first_day_of_month) + timedelta(days=7))
    )
    m3 = week_begin_date_key(
        date_to_key(key_to_date(first_day_of_month) + timedelta(days=14))
    )
    m4 = week_begin_date_key(
        date_to_key(key_to_date(first_day_of_month) + timedelta(days=21))
    )
    m5 = week_begin_date_key(
        date_to_key(key_to_date(first_day_of_month) + timedelta(days=28))
    )

    cur = key_to_date(k)
    if cur >= key_to_date(m5):
        return 5
    elif cur >= key_to_date(m4):
        return 4
    elif cur >= key_to_date(m3):
        return 3
    elif cur >= key_to_date(m2):
        return 2
    elif cur >= key_to_date(m1):
        return 1
    else:
        raise Exception(f"Something went wrong in week_of_month({k})")


def week_num_overall(k):
    """
    Week number from 01/01/2000 | Datatype: int | Format: 1.. (120)
    """
    wno = 0
    y = year(k)
    m = month(k)
    d = day(k)
    if y == 2000 and m == 1 and (d == 1 or d == 2):
        return 1
    num_years = y - 2000
    for i in range(num_years):
        cyear = y - (num_years - i)
        wno += isoweek.Week.last_week_of_year(cyear).week
    wno += week(k)
    return wno + 1


def week_begin_date(k):
    """
    The date of the first day of the week | Datatype: date | Format: YYYY-MM-DD (2001-12-26)
    """
    return full_date(week_begin_date_key(k))  # TODO datatype must be date


def week_begin_date_key(k):
    """
    Key for the first day of the week | Dataype: int | Format: YYYYMMDD (20011226)
    """
    dow = day_of_week(k)
    month_zero = ""
    day_zero = ""
    if dow == 1:
        return k
    else:
        wbd = key_to_date(k) - timedelta(days=(dow - 1))
        if wbd.month < 10:
            month_zero = "0"
        if wbd.day < 10:
            day_zero = "0"
        return int(f"{wbd.year}{month_zero}{wbd.month}{day_zero}{wbd.day}")


def month(k):
    """
    Month number in the year | Datatype: int | Format: 1..12 (1)
    """
    _, month, _ = ymd_int(k)
    return month


def month_name(k):
    """
    Month name | Datatype: str | Format: January..December (February)
    """
    m = month(k)
    return NAME_OF_MONTH[m]


def month_abbrev(k):
    """
    Month name for short | Datatype: str | Format: Jan..Dec (Feb)
    """
    return month_name(k)[:3]


def month_of_quarter(k):
    """
    Month number in the quarter | Datatype: int | Format: 1..3 (2)
    """
    m = month(k)
    moq = m % 3
    if moq == 0:
        moq = 3
    return moq


def month_num_overall(k):
    """
    Month number from 01/01/2000 | Datatype: int | Format: 1.. (47)
    """
    mno = 0
    y = year(k)
    num_years = y - 2000
    for i in range(num_years):
        mno += 12
    mno += month(k)
    return mno


def quarter(k):
    """
    Quarter number in the year | Datatype: int | Format: 1..4 (1)
    """
    m = month(k)
    return (m - 1) // 3 + 1


def quarter_name(k):
    """
    Quarter name as Quarter # | Datatype: str | Format: Quarter 1..Quarter 4 (Quarter 1)
    """
    return f"Quarter {quarter(k)}"


def quarter_abbrev(k):
    """
    Quarter name for short, Q# | Datatype: str | Format: Q1..Q4 (Q1)
    """
    return f"Q{quarter(k)}"


def quarter_num_overall(k):
    """
    Quarter number from 01/01/2000 | Datatype: int | Format: 1.. (20)
    """
    qno = 0
    y = year(k)
    num_years = y - 2000
    for i in range(num_years):
        qno += 4
    qno += quarter(k)
    return qno


def year_half(k):
    """
    Number of the year half | Datatype: int | Format: 1..2 (1)
    """
    m = month(k)
    if m < 7:
        return 1
    else:
        return 2


def year_half_name(k):
    """
    Year half name as YYYYH# | Datatype: str | Format: 2000H1..2050H2 (2023H1)
    """
    y = year(k)
    half = year_half(k)
    return f"{y}H{half}"


def year_half_abbrev(k):
    """
    Year half for short H# | Datatype: str | Format: H1..H2 (H1)
    """
    return f"H{year_half(k)}"


def year_half_num_overall(k):
    """
    Year half number from 01/01/2000 | Datatype: int | Format: 1.. (7)
    """
    yhno = 0
    y = year(k)
    num_years = y - 2000
    for i in range(num_years):
        yhno += 2
    yhno += year_half(k)
    return yhno


def year(k):
    """
    Year | Datatype: int | Format: 2000..2050 (2023)
    """
    year, _, _ = ymd_int(k)
    return year


def year_month(k):
    """
    Date format in YYYYMM | Datatype: int | Format: 200001..205012 (202301)
    """
    year, month, _ = ymd_int(k)
    month_zero = ""
    if month < 10:
        month_zero = "0"
    return int(f"{year}{month_zero}{month}")


def year_month_full(k):
    """
    Date format in YYYY-MM | Datatype: str | Format: 2000-01..2050-12 (2023-01)
    """
    (
        year,
        month,
        _,
    ) = ymd_str(k)
    return f"{year}-{month}"


def is_leap_year(k):
    """
    Boolean for leap year | Datatype: bool | Format: True..False (False)
    """
    if len(str(k)) == 4:
        return calendar.isleap(k)
    y = year(k)
    return calendar.isleap(y)


def is_peak_week(k):
    """
    Boolean to flag peak week (Tue prior to Black Friday through to Cyber Monday) | Datatype: bool | Format: True..False (False)
    """
    cur = key_to_date(k)

    # check if it is Black Friday, Cyber Monday, or Thanksgiving.  If so, it is peak week.
    h = holiday_name(k)
    if h == "Black Friday" or h == "Cyber Monday" or h == "Thanksgiving":
        return True

    # check if black friday is within 7 days of d, if not, we know it is not peak week
    seven_range = []
    for i in range(7):
        seven_range.append(date_to_key(cur - timedelta(days=i + 1)))
        seven_range.append(date_to_key(cur + timedelta(days=i + 1)))
    which = ""
    found = False
    for i, w in enumerate(seven_range):
        if is_holiday(w) and holiday_name(w) == "Black Friday":
            found = True
            which = w
    if not found:
        return False

    # if we're here, we have found Black Friday.  Determine peak week days from there.
    begin = key_to_date(which) - timedelta(days=3)
    end = key_to_date(which) + timedelta(days=3)
    if found:
        if cur >= begin and cur <= end:
            return True
    return False


def is_holiday(k):
    cur = key_to_date(k)
    h = holidays.US()
    holiday = h.get(cur)
    if holiday in SUPPORTED_HOLIDAYS:
        return True

    # check if black friday (day after thanksgiving)
    cur -= timedelta(days=1)
    if h.get(cur) == "Thanksgiving":
        return True
    # check if cyber monday (monday after thanksgiving)
    cur -= timedelta(days=3)
    if h.get(cur) == "Thanksgiving":
        return True

    return False


def holiday_name(k):
    if is_holiday(k):
        holiday = holidays.US().get(key_to_date(k))
        if not holiday:
            cur = key_to_date(k)
            # check if black friday (day after thanksgiving)
            cur -= timedelta(days=1)
            if holiday_name(date_to_key(cur)) == "Thanksgiving":
                return "Black Friday"
            # check if cyber monday (monday after thanksgiving)
            cur -= timedelta(days=3)
            if holiday_name(date_to_key(cur)) == "Thanksgiving":
                return "Cyber Monday"
            # check if Christmas Eve (day before Christmas)
            cur = key_to_date(k)
            cur += timedelta(days=1)
            if holiday_name(date_to_key(cur)) == "Christmas Day":
                return "Christmas Eve"

            return "Not Applicable"
        else:
            return holiday
    else:
        return "Not Applicable"


def create_dataframe():
    columns = [
        "date_key",
        "full_date",
        "day",
        "day_of_week",
        "day_of_quarter",
        "day_of_year_half",
        "day_of_year",
        "day_num_overall",
        "is_last_day_in_month",
        "is_weekend",
        "week",
        "weekday_name",
        "weekday_abbrev",
        "week_of_month",
        "week_num_overall",
        "week_begin_date",
        "week_begin_date_key",
        "month",
        "month_name",
        "month_abbrev",
        "month_of_quarter",
        "month_num_overall",
        "quarter",
        "quarter_name",
        "quarter_abbrev",
        "quarter_num_overall",
        "year_half",
        "year_half_name",
        "year_half_abbrev",
        "year_half_num_overall",
        "year",
        "year_month",
        "year_month_full",
        "is_leap_year",
        "is_peak_week",
        "is_holiday",
        "holiday_name",
    ]
    data = []
    cur = key_to_date(20000101)
    while True:
        if cur.year == 2051:
            break
        d = date_to_key(cur)
        data.append(calculate_columns(d))
        cur = cur + timedelta(days=1)
    table = pd.DataFrame(data=data, columns=columns)

    return table


if __name__ == "__main__":
    table = create_dataframe()
    table.to_csv("dates.csv")
    print("Done")
