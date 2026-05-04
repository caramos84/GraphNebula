import io

from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy import delete

from app.main import app
from app.db.database import SessionLocal
from app.models.asset import Asset
from app.models.brand import Brand
from app.models.collection import Collection


client = TestClient(app)


def _png_bytes() -> bytes:
    image = Image.new("RGB", (40, 40), color="white")
    buff = io.BytesIO()
    image.save(buff, format="PNG")
    return buff.getvalue()


def _reset_tables() -> None:
    db = SessionLocal()
    db.execute(delete(Asset))
    db.execute(delete(Collection))
    db.execute(delete(Brand))
    db.commit()
    db.close()


def test_create_brand_and_list():
    _reset_tables()
    res = client.post('/api/brands', json={'name': 'Acme', 'description': 'Test brand'})
    assert res.status_code == 200
    payload = res.json()
    assert payload['name'] == 'Acme'

    list_res = client.get('/api/brands')
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1


def test_upload_creates_collection_and_assigns_asset_brand():
    _reset_tables()
    brand = client.post('/api/brands', json={'name': 'Globex'}).json()

    files = [('files', ('sample.png', _png_bytes(), 'image/png'))]
    data = {'brand_id': str(brand['id'])}
    res = client.post('/api/assets/upload', files=files, data=data)
    assert res.status_code == 200
    payload = res.json()

    assert payload['errors'] == []
    assert len(payload['uploaded']) == 1
    assert payload['collection'] is not None
    assert payload['uploaded'][0]['brand_id'] == brand['id']
    assert payload['uploaded'][0]['collection_id'] == payload['collection']['id']

    coll_res = client.get(f"/api/brands/{brand['id']}/collections")
    assert coll_res.status_code == 200
    assert len(coll_res.json()) == 1


def test_assets_listing_still_works():
    res = client.get('/api/assets')
    assert res.status_code == 200
    assert isinstance(res.json(), list)
