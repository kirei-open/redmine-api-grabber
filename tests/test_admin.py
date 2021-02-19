from unittest import TestCase
from fastapi.testclient import TestClient
from app.main import app

import json


client = TestClient(app)

def test_read_main_admin():
    response = client.get("/admin/", headers={"X-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZmlyc3RuYW1lIjoiYWRtaW4iLCJsYXN0bmFtZSI6InRlc3RpbmciLCJhbGFtYXQiOiJwYWRhbGFyYW5nIiwidXNlcm5hbWUiOiJhZG1pbmZhc3QiLCJleHAiOjE2MTM1NDgzNjN9.TESHsLYRHpSlKyL4onfKQgQFJWxBg1MAp-EfKYy83ZI"})
    assert response.status_code == 200

def test_read_main_admin_bad_token():
    response = client.get("/admin/", headers={"X-Token": "abc"})
    assert response.status_code == 401

