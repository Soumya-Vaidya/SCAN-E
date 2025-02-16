export default function Page({ params }) {
    return <div>
        <h1>Hello, I am SCAN-E for {params.name}</h1>
        Upload a file here.
        <br></br>
        <button>Upload</button>
        </div>
}