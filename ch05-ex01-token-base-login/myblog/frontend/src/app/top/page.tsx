"use client";

import { useEffect, useState } from "react";
import { useRouter } from 'next/navigation'

export default function Page() {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);
    const router = useRouter();

    useEffect(() => {
        const authToken = localStorage.getItem("auth_token");
        if (!authToken) {
            setError("未認証です。ログインしてください。");
            return;
        }

        const fetchUser = async () => {
            try {
                const response = await fetch("http://127.0.0.1:8000/account/user/", {
                    method: 'GET',
                    headers: {
                        Authorization: `Token ${authToken}`,
                        "Content-Type": "application/json",
                    },
                    cache: "no-store",
                });

                if (!response.ok) {
                    throw new Error("ユーザー情報を取得できませんでした。");
                }

                const userData = await response.json();
                setUser(userData);
            } catch (error) {
                setError(error.message);
            }
        };

        fetchUser();
    }, []);

    // ログアウト処理
    const handleLogout = () => {
        localStorage.removeItem("auth_token"); // トークン削除
        router.push("/account/login"); // ログインページへリダイレクト
        console.log("ログアウトしました。");
    };

    if (error) {
        return <p>{error}</p>;
    }

    if (!user) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h1>トップページ</h1>
            <button onClick={handleLogout}>
                ログアウト
            </button>

            <h1>ダッシュボード</h1>
            <p>ようこそ, {user.username} さん</p>
        </div>
    );
}
