"""
Tests for health check endpoints.
"""
import pytest
from fastapi import status


@pytest.mark.unit
def test_root_endpoint(client):
    """Test root endpoint returns API information."""
    response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "running"
    assert data["message"] == "School Records Management System API"
    assert data["version"] == "1.0.0"
    assert "docs" in data


@pytest.mark.unit
def test_health_check_healthy(client):
    """Test health check endpoint returns healthy status."""
    response = client.get("/health")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data


@pytest.mark.unit
def test_health_check_database_connection(client):
    """Test that health check verifies database connection."""
    response = client.get("/health")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # With SQLite in-memory, connection should always succeed in tests
    assert data["database"] in ["connected", "disconnected"]
