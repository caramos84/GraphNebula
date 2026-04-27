import { previewsBase } from '../api/client'
import type { Asset } from '../types/asset'

type Props = {
  assets: Asset[]
}

export function AssetCardGrid({ assets }: Props) {
  return (
    <div className="cardGrid">
      {assets.map((asset) => (
        <article key={asset.id} className="card">
          {asset.preview_path && <img src={`${previewsBase}${asset.preview_path}`} alt={asset.original_filename} />}
          <h4>{asset.original_filename}</h4>
          <p>{asset.extension.toUpperCase()} · {asset.mime_type}</p>
          <p>{asset.width ?? '-'} x {asset.height ?? '-'}</p>
          <p>{asset.is_animated ? 'Animated' : 'Static'} · {asset.page_or_frame_count ?? '-'} frame/page</p>
        </article>
      ))}
    </div>
  )
}
