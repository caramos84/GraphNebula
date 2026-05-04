import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app
from app.models import asset, brand, collection, layout_feature, text_block, visual_region  # noqa: F401


def _png_bytes() -> bytes:
    image = Image.new("RGB", (40, 40), color="white")
    buff = io.BytesIO()
    image.save(buff, format="PNG")
    return buff.getvalue()


@pytest.fixture()
def client(tmp_path):
    db_file = tmp_path / "test.db"
    test_engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_create_brand_and_list(client):
    res = client.post('/api/brands', json={'name': 'Acme', 'description': 'Test brand'})
    assert res.status_code == 200
    payload = res.json()
    assert payload['name'] == 'Acme'

    list_res = client.get('/api/brands')
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1


def test_upload_creates_collection_and_assigns_asset_brand(client):
    brand_payload = client.post('/api/brands', json={'name': 'Globex'}).json()

    files = [('files', ('sample.png', _png_bytes(), 'image/png'))]
    data = {'brand_id': str(brand_payload['id'])}
    res = client.post('/api/assets/upload', files=files, data=data)
    assert res.status_code == 200
    payload = res.json()

    assert payload['errors'] == []
    assert len(payload['uploaded']) == 1
    assert payload['collection'] is not None
    assert payload['uploaded'][0]['brand_id'] == brand_payload['id']
    assert payload['uploaded'][0]['collection_id'] == payload['collection']['id']

    coll_res = client.get(f"/api/brands/{brand_payload['id']}/collections")
    assert coll_res.status_code == 200
    assert len(coll_res.json()) == 1


def test_assets_listing_still_works(client):
    res = client.get('/api/assets')
    assert res.status_code == 200
    assert isinstance(res.json(), list)
