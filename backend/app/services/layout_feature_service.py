from __future__ import annotations

from dataclasses import dataclass

from app.services.ocr_service import OCRBlock
from app.services.region_detection_service import VisualRegionData


@dataclass
class LayoutFeatureData:
    source_type: str
    source_index: int
    vertical_position: str
    horizontal_position: str
    area_ratio: float
    text_density: float | None


class LayoutFeatureService:
    def compute_for_text_blocks(self, blocks: list[OCRBlock], canvas_width: int, canvas_height: int) -> list[LayoutFeatureData]:
        features: list[LayoutFeatureData] = []
        canvas_area = max(canvas_width * canvas_height, 1)

        for idx, block in enumerate(blocks):
            area = max(block.width * block.height, 1)
            features.append(
                LayoutFeatureData(
                    source_type="text_block",
                    source_index=idx,
                    vertical_position=self._vertical_position(block.y + block.height / 2, canvas_height),
                    horizontal_position=self._horizontal_position(block.x + block.width / 2, canvas_width),
                    area_ratio=round(area / canvas_area, 6),
                    text_density=round(len(block.text) / area, 6),
                )
            )

        return features

    def compute_for_regions(self, regions: list[VisualRegionData], canvas_width: int, canvas_height: int) -> list[LayoutFeatureData]:
        features: list[LayoutFeatureData] = []
        canvas_area = max(canvas_width * canvas_height, 1)

        for idx, region in enumerate(regions):
            features.append(
                LayoutFeatureData(
                    source_type="visual_region",
                    source_index=idx,
                    vertical_position=self._vertical_position(region.y + region.height / 2, canvas_height),
                    horizontal_position=self._horizontal_position(region.x + region.width / 2, canvas_width),
                    area_ratio=round(region.area / canvas_area, 6),
                    text_density=None,
                )
            )

        return features

    def _vertical_position(self, center_y: float, canvas_height: int) -> str:
        if center_y < canvas_height / 3:
            return "top"
        if center_y < (2 * canvas_height) / 3:
            return "middle"
        return "bottom"

    def _horizontal_position(self, center_x: float, canvas_width: int) -> str:
        if center_x < canvas_width / 3:
            return "left"
        if center_x < (2 * canvas_width) / 3:
            return "center"
        return "right"
