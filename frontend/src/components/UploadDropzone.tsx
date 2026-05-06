import { useRef, useState } from 'react'

type Props = {
  onUpload: (files: File[]) => Promise<void>
}

export function UploadDropzone({ onUpload }: Props) {
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const acceptedTypes = '.jpg,.jpeg,.png,.gif,.pdf'

  const handleFiles = async (fileList: FileList | null) => {
    if (!fileList || fileList.length === 0) return
    setUploading(true)
    await onUpload(Array.from(fileList))
    setUploading(false)
  }

  return (
    <div className={`dropzone ${dragging ? 'dragging' : ''}`} onDragOver={(e) => { e.preventDefault(); setDragging(true) }} onDragLeave={() => setDragging(false)} onDrop={async (e) => { e.preventDefault(); setDragging(false); await handleFiles(e.dataTransfer.files) }}>
      <input ref={inputRef} type="file" multiple accept={acceptedTypes} hidden onChange={async (e) => handleFiles(e.target.files)} />
      <p className="dropzoneLead">Drop files or <button onClick={() => inputRef.current?.click()} className="linkButton">browse</button></p>
      <p className="dropzoneMeta">Archive formats: JPG · PNG · GIF · PDF</p>
      {uploading && <p className="dropzoneMeta">Uploading…</p>}
    </div>
  )
}
