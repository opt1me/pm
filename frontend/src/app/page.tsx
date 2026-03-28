"use client";

import { KanbanBoard } from "@/components/KanbanBoard";
import { Login } from "@/components/Login";
import { useAuth } from "@/lib/auth";

export default function Home() {
  const { isAuthenticated, isLoading, logout } = useAuth();

  if (isLoading) {
    return <div className="flex min-h-screen items-center justify-center bg-[var(--navy-dark)]"><div className="text-white text-xl">Loading...</div></div>;
  }

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <div className="relative">
      <header className="absolute top-4 right-4 z-50">
        <button
          onClick={logout}
          className="rounded bg-[var(--secondary-purple)] px-4 py-2 text-sm font-medium text-white hover:bg-[#5e2d75] shadow-md transition-colors"
        >
          Sign Out
        </button>
      </header>
      <KanbanBoard />
    </div>
  );
}
