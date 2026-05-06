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
        min_area = max(250, int(img_area * 0.01))

        boxes: list[tuple[int, int, int, int]] = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = int(w * h)
            if area < min_area:
                continue
            boxes.append((int(x), int(y), int(w), int(h)))

        merged = self._merge_nearby_boxes(boxes, gap=max(8, int(min(gray.shape) * 0.02)))

        regions: list[VisualRegionData] = []
        for x, y, w, h in merged:
            area = int(w * h)
            regions.append(
                VisualRegionData(
                    x=x,
                    y=y,
                    width=w,
                    height=h,
                    area=area,
                    relative_area=round(area / img_area, 6),
                )
            )

        regions.sort(key=lambda item: item.area, reverse=True)
        return regions[:12]

    def _merge_nearby_boxes(self, boxes: list[tuple[int, int, int, int]], gap: int) -> list[tuple[int, int, int, int]]:
        if not boxes:
            return []

        merged = boxes[:]
        changed = True
        while changed:
            changed = False
            next_boxes: list[tuple[int, int, int, int]] = []
            while merged:
                base = merged.pop(0)
                bx, by, bw, bh = base
                b_right = bx + bw
                b_bottom = by + bh

                i = 0
                while i < len(merged):
                    ox, oy, ow, oh = merged[i]
                    o_right = ox + ow
                    o_bottom = oy + oh

                    horizontal_close = not (o_right < bx - gap or ox > b_right + gap)
                    vertical_close = not (o_bottom < by - gap or oy > b_bottom + gap)

                    if horizontal_close and vertical_close:
                        bx = min(bx, ox)
                        by = min(by, oy)
                        b_right = max(b_right, o_right)
                        b_bottom = max(b_bottom, o_bottom)
                        bw = b_right - bx
                        bh = b_bottom - by
                        merged.pop(i)
                        changed = True
                    else:
                        i += 1

                next_boxes.append((bx, by, bw, bh))
            merged = next_boxes

        return merged
