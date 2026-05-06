import { useEffect, useState } from 'react'
import { fetchAssets, uploadAssets } from './api/assets'
import { createBrand, fetchBrands, type Brand } from './api/brands'
import { AssetCardGrid } from './components/AssetCardGrid'
import { AssetTable } from './components/AssetTable'
import { Filters } from './components/Filters'
import { UploadDropzone } from './components/UploadDropzone'
import { AssetDetail } from './components/AssetDetail'
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
  const [brands, setBrands] = useState<Brand[]>([])
  const [selectedBrandId, setSelectedBrandId] = useState('')
  const [collectionName, setCollectionName] = useState('')
  const [lastCollection, setLastCollection] = useState<string | null>(null)
  const [newBrandName, setNewBrandName] = useState('')
  const [newBrandDesc, setNewBrandDesc] = useState('')
  const [errors, setErrors] = useState<{ filename: string; error: string }[]>([])
  const [warnings, setWarnings] = useState<{ filename: string; warning: string }[]>([])
  const [view, setView] = useState<'cards' | 'table'>('cards')
  const [filters, setFilters] = useState<FilterState>(initialFilters)
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null)

  const loadAssets = async () => setAssets(await fetchAssets(filters))
  const loadBrands = async () => {
    const data = await fetchBrands()
    setBrands(data)
    if (!selectedBrandId && data.length > 0) setSelectedBrandId(String(data[0].id))
  }

  const onUpload = async (files: File[]) => {
    if (!selectedBrandId) {
      setErrors([{ filename: '*', error: 'Please select a brand before uploading.' }])
      return
    }
    const result = await uploadAssets(files, selectedBrandId, collectionName || undefined)
    setErrors(result.errors)
    setWarnings(result.warnings ?? [])
    setLastCollection(result.collection?.name ?? null)
    await loadAssets()
  }

  const onCreateBrand = async () => {
    if (!newBrandName.trim()) return
    const brand = await createBrand({ name: newBrandName.trim(), description: newBrandDesc || undefined })
    setNewBrandName('')
    setNewBrandDesc('')
    await loadBrands()
    setSelectedBrandId(String(brand.id))
  }

  useEffect(() => { loadAssets() }, [filters.fileType, filters.minWidth, filters.minHeight, filters.aspectRatio, filters.animated])
  useEffect(() => { loadBrands() }, [])

  return (
    <main className="container">
      <header className="pageHeader">
        <h1>StudioBlank Asset Archive</h1>
        <p className="pageSubhead">Design Operations Visual Analysis</p>
      </header>

      <section className="brandBar">
        <div className="brandSection">
          <h3>Brand Space</h3>
          <select value={selectedBrandId} onChange={(e) => setSelectedBrandId(e.target.value)}>
            <option value="">Select brand</option>
            {brands.map((brand) => <option key={brand.id} value={brand.id}>{brand.name}</option>)}
          </select>
        </div>
        <div className="collectionSection">
          <h3>Collection</h3>
          <input placeholder="Collection title (optional)" value={collectionName} onChange={(e) => setCollectionName(e.target.value)} />
        </div>
        <div className="brandCreateInline">
          <h3>Create Brand</h3>
          <div className="brandCreateFields">
            <input placeholder="Brand name" value={newBrandName} onChange={(e) => setNewBrandName(e.target.value)} />
            <input placeholder="Description" value={newBrandDesc} onChange={(e) => setNewBrandDesc(e.target.value)} />
            <button onClick={onCreateBrand}>Create</button>
          </div>
        </div>
      </section>

      <section className="uploadStrip">
        <UploadDropzone onUpload={onUpload} />
      </section>

      {lastCollection && <p className="collectionNotice">Uploaded to collection: <strong>{lastCollection}</strong></p>}

      <section className="toolStrip">
        <h3>Archive Tools</h3>
        <Filters filters={filters} onChange={setFilters} />
        <div className="toolbar">
          <button onClick={() => setView('cards')} disabled={view === 'cards'}>Card view</button>
          <button onClick={() => setView('table')} disabled={view === 'table'}>Table view</button>
        </div>
      </section>

      {errors.length > 0 && <section className="errors"><h3>Upload errors</h3><ul>{errors.map((err, idx) => <li key={`${err.filename}-${idx}`}>{err.filename}: {err.error}</li>)}</ul></section>}
      {warnings.length > 0 && <section className="warnings"><h3>Non-fatal warnings</h3><ul>{warnings.map((warn, idx) => <li key={`${warn.filename}-${idx}`}>{warn.filename}: {warn.warning}</li>)}</ul></section>}

      <section className="archiveSection">
        <h3>Asset Archive</h3>
        {view === 'cards' ? <AssetCardGrid assets={assets} onSelectAsset={setSelectedAsset} /> : <AssetTable assets={assets} />}
      </section>

      {selectedAsset && (
        <AssetDetail asset={selectedAsset} onClose={() => setSelectedAsset(null)} />
      )}
    </main>
  )
}

export default App
