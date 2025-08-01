"use client";

import { useState } from "react";

export default function Page() {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) {
      setMessage("텍스트를 입력해주세요.");
      return;
    }

    setIsLoading(true);
    setMessage("");

    try {
      // 입력된 텍스트를 JSON으로 변환
      const jsonData = {
        text: input,
        timestamp: new Date().toISOString(),
        source: "frontend"
      };

      console.log("전송할 JSON 데이터:", jsonData);

      // Gateway API로 전송
      const response = await fetch("/api/process-text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Gateway 응답:", result);
        setMessage("데이터가 성공적으로 전송되었습니다!");
        setInput(""); // 입력 필드 초기화
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error("전송 오류:", error);
      setMessage("전송 중 오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-black text-white">
      <div className="w-full max-w-xl text-center space-y-6 px-4">
        {/* 타이틀 */}
        <h1 className="text-2xl font-semibold">무엇을 도와드릴까요?</h1>

        {/* 메시지 표시 */}
        {message && (
          <div className={`text-sm p-3 rounded-lg ${
            message.includes("성공") 
              ? "bg-green-900 text-green-100" 
              : "bg-red-900 text-red-100"
          }`}>
            {message}
          </div>
        )}

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
            disabled={isLoading}
            className="bg-transparent flex-1 outline-none text-sm placeholder-zinc-400 disabled:opacity-50"
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

            {/* 전송 버튼 */}
            <button 
              type="submit" 
              disabled={isLoading}
              className="disabled:opacity-50"
            >
              {isLoading ? (
                <svg className="animate-spin h-5 w-5 text-zinc-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
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
              )}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}