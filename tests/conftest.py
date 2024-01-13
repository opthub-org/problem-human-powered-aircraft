# MAY write SetUp and TearDown in this file
import json

import pytest


@pytest.fixture(params=["bracket", "quotation", "end-comma"])
def invalid_json_string(request):
    if request.param == "bracket":
        return "1, 2, 3, 4"

    if request.param == "quotation":
        return """{'list': [1, 2, 3, 4]}"""

    if request.param == "end-comma":
        return '{"list": [1, 2, 3, 4], "var": 5,}'


@pytest.fixture
def nan_json_string():
    return json.dumps([float("nan") for _ in range(5)])


@pytest.fixture
def null_json_string():
    return json.dumps([None for _ in range(5)])


@pytest.fixture
def inf_json_string():
    return json.dumps([float("inf") for _ in range(5)])


@pytest.fixture
def minf_json_string():
    return json.dumps([float("-inf") for _ in range(5)])


@pytest.fixture
def nonsense_input():
    out = {"hoge": "fuga", "piyo": [1, -1, 2.0, "foo", "100", {"bar": 10}]}
    return out


@pytest.fixture
def nan_input():
    return json.loads(json.dumps([float("inf") for _ in range(5)]))


@pytest.fixture
def null_input():
    return json.loads(json.dumps([None for _ in range(5)]))


@pytest.fixture
def inf_input():
    return json.loads(json.dumps([float("inf") for _ in range(5)]))


@pytest.fixture
def minf_input():
    return json.loads(json.dumps([float("-inf") for _ in range(5)]))


@pytest.fixture
def schema():
    return {}
