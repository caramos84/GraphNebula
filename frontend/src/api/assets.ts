import { api } from './client'
import type { Asset, FilterState } from '../types/asset'

export async function uploadAssets(files: File[], brandId: string, collectionName?: string): Promise<{ uploaded: Asset[]; errors: { filename: string; error: string }[]; warnings: { filename: string; warning: string }[]; collection?: { id: number; brand_id: number; name: string; type: string } | null }> {
  const form = new FormData()
  files.forEach((file) => form.append('files', file))
  form.append('brand_id', brandId)
  if (collectionName) form.append('collection_name', collectionName)
  const { data } = await api.post('/assets/upload', form)
  return data
}

export async function fetchAssets(filters: FilterState): Promise<Asset[]> {
  const params: Record<string, string> = {}

  if (filters.fileType) params.file_type = filters.fileType
  if (filters.minWidth) params.min_width = filters.minWidth
  if (filters.minHeight) params.min_height = filters.minHeight
  if (filters.aspectRatio) params.aspect_ratio = filters.aspectRatio
  if (filters.animated === 'static') params.is_animated = 'false'
  if (filters.animated === 'animated') params.is_animated = 'true'

  const { data } = await api.get('/assets', { params })
  return data
}
