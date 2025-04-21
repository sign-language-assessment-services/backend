from unittest.mock import MagicMock, Mock, patch

from app.services import primer_service as primer_service_module
from app.services.primer_service import PrimerService, get_primer, list_primers
from tests.data.models.primers import primer_1, primer_2


@patch.object(
    primer_service_module, get_primer.__name__,
    return_value=primer_1
)
def test_get_primer_by_id(
        mocked_get_primer: MagicMock,
        primer_service: PrimerService
) -> None:
    primer_id = mocked_get_primer.return_value.id
    mocked_session = Mock()

    primer = primer_service.get_primer_by_id(mocked_session, primer_id)

    assert primer.id == primer_id
    assert primer.content == mocked_get_primer.return_value.content
    mocked_get_primer.assert_called_once_with(session=mocked_session, _id=primer_id)


@patch.object(
    primer_service_module, list_primers.__name__,
    return_value=[primer_1, primer_2]
)
def test_list_primers(
        mocked_list_primer: MagicMock,
        primer_service: PrimerService
) -> None:
    mocked_session = Mock()

    primers = primer_service.list_primers(mocked_session)

    assert len(primers) == len(mocked_list_primer.return_value)
    for result, expected in zip(primers, mocked_list_primer.return_value):
        assert result.id == expected.id
        assert result.content == expected.content
    mocked_list_primer.assert_called_once_with(session=mocked_session)
