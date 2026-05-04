from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None


@dataclass
class VisualRegionData:
    x: int
    y: int
    width: int
    height: int
    area: int
    relative_area: float


class RegionDetectionService:
    def detect_regions(self, image: Image.Image) -> list[VisualRegionData]:
        if cv2 is None:
            return []

        img_array = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img_area = gray.shape[0] * gray.shape[1]
        regions: list[VisualRegionData] = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = int(w * h)
            if area < max(100, int(img_area * 0.002)):
                continue
            regions.append(
                VisualRegionData(
                    x=int(x),
                    y=int(y),
                    width=int(w),
                    height=int(h),
                    area=area,
                    relative_area=round(area / img_area, 6),
                )
            )

        regions.sort(key=lambda item: item.area, reverse=True)
        return regions[:50]
