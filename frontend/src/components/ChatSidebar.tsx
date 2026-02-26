"use client";

import { useState, useRef, useEffect } from "react";
import type { BoardData } from "@/lib/kanban";

interface ChatSidebarProps {
    onBoardUpdate: (board: BoardData) => void;
}

export function ChatSidebar({ onBoardUpdate }: ChatSidebarProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<{ role: "user" | "ai"; content: string }[]>([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput("");
        setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
        setIsLoading(true);

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!res.ok) throw new Error("Failed to chat with AI.");

            const data = await res.json();

            setMessages((prev) => [
                ...prev,
                { role: "ai", content: data.text_response || "Done." },
            ]);

            if (data.updated && data.board_data) {
                onBoardUpdate(data.board_data);
            }
        } catch (err: any) {
            setMessages((prev) => [
                ...prev,
                { role: "ai", content: `Error: ${err.message}` },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-[var(--navy-dark)] text-white shadow-xl transition-transform hover:scale-105"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z" /></svg>
            </button>
        );
    }

    return (
        <div className="fixed bottom-6 right-6 z-50 flex h-[600px] w-[400px] flex-col overflow-hidden rounded-2xl border border-[var(--stroke)] bg-white/95 shadow-2xl backdrop-blur-md transition-all">
            {/* Header */}
            <div className="flex items-center justify-between bg-[var(--navy-dark)] px-5 py-4 text-white">
                <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded bg-[var(--accent-yellow)] text-[var(--navy-dark)] font-bold">
                        AI
                    </div>
                    <div>
                        <h3 className="font-semibold">Kanban Assistant</h3>
                        <p className="text-xs text-blue-200">Powered by OpenRouter</p>
                    </div>
                </div>
                <button
                    onClick={() => setIsOpen(false)}
                    className="text-gray-300 hover:text-white"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18" /><path d="m6 6 12 12" /></svg>
                </button>
            </div>

            {/* Messages area */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-5 space-y-4 bg-gray-50/50">
                {messages.length === 0 && (
                    <div className="text-center text-sm text-[var(--gray-text)] mt-10">
                        Ask me to add a card, rename a column, or just chat!
                    </div>
                )}
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                        <div
                            className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm ${msg.role === "user"
                                    ? "bg-[var(--primary-blue)] text-white"
                                    : "bg-white border border-[var(--stroke)] text-gray-800 shadow-sm"
                                }`}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white border border-[var(--stroke)] rounded-2xl px-4 py-2 text-sm text-[var(--gray-text)] shadow-sm flex items-center gap-2">
                            <span className="flex gap-1">
                                <span className="w-1.5 h-1.5 bg-[var(--accent-yellow)] rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                <span className="w-1.5 h-1.5 bg-[var(--accent-yellow)] rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                <span className="w-1.5 h-1.5 bg-[var(--accent-yellow)] rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </span>
                        </div>
                    </div>
                )}
            </div>

            {/* Input area */}
            <form onSubmit={handleSubmit} className="border-t border-[var(--stroke)] bg-white p-4">
                <div className="relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        disabled={isLoading}
                        placeholder="Type a command..."
                        className="w-full rounded-full border border-[var(--stroke)] bg-gray-50 pl-4 pr-12 py-3 text-sm focus:border-[var(--primary-blue)] focus:outline-none focus:ring-1 focus:ring-[var(--primary-blue)] disabled:opacity-50"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="absolute right-2 top-1/2 -translate-y-1/2 flex h-8 w-8 items-center justify-center rounded-full bg-[var(--secondary-purple)] text-white disabled:opacity-50 transition-colors hover:bg-[#5e2d75]"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m22 2-7 20-4-9-9-4Z" /><path d="M22 2 11 13" /></svg>
                    </button>
                </div>
            </form>
        </div>
    );
}
