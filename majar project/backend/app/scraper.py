"""Safe demo-first review source.

A live Selenium adapter can be added for a permitted site, but the app never
bypasses authentication, CAPTCHA, or anti-bot controls.
"""

from datetime import date, timedelta

SAMPLE_REVIEWS = {
    "iphone 15": [
        ("Amazing phone with a bright display and excellent camera.", 5),
        ("Battery life is good and the phone feels very smooth.", 5),
        ("The design is nice, but the price is too high.", 3),
        ("Camera quality is disappointing in low light.", 2),
    ],
    "samsung galaxy s24": [("Fast, beautiful screen and great photos.", 5), ("The battery drains quickly.", 2), ("A solid phone for daily use.", 4), ("Good features but the software has bugs.", 3)],
    "oneplus 12": [("Very fast performance and fantastic value.", 5), ("The camera is only average.", 3), ("I love the battery and charging speed.", 5), ("Some apps crash unexpectedly.", 2)],
    "dell laptop": [("Reliable laptop with a comfortable keyboard.", 5), ("The fan is noisy under load.", 3), ("Screen quality is excellent.", 4), ("It stopped working after a week.", 1)],
    "sony headphones": [("Clear sound and comfortable for long flights.", 5), ("Noise cancellation is impressive.", 5), ("The ear cups get warm.", 3), ("Connection drops sometimes.", 2)],
}


def get_reviews(product):
    key = product.lower()
    selected = SAMPLE_REVIEWS.get(key)
    if selected is None:
        selected = [("Useful product with good overall quality.", 4), ("It works as expected, though the value could be better.", 3), ("Very happy with this purchase.", 5), ("The experience has some frustrating issues.", 2)]
    today = date.today()
    return [{"review": text, "rating": rating, "date": str(today - timedelta(days=index * 3))} for index, (text, rating) in enumerate(selected * 5)]
