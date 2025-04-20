from typing import List, Optional


def calculate_mms(closes: List[float], window: int) -> List[Optional[float]]:
    mms: List[Optional[float]] = []

    for i in range(len(closes)):
        if i < window - 1:
            mms.append(None)
        else:
            window_values = closes[i - window + 1 : i + 1]
            window_average = sum(window_values) / window
            mms.append(window_average)

    return mms


def calculate_incremental_mms(closes: List[float], window: int) -> Optional[float]:
    if not closes or window <= 0 or len(closes) < window:
        return None

    latest_window = closes[-window:]
    average = sum(latest_window) / window

    return round(average, 2)
