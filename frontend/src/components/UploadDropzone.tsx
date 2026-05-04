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
    <div
      className={`dropzone ${dragging ? 'dragging' : ''}`}
      onDragOver={(e) => {
        e.preventDefault()
        setDragging(true)
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={async (e) => {
        e.preventDefault()
        setDragging(false)
        await handleFiles(e.dataTransfer.files)
      }}
    >
      <input
        ref={inputRef}
        type="file"
        multiple
        accept={acceptedTypes}
        hidden
        onChange={async (e) => handleFiles(e.target.files)}
      />

      <div className="dropzoneIcon" aria-hidden="true">
        <svg width="44" height="36" viewBox="0 0 44 36" fill="none">
          <path d="M2 8H17L21 12H42V34H2V8Z" stroke="currentColor" strokeWidth="2" />
          <path d="M2 8V2H15L19 8" stroke="currentColor" strokeWidth="2" />
        </svg>
      </div>

      <p className="dropzoneLead">
        Drop files or{' '}
        <button type="button" onClick={() => inputRef.current?.click()} className="linkButton">
          browse
        </button>
      </p>

      <p className="dropzoneMeta">JPG · PNG · GIF · PDF</p>
      {uploading && <p className="dropzoneMeta">Uploading…</p>}
    </div>
  )
}
