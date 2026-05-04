import { api } from './client'

export type Brand = {
  id: number
  name: string
  description: string | null
  created_at: string
  updated_at: string
}

export async function fetchBrands(): Promise<Brand[]> {
  const { data } = await api.get('/brands')
  return data
}

export async function createBrand(payload: { name: string; description?: string }): Promise<Brand> {
  const { data } = await api.post('/brands', payload)
  return data
}
