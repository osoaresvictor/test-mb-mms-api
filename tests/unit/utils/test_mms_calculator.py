from app.utils.mms_calculator import calculate_mms, calculate_incremental_mms


class TestCalculateMMS:
    def test_calculate_mms_basic(self):
        closes = [10, 20, 30, 40, 50]
        window = 3
        result = calculate_mms(closes, window)
        expected = [None, None, 20.0, 30.0, 40.0]
        assert result == expected

    def test_calculate_mms_window_1(self):
        closes = [5, 10, 15]
        result = calculate_mms(closes, 1)
        expected = [5.0, 10.0, 15.0]
        assert result == expected

    def test_calculate_mms_window_larger_than_data(self):
        closes = [1, 2]
        result = calculate_mms(closes, 5)
        expected = [None, None]
        assert result == expected

    def test_calculate_mms_with_floats(self):
        closes = [1.5, 2.5, 3.5, 4.5]
        result = calculate_mms(closes, 2)
        expected = [None, 2.0, 3.0, 4.0]
        assert result == expected


class TestCalculateIncrementalMMS:
    def test_incremental_mms_basic(self):
        closes = [10, 20, 30, 40, 50]
        result = calculate_incremental_mms(closes, 3)
        assert result == 40.0

    def test_incremental_mms_exact_window(self):
        closes = [10, 20, 30]
        result = calculate_incremental_mms(closes, 3)
        assert result == 20.0

    def test_incremental_mms_window_larger_than_data(self):
        closes = [1, 2]
        result = calculate_incremental_mms(closes, 5)
        assert result is None

    def test_incremental_mms_empty_list(self):
        result = calculate_incremental_mms([], 3)
        assert result is None

    def test_incremental_mms_zero_window(self):
        result = calculate_incremental_mms([1, 2, 3], 0)
        assert result is None

    def test_incremental_mms_with_floats(self):
        closes = [1.5, 2.5, 3.5]
        result = calculate_incremental_mms(closes, 2)
        assert result == 3.0
