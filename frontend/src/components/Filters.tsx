import type { FilterState } from '../types/asset'

type Props = {
  filters: FilterState
  onChange: (next: FilterState) => void
}

export function Filters({ filters, onChange }: Props) {
  return (
    <div className="filters" aria-label="Asset filters">
      <select value={filters.fileType} onChange={(e) => onChange({ ...filters, fileType: e.target.value })}>
        <option value="">Type: All</option>
        <option value=".jpg">Type: JPG</option>
        <option value=".png">Type: PNG</option>
        <option value=".gif">Type: GIF</option>
        <option value=".pdf">Type: PDF</option>
      </select>
      <input placeholder="Min width" value={filters.minWidth} onChange={(e) => onChange({ ...filters, minWidth: e.target.value })} />
      <input placeholder="Min height" value={filters.minHeight} onChange={(e) => onChange({ ...filters, minHeight: e.target.value })} />
      <input placeholder="Aspect (e.g. 1.7778)" value={filters.aspectRatio} onChange={(e) => onChange({ ...filters, aspectRatio: e.target.value })} />
      <select value={filters.animated} onChange={(e) => onChange({ ...filters, animated: e.target.value })}>
        <option value="">Motion: Any</option>
        <option value="static">Motion: Static</option>
        <option value="animated">Motion: Animated</option>
      </select>
    </div>
  )
}
