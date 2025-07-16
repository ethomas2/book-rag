import React, { useState } from "react";
import { BookOpen, Search, Quote, Loader2 } from "lucide-react";
import { queryBook } from "./services/api";
import { QueryResponse } from "./types/api";
import "./App.css";

function App() {
  const [chapter, setChapter] = useState<number>(1);
  const [question, setQuestion] = useState<string>("");
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!question.trim()) {
      setError("Please enter a question");
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await queryBook({
        query: question.trim(),
        chapter: chapter,
      });
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-parchment">
      {/* Header */}
      <header className="bg-mahogany text-gold shadow-lg">
        <div className="container mx-auto px-6 py-8">
          <div className="flex items-center justify-center space-x-4">
            <BookOpen className="h-12 w-12" />
            <div className="text-center">
              <h1 className="text-4xl font-display font-bold">
                Literary Companion
              </h1>
              <p className="text-lg mt-2 opacity-90">
                Your spoiler-free guide through the pages
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12 max-w-4xl">
        {/* Query Form */}
        <div className="bg-white rounded-lg shadow-xl p-8 mb-8 border border-gold/20">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="chapter"
                className="block text-lg font-semibold text-ink mb-3"
              >
                Current Chapter
              </label>
              <select
                id="chapter"
                value={chapter}
                onChange={(e) => setChapter(Number(e.target.value))}
                className="w-full px-4 py-3 border border-mahogany/30 rounded-lg focus:ring-2 focus:ring-gold focus:border-transparent bg-parchment text-ink font-serif"
              >
                {Array.from({ length: 17 }, (_, i) => i + 1).map((num) => (
                  <option key={num} value={num}>
                    Chapter {num}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label
                htmlFor="question"
                className="block text-lg font-semibold text-ink mb-3"
              >
                Your Question
              </label>
              <textarea
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask anything about what you've read so far..."
                className="w-full px-4 py-3 border border-mahogany/30 rounded-lg focus:ring-2 focus:ring-gold focus:border-transparent bg-parchment text-ink font-serif resize-none"
                rows={4}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-mahogany text-gold py-4 px-6 rounded-lg font-semibold text-lg hover:bg-mahogany/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  <span>Searching the pages...</span>
                </>
              ) : (
                <>
                  <Search className="h-5 w-5" />
                  <span>Seek Knowledge</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-8">
            <p className="text-red-800 font-medium">{error}</p>
          </div>
        )}

        {/* Response Display */}
        {response && (
          <div className="space-y-8">
            {/* Answer */}
            <div className="bg-white rounded-lg shadow-xl p-8 border border-gold/20">
              <h2 className="text-2xl font-display font-bold text-ink mb-6 flex items-center">
                <BookOpen className="h-6 w-6 mr-3 text-gold" />
                Answer
              </h2>
              <div className="prose prose-lg max-w-none">
                <p className="text-ink leading-relaxed font-serif text-lg">
                  {response.answer}
                </p>
              </div>
            </div>

            {/* Quotes */}
            {response.quotes && response.quotes.length > 0 && (
              <div className="bg-white rounded-lg shadow-xl p-8 border border-gold/20">
                <h3 className="text-xl font-display font-bold text-ink mb-6 flex items-center">
                  <Quote className="h-5 w-5 mr-3 text-gold" />
                  Supporting Passages
                </h3>
                <div className="space-y-4">
                  {response.quotes.map((quote, index) => (
                    <blockquote
                      key={index}
                      className="border-l-4 border-gold pl-6 py-2 italic text-ink font-serif text-lg"
                    >
                      "{quote}"
                    </blockquote>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Empty State */}
        {!response && !loading && !error && (
          <div className="text-center py-16">
            <BookOpen className="h-16 w-16 text-mahogany/40 mx-auto mb-4" />
            <h3 className="text-xl font-display text-ink mb-2">
              Ready to explore?
            </h3>
            <p className="text-mahogany/70 font-serif">
              Enter your question above to begin your literary journey
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-mahogany text-gold py-6 mt-16">
        <div className="container mx-auto px-6 text-center">
          <p className="font-serif opacity-90">
            "The only way to do great work is to love what you do." — Steve Jobs
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
