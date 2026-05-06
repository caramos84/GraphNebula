import { useEffect, useMemo, useState } from 'react'
import { previewsBase } from '../api/client'
import type { Asset } from '../types/asset'

type Props = {
  asset: Asset
  onClose: () => void
}

type RadarMetrics = {
  asset_id: number
  complexity: number
  dominance: number
  density: number
  balance: number
  modularity: number
}

export function AssetDetail({ asset, onClose }: Props) {
  const [showRegions, setShowRegions] = useState(true)
  const [radar, setRadar] = useState<RadarMetrics | null>(null)

  const safeWidth = asset.width && asset.width > 0 ? asset.width : 1
  const safeHeight = asset.height && asset.height > 0 ? asset.height : 1

  useEffect(() => {
    const loadRadar = async () => {
      const response = await fetch(`http://localhost:8000/api/assets/${asset.id}/radar`)
      if (response.ok) {
        setRadar(await response.json())
      }
    }
    loadRadar()
  }, [asset.id])

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

  const radarPoints = useMemo(() => {
    if (!radar) return ''
    const values = [radar.complexity, radar.dominance, radar.density, radar.balance, radar.modularity]
    const center = 90
    const radius = 62
    return values.map((value, index) => {
      const angle = (Math.PI * 2 * index) / values.length - Math.PI / 2
      const r = radius * Math.max(0, Math.min(1, value))
      const x = center + r * Math.cos(angle)
      const y = center + r * Math.sin(angle)
      return `${x},${y}`
    }).join(' ')
  }, [radar])

  return (
    <section className="assetDetail">
      <header className="assetDetailHeader">
        <h3>Asset Detail</h3>
        <button onClick={onClose}>Close</button>
      </header>

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

      <div className="detailMeta">
        <h4>{asset.original_filename}</h4>
        <p>{asset.mime_type} · {asset.extension.toUpperCase()} · {asset.file_size} bytes</p>
        <p>{asset.width ?? '-'} x {asset.height ?? '-'} · aspect {asset.aspect_ratio ?? '-'}</p>
        <p>{asset.visual_regions.length} regions · {asset.text_blocks.length} text blocks · {asset.layout_features.length} layout features</p>
      </div>

      <div className="detailActions">
        <button onClick={() => setShowRegions((prev) => !prev)}>{showRegions ? 'Hide regions' : 'Show regions'}</button>
      </div>

      <div className="radarPanel">
        <h3>GraphRadar Metrics</h3>
        {radar ? (
          <>
            <svg viewBox="0 0 180 180" className="radarChart" role="img" aria-label="GraphRadar chart">
              <polygon points="90,20 156,65 132,145 48,145 24,65" className="radarGuide" />
              <polygon points={radarPoints} className="radarShape" />
            </svg>
            <p>complexity {radar.complexity.toFixed(2)} · dominance {radar.dominance.toFixed(2)} · density {radar.density.toFixed(2)} · balance {radar.balance.toFixed(2)} · modularity {radar.modularity.toFixed(2)}</p>
          </>
        ) : <p>Calculating metrics…</p>}
      </div>

      <div className="detailPlaceholders">
        <p>Language Stress Analysis — Coming next</p>
        <p>Heatmap Estimation — Coming next</p>
        <p>GraphRadar Metrics — Coming next</p>
      </div>
    </section>
  )
}
