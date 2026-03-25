# This map links AI-detected intent to your 10 physical indexes
INDEX_MAP = {
    ("SA", "Finance"): "idx-sa-finance", ("SA", "Digital"): "idx-sa-digital",
    ("NG", "Finance"): "idx-ng-finance", ("NG", "Digital"): "idx-ng-digital",
    ("KE", "Finance"): "idx-ke-finance", ("KE", "Digital"): "idx-ke-digital",
    ("UK", "Finance"): "idx-uk-finance", ("UK", "Digital"): "idx-uk-digital",
    ("US", "Finance"): "idx-us-finance", ("US", "Digital"): "idx-us-digital"
}

def get_index_from_intent(country_code, topic):
    # Default to a general index if topic is unclear
    return INDEX_MAP.get((country_code.upper(), topic.capitalize()), "idx-sa-finance")