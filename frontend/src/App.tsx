import { useEffect, useState } from 'react'
import { fetchAssets, uploadAssets } from './api/assets'
import { AssetCardGrid } from './components/AssetCardGrid'
import { AssetTable } from './components/AssetTable'
import { Filters } from './components/Filters'
import { UploadDropzone } from './components/UploadDropzone'
import type { Asset, FilterState } from './types/asset'

const initialFilters: FilterState = {
  fileType: '',
  minWidth: '',
  minHeight: '',
  aspectRatio: '',
  animated: ''
}

function App() {
  const [assets, setAssets] = useState<Asset[]>([])
  const [errors, setErrors] = useState<{ filename: string; error: string }[]>([])
  const [view, setView] = useState<'cards' | 'table'>('cards')
  const [filters, setFilters] = useState<FilterState>(initialFilters)

  const loadAssets = async () => {
    const data = await fetchAssets(filters)
    setAssets(data)
  }

  const onUpload = async (files: File[]) => {
    const result = await uploadAssets(files)
    setErrors(result.errors)
    await loadAssets()
  }

  useEffect(() => {
    loadAssets()
  }, [filters.fileType, filters.minWidth, filters.minHeight, filters.aspectRatio, filters.animated])

  return (
    <main className="container">
      <h1>DesignOps Visual Asset Catalog (Sprint 1 MVP)</h1>
      <UploadDropzone onUpload={onUpload} />

      <section>
        <h3>Filters</h3>
        <Filters filters={filters} onChange={setFilters} />
      </section>

      <section className="toolbar">
        <button onClick={() => setView('cards')} disabled={view === 'cards'}>Card view</button>
        <button onClick={() => setView('table')} disabled={view === 'table'}>Table view</button>
      </section>

      {errors.length > 0 && (
        <section className="errors">
          <h3>Upload errors</h3>
          <ul>
            {errors.map((err, idx) => <li key={`${err.filename}-${idx}`}>{err.filename}: {err.error}</li>)}
          </ul>
        </section>
      )}

      {view === 'cards' ? <AssetCardGrid assets={assets} /> : <AssetTable assets={assets} />}
    </main>
  )
}

export default App
