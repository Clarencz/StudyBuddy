import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Bot } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";

const AITutor = () => {
  const { apiCall } = useAuth();

  const [question, setQuestion] = useState("");
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(false);

  const [flashcards, setFlashcards] = useState([]);
  const [practiceTests, setPracticeTests] = useState([]);

  // Fetch flashcards and practice tests on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const flashRes = await apiCall("/ai/flashcards", { method: "GET" });
        setFlashcards(flashRes.flashcards || []);

        const testRes = await apiCall("/ai/practice-tests", { method: "GET" });
        setPracticeTests(testRes.practice_tests || []);
      } catch (err) {
        console.error("Failed to fetch AI data:", err);
      }
    };

    fetchData();
  }, []);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);

    try {
      // Create a conversation if needed (for simplicity, using a default QA conversation)
      const convRes = await apiCall("/ai/conversations", {
        method: "POST",
        body: JSON.stringify({ type: "qa", title: "Quick Q&A" }),
      });
      const conversationId = convRes.conversation.id;

      // Send message
      const msgRes = await apiCall(
        `/ai/conversations/${conversationId}/messages`,
        {
          method: "POST",
          body: JSON.stringify({ content: question }),
        }
      );

      setAnswers((prev) => [
        ...prev,
        {
          question: msgRes.user_message.content,
          answer: msgRes.ai_message.content,
        },
      ]);
      setQuestion("");
    } catch (err) {
      console.error("AI Tutor request failed:", err);
      alert("Failed to get AI response");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateFlashcards = async () => {
    try {
      const res = await apiCall("/ai/generate-flashcards", {
        method: "POST",
        body: JSON.stringify({
          text: "Example text to generate flashcards",
          count: 5,
        }),
      });
      setFlashcards(res.flashcards);
    } catch (err) {
      console.error("Flashcard generation failed:", err);
      alert("Failed to generate flashcards");
    }
  };

  const handleGeneratePracticeTest = async () => {
    try {
      const res = await apiCall("/ai/generate-practice-test", {
        method: "POST",
        body: JSON.stringify({
          text: "Example text for practice test",
          question_count: 5,
        }),
      });
      setPracticeTests(res.practice_test ? [res.practice_test] : []);
    } catch (err) {
      console.error("Practice test generation failed:", err);
      alert("Failed to generate practice test");
    }
  };

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">AI Tutor</h1>

      {/* Q&A Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Bot className="h-5 w-5 mr-2" /> Q&A
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <textarea
            className="w-full p-2 border rounded"
            rows={3}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question..."
          />
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
            onClick={handleAsk}
            disabled={loading}
          >
            {loading ? "Thinking..." : "Ask"}
          </button>

          <div className="mt-4 space-y-2">
            {answers.map((qa, idx) => (
              <div key={idx} className="p-2 border rounded bg-gray-50">
                <p className="font-semibold">Q: {qa.question}</p>
                <p>A: {qa.answer}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Flashcards Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Bot className="h-5 w-5 mr-2" /> Flashcards
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <button
            className="px-4 py-2 bg-green-600 text-white rounded"
            onClick={handleGenerateFlashcards}
          >
            Generate Flashcards
          </button>
          <ul className="space-y-2">
            {flashcards.map((card) => (
              <li key={card.id} className="p-2 border rounded bg-gray-50">
                <p className="font-semibold">Q: {card.question}</p>
                <p>A: {card.answer}</p>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* Practice Test Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Bot className="h-5 w-5 mr-2" /> Practice Tests
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <button
            className="px-4 py-2 bg-purple-600 text-white rounded"
            onClick={handleGeneratePracticeTest}
          >
            Generate Practice Test
          </button>
          <ul className="space-y-2">
            {practiceTests.map((test) => (
              <li key={test.id} className="p-2 border rounded bg-gray-50">
                <p className="font-semibold">Title: {test.title}</p>
                <pre className="text-sm">{test.questions}</pre>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};

export default AITutor;
