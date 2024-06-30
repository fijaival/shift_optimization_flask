import pytest
from api.v1.models import Qualification
from api.v1.service.qualifications import get_qualification_service, add_qualification_service, delete_qualification_service
from test.conftest import mock_session_scope
from api.v1.service import qualifications


def test_delete_qualification_service(session, monkeypatch):
    qualification_name = "Qualification_1"
    qualification = Qualification(name=qualification_name)
    squalification = Qualification(name="qualification_name")
    session.add(qualification)
    session.add(squalification)
    session.commit()

    monkeypatch.setattr(qualifications, 'session_scope', lambda: mock_session_scope(session))
    result = delete_qualification_service(1)

    assert result is not None
    assert result.qualification_id == 1
    assert result.name == qualification_name

    # データベースにその資格が存在しないことを確認
    qualification_in_db = session.query(Qualification).filter_by(qualification_id=1).first()
    assert qualification_in_db is None


def test_delete_qualification_service_no_qualification(session, monkeypatch):
    qualification_id = 1

    monkeypatch.setattr(qualifications, 'session_scope', lambda: mock_session_scope(session))
    result = delete_qualification_service(qualification_id)

    assert result is None
    assert session.query(Qualification).filter_by(qualification_id=qualification_id).first() is None
