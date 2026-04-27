export type Asset = {
  id: number
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
}

export type FilterState = {
  fileType: string
  minWidth: string
  minHeight: string
  aspectRatio: string
  animated: string
}
