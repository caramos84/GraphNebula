from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.radar_metric import RadarMetric


class RadarMetricsService:
    def compute_and_persist(self, db: Session, asset: Asset) -> RadarMetric:
        existing = db.query(RadarMetric).filter(RadarMetric.asset_id == asset.id).first()
        metrics = self._compute(asset)

        if existing:
            existing.complexity = metrics["complexity"]
            existing.dominance = metrics["dominance"]
            existing.density = metrics["density"]
            existing.balance = metrics["balance"]
            existing.modularity = metrics["modularity"]
            db.commit()
            db.refresh(existing)
            return existing

        created = RadarMetric(asset_id=asset.id, **metrics)
        db.add(created)
        db.commit()
        db.refresh(created)
        return created

    def _compute(self, asset: Asset) -> dict[str, float]:
        regions = asset.visual_regions
        text_blocks = asset.text_blocks

        total_regions = max(len(regions), 1)
        total_text = len(text_blocks)
        total_layout = len(asset.layout_features)

        complexity = min(1.0, (total_regions + total_text + total_layout / 2) / 30)

        max_region_area = max((r.relative_area for r in regions), default=0.0)
        dominance = min(1.0, max_region_area * 2.5)

        text_area_ratio = sum((f.area_ratio for f in asset.layout_features if f.source_type == "text_block"), 0.0)
        density = min(1.0, (total_text / total_regions) * 0.2 + text_area_ratio)

        left = sum(1 for f in asset.layout_features if f.horizontal_position == "left")
        center = sum(1 for f in asset.layout_features if f.horizontal_position == "center")
        right = sum(1 for f in asset.layout_features if f.horizontal_position == "right")
        horiz_total = max(left + center + right, 1)
        skew = abs(left - right) / horiz_total
        balance = max(0.0, 1.0 - skew)

        modularity = min(1.0, total_regions / 12)

        return {
            "complexity": round(complexity, 4),
            "dominance": round(dominance, 4),
            "density": round(density, 4),
            "balance": round(balance, 4),
            "modularity": round(modularity, 4),
        }
