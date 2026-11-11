
import pytest

from solution import validate_server


def test_valid_server():
    server = {
        "hostname": "web-server-01",
        "cpu": "4",
        "memory": "16",
        "environment": "production"
    }

    result = validate_server(server)

    assert result["valid"] is True
    assert result["cpu"] == 4
    assert result["memory"] == 16


def test_missing_hostname():
    server = {
        "cpu": "4",
        "memory": "16",
        "environment": "production"
    }

    result = validate_server(server)

    assert result["valid"] is False
    assert any("hostname" in error for error in result["errors"])


def test_invalid_cpu():
    server = {
        "hostname": "web-server-01",
        "cpu": "invalid",
        "memory": "16",
        "environment": "production"
    }

    result = validate_server(server)

    assert result["valid"] is False


def test_zero_memory():
    server = {
        "hostname": "web-server-01",
        "cpu": "4",
        "memory": "0",
        "environment": "production"
    }

    result = validate_server(server)

    assert result["valid"] is False


def test_non_dictionary_input():
    result = validate_server(None)

    assert result["valid"] is False
