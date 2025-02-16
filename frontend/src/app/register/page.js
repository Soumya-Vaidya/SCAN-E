import Link from "next/link";
export default function Page() {
    return <div>
        <h1>Hello, SCAN-E Register</h1>
        Have an account? <Link href="/login">Login here.</Link>
    </div>
  }