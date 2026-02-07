"use client";

import { useAuth } from "@clerk/nextjs";

export default function TestPage() {
    const { getToken } = useAuth();

    const callProtected = async () => {
        const token = await getToken({ template: "fastapi" });


        const res = await fetch("http://localhost:8000/protected", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        const data = await res.json();
        console.log(data);
        alert(JSON.stringify(data));
    };

    return (
        <div className="p-10">
            <button
                onClick={callProtected}
                className="bg-blue-500 text-white px-6 py-2 rounded"
            >
                Call Protected API
            </button>
        </div>
    );
}
