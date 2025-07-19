"""
References:
Jean Meeus, Astronomical Algorithms, Willmann-Bell, 2nd edition, 1998
U.S. Naval Observatory: Explanatory Supplement to the Astronomical Almanac
NASA’s lunar phase algorithm notes, sometimes used in calendars and software
Author: Danh Hong (danhhong@gmail.com)
Date: 7/16/2025
"""

import datetime
import math

khmer_day_string = {
  "1": "១កើត",
  "2": "២កើត",
  "3": "៣កើត",
  "4": "៤កើត",
  "5": "៥កើត",
  "6": "៦កើត",
  "7": "៧កើត",
  "8": "៨កើត",
  "9": "៩កើត",
  "10": "១០កើត",
  "11": "១១កើត",
  "12": "១២កើត",
  "13": "១៣កើត",
  "14": "១៤កើត",
  "15": "១៥កើត",
  "16": "១រោច",
  "17": "២រោច",
  "18": "៣រោច",
  "19": "៤រោច",
  "20": "៥រោច",
  "21": "៦រោច",
  "22": "៧រោច",
  "23": "៨រោច",
  "24": "៩រោច",
  "25": "១០រោច",
  "26": "១១រោច",
  "27": "១២រោច",
  "28": "១៣រោច",
  "29": "១៤រោច",
  "30": "១៥រោច",
}

khmer_day_of_week = {
  "Monday": "ចន្ទ",
  "Tuesday": "អង្គារ",
  "Wednesday": "ពុធ",
  "Thursday": "ព្រហស្បតិ៍",
  "Friday": "សុក្រ",
  "Saturday": "សៅរ៍",
  "Sunday": "អាទិត្យ",
}

khmer_digits = {
  "0": "០",
  "1": "១",
  "2": "២",
  "3": "៣",
  "4": "៤",
  "5": "៥",
  "6": "៦",
  "7": "៧",
  "8": "៨",
  "9": "៩",
}


def replace_all(text, dic):
  for i, j in dic.items():
    text = text.replace(i, j)
  return text


# Khmer month names (1-based index, 1=ចេត្រ, 2=ពិសាខ, etc.)
KHMER_MONTHS = [
  "ចេត្រ",
  "ពិសាខ",
  "ជេស្ឋ",
  "អាសាឍ",
  "ស្រាពណ៍",
  "ភទ្របទ",
  "អស្សុជ",
  "កត្តិក",
  "មិគសិរ",
  "បុស្ស",
  "មាឃ",
  "ផល្គុន",
]

# Khmer zodiac animals (12-year cycle, 0=ជូត, 1=ឆ្លូវ, etc.)
KHMER_ZODIAC = [
  "ជូត",
  "ឆ្លូវ",
  "ខាល",
  "ថោះ",
  "រោង",
  "ម្សាញ់",
  "មមី",
  "មមែ",
  "វក",
  "រកា",
  "ច",
  "កុរ",
]

# Khmer heavenly stems (10-year cycle, 0=ឯកស័ក, 1=ទោស័ក, etc.)
KHMER_STEMS = [
  "ឯកស័ក",
  "ទោស័ក",
  "ត្រីស័ក",
  "ចត្វាស័ក",
  "បញ្ចស័ក",
  "ឆស័ក",
  "សប្តស័ក",
  "អដ្ឋស័ក",
  "នព្វស័ក",
  "សំរឹទ្ធិស័ក",
]


# Validate Gregorian date
def is_valid_date(day, month, year):
  if not (1 <= month <= 12):
    return False
  if year < 1:
    return False
  days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
    days_in_month[1] = 29
  if not (1 <= day <= days_in_month[month - 1]):
    return False
  return True


# Convert Gregorian date to Julian Day Number (JDN)
def gregorian_to_jd(day, month, year):
  a = (14 - month) // 12
  y = year + 4800 - a
  m = month + 12 * a - 3
  jd = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
  return jd


# Calculate the mean lunar month (synodic month, ~29.530588853 days)
def get_new_moon_day(k, timezone=7.0):
  T = k / 1236.85
  JDE = (
    2451550.09766
    + 29.530588861 * k
    + 0.00015437 * T**2
    - 0.000000150 * T**3
    + 0.00000000073 * T**4
  )
  JDE += timezone / 24.0
  return math.floor(JDE + 0.5)


