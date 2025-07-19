import datetime
from src import gregorian_to_khmer_lunar, khmer_day_of_week


def test_get_today_simple():
  today = datetime.datetime(2025, 7, 19)

  # Get Gregorian Date
  dd = today.day
  mm = today.month
  yyyy = today.year
  day_name = today.strftime("%A")
  day_name = khmer_day_of_week[day_name]
  result = gregorian_to_khmer_lunar(dd, mm, yyyy)
  result_fmt = f"ថ្ងៃ{day_name} {result['lunar_day']} ខែ{result['lunar_month']} ឆ្នាំ{result['zodiac_year']} {result['stem']} ព.ស. {result['lunar_year']}"

  assert result_fmt == "ថ្ងៃសៅរ៍ ៩រោច ខែអាសាឍ ឆ្នាំម្សាញ់ សប្តស័ក ព.ស. ២៥៦៩"
