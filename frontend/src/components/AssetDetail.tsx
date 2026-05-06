import { useMemo, useState } from 'react'
import { previewsBase } from '../api/client'
import type { Asset } from '../types/asset'

type Props = {
  asset: Asset
  onClose: () => void
}

export function AssetDetail({ asset, onClose }: Props) {
  const [showRegions, setShowRegions] = useState(true)

  const safeWidth = asset.width && asset.width > 0 ? asset.width : 1
  const safeHeight = asset.height && asset.height > 0 ? asset.height : 1

  const overlayRegions = useMemo(
    () => asset.visual_regions.map((region, index) => ({
      id: `${asset.id}-${index}`,
      left: `${(region.x / safeWidth) * 100}%`,
      top: `${(region.y / safeHeight) * 100}%`,
      width: `${(region.width / safeWidth) * 100}%`,
      height: `${(region.height / safeHeight) * 100}%`
    })),
    [asset.id, asset.visual_regions, safeWidth, safeHeight]
  )

  return (
    <section className="assetDetail">
      <header className="assetDetailHeader">
        <h3>Asset Detail</h3>
        <button onClick={onClose}>Close</button>
      </header>

      <div className="assetDetailLayout">
        <div className="detailPreviewWrap">
          <div className="detailPreviewCanvas" style={{ aspectRatio: `${safeWidth} / ${safeHeight}` }}>
            {asset.preview_path && <img src={`${previewsBase}${asset.preview_path}`} alt={asset.original_filename} className="detailPreviewImage" />}
            {showRegions && overlayRegions.map((box) => (
              <div
                key={box.id}
                className="regionOverlayBox"
                style={{ left: box.left, top: box.top, width: box.width, height: box.height }}
              />
            ))}
          </div>
        </div>

        <aside className="detailPanel">
          <div className="detailMeta">
            <h4>{asset.original_filename}</h4>
            <p>{asset.mime_type} · {asset.extension.toUpperCase()} · {asset.file_size} bytes</p>
            <p>{asset.width ?? '-'} x {asset.height ?? '-'} · aspect {asset.aspect_ratio ?? '-'}</p>
            <p>{asset.visual_regions.length} regions · {asset.text_blocks.length} text blocks · {asset.layout_features.length} layout features</p>
          </div>

          <div className="detailActions">
            <button onClick={() => setShowRegions((prev) => !prev)}>{showRegions ? 'Hide regions' : 'Show regions'}</button>
          </div>

          <div className="detailPlaceholders">
            <p>Language Stress Analysis — Coming next</p>
            <p>Heatmap Estimation — Coming next</p>
          </div>
        </aside>
      </div>
    </section>
  )
}
