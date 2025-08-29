import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Bot } from 'lucide-react'

const AITutor = () => {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">AI Tutor</h1>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Bot className="h-5 w-5 mr-2" />
            AI-Powered Learning Assistant
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600">
            AI tutor chat interface, flashcard generation, and practice test features will be implemented here.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default AITutor

