'use client';

import { FormEvent } from 'react'
import { useRouter } from 'next/navigation'


export default function LoginPage() {

    const router = useRouter()

    async function onSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault()

        const formData = new FormData(event.currentTarget);
        const formDataJson = Object.fromEntries(formData.entries());

        const response = await fetch('http://127.0.0.1:8000/account/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formDataJson),
        })

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        console.log(data.token);
        localStorage.setItem('auth_token', data.token);
        router.push("/top");
    }

    return (
        <div>
            <h1>Login</h1>

            <form onSubmit={onSubmit}>
                <label>username</label>
                <input type="text" name="username" />
                <label>password</label>
                <input type="password" name="password" />
                <button type="submit">Submit</button>
            </form>
        </div>
    )
}
