from datetime import datetime

list_of_expected_keys = [
  "location",
  "city",
  "country",
  "state",
  "is_remote",
  "willing_to_relocate",
  "technologies_used",
  "resume_link",
  "email",
  "personal_website",
  "description",
  "name",
  "title",
  "level",
  "years_of_experience",
  "capacity",
]


def clean_profile_json_object(original_comment: dict, nlp_data: dict) -> dict:
  make_sure_all_keys_exists(nlp_data, list_of_expected_keys)
  nlp_data["years_of_experience"] = check_years_of_experience_value(nlp_data['years_of_experience'], original_comment['text'])
  nlp_data["level"] = check_that_level_is_one_the_allowed_values(nlp_data['level'])
  check_boolean_value(nlp_data['is_remote'])
  check_boolean_value(nlp_data['willing_to_relocate'])

  for key, value in nlp_data.items():
      nlp_data[key] = if_value_is_unknown_return_empty_string(value)

  return nlp_data

def check_years_of_experience_value(years: int, text: str):
  """Python function to check that the estimated years of experience appears in the text."""
  if str(years) in text and isinstance(years, int):
      return years
  else:
      return None

def check_that_level_is_one_the_allowed_values(level: str) -> bool:
    if level in ["Senior", "Mid-level", "Junior", "Principal", "C-Level"]:
        return level
    else:
        return ""

def if_value_is_unknown_return_empty_string(value: str) -> str:
    if value in ["Unknown", "unknown", "empty", "not specified", "N/A"]:
        return ""
    else:
        return value

"""
options for willing to relocate + mapping
- Yes
  - Open for relocation
  - Anywhere really
  - Sure!
  - Yes, only if sponsored
  - open to discussing it
  - Can discuss
- Yes (ceratin places)
  - Within Texas
- No
  - Not in the next year
- Maybe
  - In exceptional cases
  - It depends on the position.
  - Possibly
  - Possibly
"""


def sort_dates(dates):
    """
      Sorts a list of dates in ascending order.
    """
    date_format = "%B %Y"
    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, date_format))
    return sorted_dates

def check_boolean_value(boolean_value: any) -> bool:
    if isinstance(boolean_value, bool) or boolean_value in ["True", "true", "Yes", "yes"]:
        return boolean_value
    else:
        return False

def make_sure_all_keys_exists(data: dict, keys: list) -> dict:
    for key in keys:
      try:
        data[key]
      except KeyError:
        data[key] = ""

    return data
