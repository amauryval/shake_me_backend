import pytest


@pytest.fixture
def start_date():
    return "2000-01-06"


@pytest.fixture
def end_date():
    return "2001-01-09"


@pytest.fixture
def min_lat():
    return 39.65645604812829


@pytest.fixture
def min_lng():
    return -2.6806640625


@pytest.fixture
def max_lat():
    return 49.69606181911566


@pytest.fixture
def max_lng():
    return 12.568359375000002
