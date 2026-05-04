import numpy as np
from PIL import Image, ImageDraw

import app.services.region_detection_service as region_module
from app.services.region_detection_service import RegionDetectionService


class FakeCV2:
    COLOR_RGB2GRAY = 1
    THRESH_BINARY_INV = 2
    THRESH_OTSU = 4
    RETR_EXTERNAL = 0
    CHAIN_APPROX_SIMPLE = 0

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
    def findContours(binary, _mode, _method):
        ys, xs = np.where(binary > 0)
        if len(xs) == 0:
            return [], None
        contour = np.array([[int(xs.min()), int(ys.min())], [int(xs.max()), int(ys.max())]])
        return [contour], None

    @staticmethod
    def boundingRect(contour):
        x0, y0 = contour[0]
        x1, y1 = contour[1]
        return int(x0), int(y0), int(x1 - x0 + 1), int(y1 - y0 + 1)


def test_region_detection_returns_regions(monkeypatch):
    monkeypatch.setattr(region_module, "cv2", FakeCV2)
    service = RegionDetectionService()

    image = Image.new("RGB", (200, 200), color="white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 20, 120, 120), fill="black")

    regions = service.detect_regions(image)

    assert len(regions) == 1
    assert regions[0].x <= 20
    assert regions[0].y <= 20
    assert regions[0].area > 5000
    assert regions[0].relative_area > 0.1
