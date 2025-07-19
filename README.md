# 🇰🇭 Khmer Lunar Date Converter

A Python script to convert the **Gregorian date** into the **Khmer lunar calendar** — complete with lunar day (កើត/រោច), lunar month (including leap detection), zodiac animal year, heavenly stem (ស័ក), weekday in Khmer, and Buddhist year (ព.ស.).  

This project is created to support Cambodian culture and make Khmer calendar logic accessible through code.

---

## 🙏 Sponsored by Hun Vannak

> This open-source project is proudly sponsored by **Hun Vannak**, who supports the preservation of Khmer heritage through technology and innovation.

---

## ✨ Features

- Convert today's Gregorian date to Khmer lunar date
- Accurate new moon calculation for lunar day
- Detect leap months using solar longitude
- Show Khmer zodiac animal and heavenly stem
- Convert all numbers to Khmer numerals
- Output Buddhist year (ព.ស.)
- Localized Khmer weekday name

---

## 🚀 Usage

```shell
# from pypi
pip install khmerdate

# or directly from source
pip install git+https://github.com/danhhong/khmer_lunar_date.git
```

---

```python
import datetime
from khmerdate import gregorian_to_khmer_lunar, khmer_day_of_week, today

day, month, year = 1, 7, 2025

result = gregorian_to_khmer_lunar(day, month, year)
print(result)

# =>
{
    "lunar_day": "៦កើត",
    "lunar_month": "អាសាឍ",
    "lunar_year": "២៥៦៩",
    "zodiac_year": "ម្សាញ់",
    "stem": "សប្តស័ក",
}

# formatting as string
day_name = datetime.datetime(year, month, day).strftime("%A")
day_name = khmer_day_of_week[day_name]

result_fmt = f"ថ្ងៃ{day_name} {result['lunar_day']} ខែ{result['lunar_month']} ឆ្នាំ{result['zodiac_year']} {result['stem']} ព.ស. {result['lunar_year']}"

print(result_fmt)
# => ថ្ងៃអង្គារ ៦កើត ខែអាសាឍ ឆ្នាំម្សាញ់ សប្តស័ក ព.ស. ២៥៦៩

print(today())
# => ថ្ងៃសៅរ៍ ៩រោច ខែអាសាឍ ឆ្នាំម្សាញ់ សប្តស័ក ព.ស. ២៥៦៩
```