import pytest
import json
from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from sqlalchemy.orm import Session
from unittest.mock import Mock, MagicMock, patch
from uuid import uuid4, UUID
from smart_solutions.app.core.config import settings
from smart_solutions.app.api.deps import get_current_user
from smart_solutions.app.tests.conftest import app
from smart_solutions.app.tests.conftest import client
from fastapi.encoders import jsonable_encoder


class TestCreateSolution:
    """Test cases for POST /solution/"""
    def setup_method(self):
        # Mock settings
        self.original_allowed_tags = getattr(settings, 'ALLOWED_TAGS', [])
        settings.ALLOWED_TAGS = ["technology", "innovation", "health", "education"]

    def teardown_method(self):
        # Restore original settings
        settings.ALLOWED_TAGS = self.original_allowed_tags

    def test_create_solution_success(self, mock_current_user, sample_solution_create):
        app.dependency_overrides[get_current_user] = lambda: mock_current_user

        response = client.post("/solution/", json=jsonable_encoder(sample_solution_create))

        print("Response JSON:", response.json())  # debug

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["name"] == "Test Solution"
        assert data["description"] == "Test Description"
        assert len(data["tags"]) == 2
        assert len(data["images"]) == 1
        assert len(data["videos"]) == 1
