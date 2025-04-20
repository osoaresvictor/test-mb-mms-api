from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.services.mms_service import get_mms_data
from app.schemas.mms_schema import MMSResponse


def test_get_mms_data_cache_hit(monkeypatch):
    mock_cache = [MMSResponse(pair="BRLBTC", timestamp=123456, mms=12.34)]
    monkeypatch.setattr("app.services.mms_service.get_cache", lambda _: mock_cache)
    result = get_mms_data("BRLBTC", 123456, 123999, 20, MagicMock(spec=Session))
    assert result == mock_cache


def test_get_mms_data_cache_miss(monkeypatch):
    monkeypatch.setattr("app.services.mms_service.get_cache", lambda _: None)
    monkeypatch.setattr("app.services.mms_service.set_cache", lambda *_, **__: None)
    monkeypatch.setattr(
        "app.services.mms_service.fetch_mms_data",
        lambda *_, **__: [MMSResponse(pair="BRLBTC", timestamp=123456, mms=20.5)],
    )

    result = get_mms_data("BRLBTC", 123456, 123999, 20, MagicMock(spec=Session))
    assert len(result) == 1
    assert result[0].mms == 20.5
