import Link from "next/link";

export default function Page() {
  return <div><h1>Hello, I am SCAN-E</h1>
    <br></br>
    <button><Link href="/register">Register</Link></button>
    <br></br>
    <button><Link href="/login">Login</Link></button>
    <br></br>
    <button><Link href="/dashboard/John">Dashboard</Link></button>
    </div>
}