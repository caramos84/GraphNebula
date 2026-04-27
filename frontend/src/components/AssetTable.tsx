import type { Asset } from '../types/asset'

type Props = {
  assets: Asset[]
}

export function AssetTable({ assets }: Props) {
  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th>Size (bytes)</th>
          <th>Dimensions</th>
          <th>Aspect Ratio</th>
          <th>Status</th>
          <th>Pages/Frames</th>
        </tr>
      </thead>
      <tbody>
        {assets.map((asset) => (
          <tr key={asset.id}>
            <td>{asset.original_filename}</td>
            <td>{asset.extension}</td>
            <td>{asset.file_size}</td>
            <td>{asset.width ?? '-'} x {asset.height ?? '-'}</td>
            <td>{asset.aspect_ratio ?? '-'}</td>
            <td>{asset.is_animated ? 'Animated' : 'Static'}</td>
            <td>{asset.page_or_frame_count ?? '-'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
