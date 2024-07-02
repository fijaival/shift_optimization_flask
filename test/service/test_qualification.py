from api.v1.service.qualifications import delete_qualification_service
import pytest
from unittest.mock import MagicMock, patch
from test.conftest import mock_session_scope
from api.v1.service import qualifications
from api.v1.models import Qualification
from api.v1.service.qualifications import get_qualification_service, add_qualification_service, delete_qualification_service

from factory import Faker, Sequence, SubFactory, Iterator, SelfAttribute
from factory.alchemy import SQLAlchemyModelFactory


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


@pytest.fixture
def qualification_factory(session):
    class QualificationFactory(SQLAlchemyModelFactory):
        class Meta:
            model = Qualification
            sqlalchemy_session = session

        qualification_id = Sequence(lambda n: n+1)
        name = Sequence(lambda n: f'name_{n}')
        created_at = Faker('date_time_this_decade')
        updated_at = Faker('date_time_this_decade')
    return QualificationFactory


@pytest.mark.small
def test_delete_qualification_service_small(qualification_factory, monkeypatch):
    data = [
        qualification_factory(),
        qualification_factory(),
        qualification_factory(),
    ]
    assert len(data) == 3
    print(data)

    # モックセッションを作成
    mock_session = MagicMock()
    mock_query = mock_session.query.return_value

    def mock_filter_by(**kwargs):
        qualification_id = kwargs.get('qualification_id')
        return MagicMock(first=lambda: next((q for q in data if q.qualification_id == qualification_id), None))
    mock_query.filter_by.side_effect = mock_filter_by

    # モックするスコープを作成
    mock_scope = MagicMock()
    mock_scope.return_value.__enter__.return_value = mock_session

    monkeypatch.setattr('api.v1.service.qualifications.session_scope', mock_scope)

    result = delete_qualification_service(1)
    mock_session.delete.assert_called_once_with(data[0])

    # 結果の確認
    assert result is not None
    assert result.qualification_id == 1
    assert result.name == data[0].name
