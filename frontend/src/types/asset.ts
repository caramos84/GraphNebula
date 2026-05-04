export type TextBlock = {
  text: string
  x: number
  y: number
  width: number
  height: number
  confidence: number
}

export type VisualRegion = {
  x: number
  y: number
  width: number
  height: number
  area: number
  relative_area: number
}

export type LayoutFeature = {
  source_type: string
  source_index: number
  vertical_position: string
  horizontal_position: string
  area_ratio: number
  text_density: number | null
}

export type Asset = {
  id: number
  brand_id: number | null
  collection_id: number | null
  original_filename: string
  extension: string
  mime_type: string
  file_size: number
  width: number | null
  height: number | null
  aspect_ratio: string | null
  is_animated: boolean
  page_or_frame_count: number | null
  preview_path: string | null
  text_blocks: TextBlock[]
  visual_regions: VisualRegion[]
  layout_features: LayoutFeature[]
}

export type FilterState = {
  fileType: string
  minWidth: string
  minHeight: string
  aspectRatio: string
  animated: string
}
