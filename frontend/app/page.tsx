"use client";

import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ role: "user" | "assistant", text: string }[]>([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [showAgents, setShowAgents] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState("Master Agent");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatResponse = (data: any) => {
    if (data.action_type === "gmail_read_emails") {
      return "Here are your latest emails:\n\n" +
        data.data.map((email: any, index: number) =>
          `${index + 1}. ${email.sender}\nSubject: ${email.subject}`
        ).join("\n\n");
    }

    if (data.action_type === "calendar_list_events") {
      return "Here are your upcoming events:\n\n" +
        data.data.map((event: any, index: number) =>
          `${index + 1}. ${event.summary}\nStart: ${event.start}\nEnd: ${event.end}`
        ).join("\n\n");
    }

    if (data.status === "failed") {
      return `⚠️ ${data.message}`;
    }

    return data.message || "Request completed successfully.";
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;

    setMessages(prev => [
      ...prev,
      { role: "user", text: userMessage }
    ]);

    setInput("");

    setMessages(prev => [
      ...prev,
      { role: "assistant", text: "" }
    ]);

    try {
      const response = await fetch("http://127.0.0.1:8000/nlp/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_input: userMessage
        })
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        const rawChunk = decoder.decode(value);

        const chunk = rawChunk
          .replace(/(\b\w+\b)( \1\b)+/gi, "$1")   // repeated words
          .replace(/(\d+)\.\./g, "$1.")          // 11.. -> 1.
          .replace(/\[\[/g, "[")
          .replace(/\]\]/g, "]")
          .replace(/\s+/g, " ");

        setMessages(prev => {
          const updated = [...prev];
          updated[updated.length - 1].text += chunk;
          return updated;
        });
      }

    } catch (error) {
      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1].text =
          "Error connecting to Personal Agent backend.";
        return updated;
      });
    }
  };
  return (
    <div className="flex h-screen bg-[#212121] text-gray-100 font-sans selection:bg-gray-700">

      {/* Sidebar Overlay for Mobile */}
      <div className={`fixed inset-0 bg-black/50 z-40 lg:hidden ${isSidebarOpen ? 'block' : 'hidden'}`} onClick={() => setIsSidebarOpen(false)} />

      {/* Sidebar */}
      <aside className={`fixed lg:static top-0 left-0 h-full w-[260px] bg-[#171717] flex flex-col transition-transform duration-300 z-50 ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'} lg:flex-shrink-0`}>
        <div className="p-3 pb-2 flex justify-between items-center h-14">
          <button
            className="flex-1 flex items-center gap-2 hover:bg-[#202123] rounded-md p-2 transition-colors text-sm font-medium"
            onClick={() => setMessages([])}
          >
            <div className="w-7 h-7 rounded-full bg-white flex items-center justify-center">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
            </div>
            New chat
          </button>
          <button onClick={() => setIsSidebarOpen(false)} className="lg:hidden p-2 text-gray-400 hover:text-white">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
          <button className="hidden lg:flex p-2 text-gray-400 hover:text-white rounded-md hover:bg-[#202123] ml-1" onClick={() => setIsSidebarOpen(false)}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line></svg>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
          <div className="text-xs font-semibold text-gray-500 mb-3 px-2 mt-4">Today</div>
          <button className="w-full text-left p-2 rounded-md hover:bg-[#202123] text-sm text-gray-300 truncate">
            Building ChatGPT Clone
          </button>
        </div>

        <div className="p-3 border-t border-white/10">
          <button className="flex items-center gap-3 w-full p-2 rounded-md hover:bg-[#202123] text-sm font-medium transition-colors">
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"></div>
            User Account
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative w-full h-full overflow-hidden bg-[#212121]">

        {/* Top bar (mobile + sidebar toggle) */}
        <div className="absolute top-0 w-full z-10 flex items-center p-2 text-gray-200">
          {!isSidebarOpen && (
            <button className="p-2 hover:bg-[#2f2f2f] rounded-md transition-colors" onClick={() => setIsSidebarOpen(true)}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
            </button>
          )}
          <div className="flex-1 font-medium opacity-0">ChatGPT Clone</div>
        </div>

        {/* Top Spacer for centering */}
        <div className={`transition-[flex-grow] duration-700 ease-in-out ${messages.length === 0 ? 'flex-[1]' : 'flex-[0] min-h-0'}`} />

        {/* Chat Messages */}
        <div className={`w-full flex flex-col overflow-y-auto scroll-smooth transition-all duration-700 ease-in-out ${messages.length === 0 ? 'flex-[0] opacity-0 h-0 overflow-hidden' : 'flex-[1] opacity-100 pt-14'}`}>
          <div className="flex flex-col pb-9">
            {messages.map((msg, index) => (
              <div key={index} className="w-full bg-[#212121]">
                <div className="max-w-3xl mx-auto flex gap-4 px-4 py-6 md:px-5 lg:px-1 xl:px-5">
                  <div className="flex-shrink-0 flex flex-col items-center mt-1">
                    {msg.role === "assistant" ? (
                      <div className="w-8 h-8 rounded-full bg-[#10a37f] flex items-center justify-center">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
                      </div>
                    ) : (
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"></div>
                    )}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="font-semibold text-sm mb-1">{msg.role === "user" ? "You" : selectedAgent}</div>
                    <div className="text-base text-gray-100 leading-relaxed">
                      {msg.role === "assistant" ? (
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            h1: ({ node, ...props }) => <h1 className="text-2xl font-bold text-white mt-6 mb-4" {...props} />,
                            h2: ({ node, ...props }) => <h2 className="text-xl font-bold text-white mt-5 mb-3" {...props} />,
                            h3: ({ node, ...props }) => <h3 className="text-lg font-bold text-white mt-4 mb-2" {...props} />,
                            h4: ({ node, ...props }) => <h4 className="text-base font-bold text-gray-200 mt-4 mb-2" {...props} />,
                            p: ({ node, ...props }) => <p className="mb-3 last:mb-0" {...props} />,
                            ul: ({ node, ...props }) => <ul className="list-disc list-outside ml-5 mb-4 space-y-1" {...props} />,
                            ol: ({ node, ...props }) => <ol className="list-decimal list-outside ml-5 mb-4 space-y-1" {...props} />,
                            li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                            strong: ({ node, ...props }) => <strong className="font-semibold text-white" {...props} />,
                            blockquote: ({ node, ...props }) => <blockquote className="border-l-4 border-gray-600 pl-4 py-1 my-3 text-gray-400 bg-gray-800/30 rounded-r" {...props} />,
                            code: ({ node, className, children, ...props }: any) => {
                              const match = /language-(\w+)/.exec(className || '')
                              return !match ? (
                                <code className="bg-[#2f2f2f] px-1.5 py-0.5 rounded text-sm font-mono text-pink-300" {...props}>
                                  {children}
                                </code>
                              ) : (
                                <code className="block bg-[#1e1e1e] p-3 rounded-md text-sm font-mono text-gray-200 overflow-x-auto my-3" {...props}>
                                  {children}
                                </code>
                              )
                            }
                          }}
                        >
                          {msg.text}
                        </ReactMarkdown>
                      ) : (
                        <div className="whitespace-pre-wrap">{msg.text}</div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} className="h-4" />
          </div>
        </div>

        {/* Center / Bottom Input Area */}
        <div className={`w-full transition-all duration-700 ease-in-out flex flex-col items-center flex-none ${messages.length === 0 ? 'px-4 md:px-6' : 'px-4 md:px-6 pb-4 md:pb-6'}`}>

          {/* Title */}
          <h1 className={`text-3xl md:text-4xl font-semibold text-gray-200 transition-all duration-700 ease-in-out whitespace-nowrap overflow-hidden flex items-center justify-center ${messages.length === 0 ? 'h-16 mb-6 opacity-100' : 'h-0 mb-0 opacity-0'}`}>
            What are you working on?
          </h1>

          <div className="w-full max-w-[700px] relative">
            <div className="relative flex items-center w-full p-2 bg-[#2f2f2f] rounded-[32px] border border-gray-700 shadow-sm focus-within:border-gray-500 transition-shadow">

              <div className="flex items-center ml-1">
                {/* Add File Button */}
                <button
                  className="p-2 text-gray-400 hover:text-white rounded-full transition-colors flex items-center justify-center"
                  title="Attach files"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                </button>

                {/* Agent Selector */}
                <div className="relative flex items-center">
                  <button
                    onClick={() => setShowAgents(!showAgents)}
                    className="p-2 text-gray-400 hover:text-white rounded-full transition-colors flex items-center justify-center relative"
                    title="Choose Agent"
                  >
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="3" y="11" width="18" height="10" rx="2"></rect>
                      <circle cx="12" cy="5" r="2"></circle>
                      <path d="M12 7v4"></path>
                      <line x1="8" y1="16" x2="8" y2="16.01"></line>
                      <line x1="16" y1="16" x2="16" y2="16.01"></line>
                    </svg>

                    {/* Selected agent indicator dot */}
                    <span className="absolute top-1 right-1 w-2 h-2 bg-blue-500 rounded-full border border-[#2f2f2f]"></span>
                  </button>

                  {showAgents && (
                    <>
                      <div className="fixed inset-0 z-40" onClick={() => setShowAgents(false)}></div>
                      <div className="absolute bottom-full left-0 mb-2 w-56 bg-[#2f2f2f] border border-gray-700 rounded-xl shadow-lg overflow-hidden z-50 py-1">
                        <div className="px-3 py-2 text-xs font-semibold text-gray-400 border-b border-gray-700 mb-1">Select Agent</div>
                        {["Master Agent", "Coding Agent", "Research Agent", "Calendar Agent"].map(agent => (
                          <button
                            key={agent}
                            onClick={() => { setSelectedAgent(agent); setShowAgents(false); }}
                            className={`w-full text-left px-4 py-2 text-sm flex items-center justify-between hover:bg-[#40414f] transition-colors ${selectedAgent === agent ? 'text-white bg-[#40414f]' : 'text-gray-300'}`}
                          >
                            {agent}
                            {selectedAgent === agent && (
                              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            )}
                          </button>
                        ))}
                      </div>
                    </>
                  )}
                </div>
              </div>

              <textarea
                value={input}
                onChange={(e) => {
                  setInput(e.target.value);
                  e.target.style.height = 'auto';
                  e.target.style.height = `${Math.min(e.target.scrollHeight, 200)}px`;
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                placeholder="Ask anything"
                className="mx-2 w-full resize-none bg-transparent py-[10px] text-base text-white placeholder-gray-400 focus:outline-none"
                rows={1}
                style={{ minHeight: "44px", maxHeight: "200px" }}
              />

              <button
                onClick={handleSend}
                disabled={!input.trim()}
                className={`p-2 rounded-full mb-0.5 transition-colors ${input.trim() ? 'bg-white text-black hover:bg-gray-200' : 'bg-[#40414f] text-gray-500'}`}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
              </button>
            </div>
            <div className="text-center text-xs text-gray-400 mt-3 h-4">
              This is PersonalAgent. A powerful tool for automation using Agentic Cluster.
            </div>
          </div>
        </div>

        {/* Bottom Spacer for centering */}
        <div className={`transition-[flex-grow] duration-700 ease-in-out ${messages.length === 0 ? 'flex-[1]' : 'flex-[0] min-h-0'}`} />

      </main>
    </div>
  );
}