import pytest
from financial import find


@pytest.fixture
def valid_html():
    return """
    <div class="row">
        <div class="column sticky">
            <div class="rowTitle" title="Total Revenue">Total Revenue</div>
        </div>
        <div class="column">123</div>
        <div class="column">456</div>
        <div class="column">789</div>
    </div>
    """


@pytest.fixture
def no_data_html():
    return '<div class="noData">No data available for this ticker</div>'


@pytest.fixture
def broken_html():
    return '<div title="Total Revenue">Total Revenue</div>'


def test_returns_tuple_on_valid_data(valid_html):
    result = find(valid_html, "Total Revenue")
    assert isinstance(result, tuple)
    assert len(result) >= 3
    assert result[0] == "Total Revenue"

    values = result[1:]
    assert len(values) >= 2
    assert all(
        isinstance(v, str) and v.strip() and v.replace(",", "").replace(".", "").isdigit()
        for v in values
    )


def test_raises_exception_on_invalid_ticker(no_data_html):
    with pytest.raises(Exception, match="Ticker not found"):
        find(no_data_html, "Total Revenue")


def test_raises_exception_on_broken_structure(broken_html):
    with pytest.raises(Exception, match="Field of the table as arguments not found"):
        find(broken_html, "Total Revenue")