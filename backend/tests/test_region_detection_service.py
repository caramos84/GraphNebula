import numpy as np
from PIL import Image

import app.services.region_detection_service as region_module
from app.services.region_detection_service import RegionDetectionService


class FakeCV2:
    COLOR_RGB2GRAY = 1
    THRESH_BINARY_INV = 2
    THRESH_OTSU = 4
    RETR_EXTERNAL = 0
    CHAIN_APPROX_SIMPLE = 0
    contours_to_return = []

    @staticmethod
    def cvtColor(img_array, _code):
        return img_array.mean(axis=2).astype(np.uint8)

    @staticmethod
    def GaussianBlur(gray, _kernel, _sigma):
        return gray

    @staticmethod
    def threshold(gray, _thresh, _max_value, _mode):
        binary = np.where(gray < 200, 255, 0).astype(np.uint8)
        return 0, binary

    @staticmethod
    def findContours(_binary, _mode, _method):
        return FakeCV2.contours_to_return, None

    @staticmethod
    def boundingRect(contour):
        x0, y0 = contour[0]
        x1, y1 = contour[1]
        return int(x0), int(y0), int(x1 - x0 + 1), int(y1 - y0 + 1)


def contour(x0, y0, x1, y1):
    return np.array([[x0, y0], [x1, y1]])


def test_region_detection_filters_noise_and_limits(monkeypatch):
    monkeypatch.setattr(region_module, "cv2", FakeCV2)
    service = RegionDetectionService()

    # include tiny noise blocks and many larger ones
    FakeCV2.contours_to_return = [contour(0, 0, 5, 5), contour(10, 10, 16, 16)] + [
        contour(i * 12, 30, i * 12 + 20, 55) for i in range(20)
    ]

    image = Image.new("RGB", (400, 200), color="white")
    regions = service.detect_regions(image)

    assert len(regions) == 12
    assert all(r.area > 250 for r in regions)


def test_region_detection_merges_nearby_regions(monkeypatch):
    monkeypatch.setattr(region_module, "cv2", FakeCV2)
    service = RegionDetectionService()

    # two nearby boxes should merge into one larger box
    FakeCV2.contours_to_return = [
        contour(20, 20, 80, 90),
        contour(86, 24, 145, 94),
    ]

    image = Image.new("RGB", (300, 200), color="white")
    regions = service.detect_regions(image)

    assert len(regions) == 1
    assert regions[0].x <= 20
    assert regions[0].width >= 120
    assert regions[0].height >= 70
