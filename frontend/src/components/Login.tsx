"use client";

import React, { useState } from "react";
import { useAuth } from "../lib/auth";

export function Login() {
    const { login } = useAuth();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const success = login(username, password);
        if (!success) {
            setError("Invalid credentials. Try 'user' / 'password'.");
        }
    };

    return (
        <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[var(--surface)] p-6">
            <div className="pointer-events-none absolute left-0 top-0 h-[600px] w-[600px] -translate-x-1/3 -translate-y-1/3 rounded-full bg-[radial-gradient(circle,_rgba(32,157,215,0.25)_0%,_rgba(32,157,215,0.05)_55%,_transparent_70%)]" />
            <div className="pointer-events-none absolute bottom-0 right-0 h-[600px] w-[600px] translate-x-1/4 translate-y-1/4 rounded-full bg-[radial-gradient(circle,_rgba(117,57,145,0.18)_0%,_rgba(117,57,145,0.05)_55%,_transparent_75%)]" />

            <div className="relative z-10 w-full max-w-md rounded-[32px] border border-[var(--stroke)] bg-white/80 p-10 shadow-[var(--shadow)] backdrop-blur">
                <div className="mb-10 text-center">
                    <p className="text-xs font-semibold uppercase tracking-[0.35em] text-[var(--gray-text)]">
                        Welcome Back
                    </p>
                    <h1 className="mt-3 font-display text-4xl font-semibold text-[var(--navy-dark)]">
                        Kanban Studio
                    </h1>
                    <p className="mt-3 text-sm leading-6 text-[var(--gray-text)]">
                        Sign in to access your customized workspace
                    </p>
                </div>

                {error && (
                    <div className="mb-6 rounded-xl bg-red-50/80 p-4 text-sm font-medium text-red-600 border border-red-100">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <label
                            htmlFor="username"
                            className="block text-xs font-semibold uppercase tracking-wider text-[var(--navy-dark)]"
                        >
                            Username
                        </label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="block w-full rounded-2xl border border-[var(--stroke)] bg-white px-4 py-3 text-sm text-[var(--navy-dark)] placeholder:text-gray-400 focus:border-[var(--primary-blue)] focus:outline-none focus:ring-1 focus:ring-[var(--primary-blue)] transition-colors"
                            placeholder="Enter username"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <label
                            htmlFor="password"
                            className="block text-xs font-semibold uppercase tracking-wider text-[var(--navy-dark)]"
                        >
                            Password
                        </label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="block w-full rounded-2xl border border-[var(--stroke)] bg-white px-4 py-3 text-sm text-[var(--navy-dark)] placeholder:text-gray-400 focus:border-[var(--primary-blue)] focus:outline-none focus:ring-1 focus:ring-[var(--primary-blue)] transition-colors"
                            placeholder="Enter password"
                            required
                        />
                    </div>

                    <div className="pt-2">
                        <button
                            type="submit"
                            className="w-full rounded-full bg-[var(--secondary-purple)] px-4 py-3.5 text-sm font-semibold tracking-[0.1em] uppercase text-white hover:bg-[#5e2d75] shadow-lg transition-all hover:-translate-y-0.5 active:translate-y-0 focus:outline-none focus:ring-2 focus:ring-[var(--secondary-purple)] focus:ring-offset-2"
                        >
                            Sign In
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
