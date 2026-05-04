import type { FilterState } from '../types/asset'

type Props = {
  filters: FilterState
  onChange: (next: FilterState) => void
}

export function Filters({ filters, onChange }: Props) {
  return (
    <div className="filters">
      <select value={filters.fileType} onChange={(e) => onChange({ ...filters, fileType: e.target.value })}>
        <option value="">All file types</option>
        <option value=".jpg">JPG</option>
        <option value=".png">PNG</option>
        <option value=".gif">GIF</option>
        <option value=".pdf">PDF</option>
      </select>
      <input placeholder="Min width" value={filters.minWidth} onChange={(e) => onChange({ ...filters, minWidth: e.target.value })} />
      <input placeholder="Min height" value={filters.minHeight} onChange={(e) => onChange({ ...filters, minHeight: e.target.value })} />
      <input placeholder="Aspect ratio (e.g. 1.7778)" value={filters.aspectRatio} onChange={(e) => onChange({ ...filters, aspectRatio: e.target.value })} />
      <select value={filters.animated} onChange={(e) => onChange({ ...filters, animated: e.target.value })}>
        <option value="">Static + Animated</option>
        <option value="static">Static</option>
        <option value="animated">Animated</option>
      </select>
    </div>
  )
}
