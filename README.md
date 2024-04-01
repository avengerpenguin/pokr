# Pokr

OKR Scorecard.

## Usage

Quick example:

```python
import datetime
import pokr
from pokr.metrics import (
    baseline,
    scaled,
    google_analytics,
    goodreads,
)

START = datetime.date(year=2021, month=10, day=1)
NEXTQ = datetime.date(year=2022, month=1, day=1)

app = pokr.app(
    name="My Scorecard",
    metric_functions={
        "Reading": {
            "Books Read": baseline(goodreads("my-goodreads-id"), 35) >= scaled((6, 12), START, NEXTQ),
        },
        "Websites": {
            "Visitors": google_analytics("MY-GA-ID") >= (100, 1000),
        },
    },
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

```
