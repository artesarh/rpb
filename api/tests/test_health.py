import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_reports_endpoint(client):
    url = reverse("api:report-list")
    response = client.get(url)
    assert response.status_code in (200, 404)