# Calculate solar longitude for a given JDN
def get_sun_longitude(jd):
  T = (jd - 2451545.0) / 36525.0
  L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T**2
  M = 357.52911 + 35999.05029 * T - 0.0001537 * T**2
  M = math.radians(M)
  C = (
    (1.914602 - 0.004817 * T - 0.000014 * T**2) * math.sin(M)
    + (0.019993 - 0.000101 * T) * math.sin(2 * M)
    + 0.000289 * math.sin(3 * M)
  )
  solar_long = (L0 + C) % 360
  return solar_long


# Determine if a lunar month is a leap month
def is_leap_month(jd_start, jd_end):
  long_start = get_sun_longitude(jd_start)
  long_end = get_sun_longitude(jd_end)
  for i in range(12):
    term = i * 30.0
    if (long_start <= term < long_end) or (
      long_end < long_start and (long_start <= term or term < long_end)
    ):
      return False
  return True


# Calculate Khmer zodiac year
def get_khmer_zodiac_year(lunar_year):
  return KHMER_ZODIAC[(lunar_year - 2020) % 12]


# Calculate Khmer heavenly stem
def get_khmer_stem(year):
  return KHMER_STEMS[(year - 2019) % 10]


# Convert Gregorian date to Khmer lunar date
def gregorian_to_khmer_lunar(day, month, year):
  if not is_valid_date(day, month, year):
    raise ValueError("Invalid Gregorian date")

  # Convert to JDN
  jd = gregorian_to_jd(day, month, year)

  # Find the nearest new moon
  k = math.floor((jd - 2451545.0) / 29.530588853)
  new_moon_jd = get_new_moon_day(k)

  if new_moon_jd > jd:
    k -= 1
    new_moon_jd = get_new_moon_day(k)
  elif get_new_moon_day(k + 1) <= jd:
    k += 1
    new_moon_jd = get_new_moon_day(k)

  lunar_day = jd - new_moon_jd + 1
  if lunar_day < 1:
    k -= 1
    new_moon_jd = get_new_moon_day(k)
    lunar_day = jd - new_moon_jd + 1

  # Determine lunar month and year
  # Use April 14 (approximate Khmer New Year) as reference
  ref_year = year if month > 4 or (month == 4 and day >= 14) else year - 1
  jd_ref = gregorian_to_jd(14, 4, ref_year)
  k_ref = math.floor((jd_ref - 2451545.0) / 29.530588853)

  month_count = 0
  current_k = k_ref
  current_new_moon = get_new_moon_day(current_k)
  while current_new_moon <= new_moon_jd:
    month_count += 1
    current_k += 1
    current_new_moon = get_new_moon_day(current_k)

  # Adjust for leap months
  is_leap = False
  k_start = k_ref
  temp_month_count = 0
  for i in range(month_count + 1):
    month_start = get_new_moon_day(k_start + i)
    month_end = get_new_moon_day(k_start + i + 1)
    if is_leap_month(month_start, month_end):
      if i < month_count:
        temp_month_count += 1
      else:
        is_leap = True
    temp_month_count += 1

  lunar_month = (month_count - 1) % 12 + 1
  lunar_year = year + 544 if month > 4 or (month == 4 and day >= 14) else year + 543

  month_name = KHMER_MONTHS[lunar_month - 1]
  if is_leap:
    month_name += " (Leap)"

  zodiac_year = get_khmer_zodiac_year(year)
  stem = get_khmer_stem(year)

  lunar_year = replace_all(str(lunar_year), khmer_digits)

  return {
    "lunar_day": khmer_day_string[str(lunar_day)],
    "lunar_month": month_name,
    "lunar_year": lunar_year,
    "zodiac_year": zodiac_year,
    "stem": stem,
  }


def today():
  date = datetime.datetime.today()
  dd = date.day
  mm = date.month
  yyyy = date.year
  day_name = date.strftime("%A")
  day_name = khmer_day_of_week[day_name]
  result = gregorian_to_khmer_lunar(dd, mm, yyyy)
  return f"ថ្ងៃ{day_name} {result['lunar_day']} ខែ{result['lunar_month']} ឆ្នាំ{result['zodiac_year']} {result['stem']} ព.ស. {result['lunar_year']}"
