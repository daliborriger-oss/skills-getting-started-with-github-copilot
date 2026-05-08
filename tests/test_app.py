import pytest
from httpx import AsyncClient
from src.app import app

import asyncio

@pytest.mark.asyncio
async def test_list_activities():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_unregister_participant():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: signup
        response_signup = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        # Assert: signup
        assert response_signup.status_code == 200
        assert f"Signed up {test_email}" in response_signup.json()["message"]

        # Act: duplicate signup
        response_dup = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        # Assert: duplicate signup
        assert response_dup.status_code == 400
        assert "already signed up" in response_dup.json()["detail"]

        # Act: unregister
        response_unreg = await ac.post(f"/activities/{activity}/unregister?email={test_email}")
        # Assert: unregister
        assert response_unreg.status_code == 200
        assert f"Removed {test_email}" in response_unreg.json()["message"]

        # Act: unregister again (should fail)
        response_unreg2 = await ac.post(f"/activities/{activity}/unregister?email={test_email}")
        # Assert: unregister again
        assert response_unreg2.status_code == 404
        assert "not registered" in response_unreg2.json()["detail"]

@pytest.mark.asyncio
async def test_signup_activity_not_found():
    # Arrange
    test_email = "nouser@mergington.edu"
    activity = "Nonexistent Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_unregister_activity_not_found():
    # Arrange
    test_email = "nouser@mergington.edu"
    activity = "Nonexistent Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity}/unregister?email={test_email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
