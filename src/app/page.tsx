"use client";

import { useState } from "react";

export default function Page() {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const jsonData = JSON.stringify({ text: input });
    console.log("입력값(JSON):", jsonData);
    // 여기에 Gateway로 전달하는 로직 추가 가능
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-black text-white">
      <div className="w-full max-w-xl text-center space-y-6 px-4">
        {/* 타이틀 */}
        <h1 className="text-2xl font-semibold">무엇을 도와드릴까요?</h1>

        {/* 폼 입력 영역 */}
        <form
          onSubmit={handleSubmit}
          className="bg-zinc-900 rounded-xl flex items-center px-4 py-3"
        >
          <input
            type="text"
            placeholder="무엇이든 물어보세요"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="bg-transparent flex-1 outline-none text-sm placeholder-zinc-400"
          />

          {/* 아이콘 영역 */}
          <div className="flex items-center space-x-3">
            {/* 도구 버튼 */}
            <button
              type="button"
              className="flex items-center text-sm text-zinc-400 hover:text-white"
            >
              <span className="text-lg mr-1">＋</span>도구
            </button>

            {/* 마이크 버튼 */}
            <button type="button">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5 text-zinc-400 hover:text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 1v14m0 0a5 5 0 005-5H7a5 5 0 005 5z"
                />
              </svg>
            </button>

            {/* 오디오파형 버튼 */}
            <button type="submit">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5 text-zinc-400 hover:text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 12h3m3 0h3m3 0h3m3 0h3"
                />
              </svg>
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}