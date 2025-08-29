import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Video } from 'lucide-react'

const StudyRoom = () => {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Study Room</h1>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Video className="h-5 w-5 mr-2" />
            Individual Study Room
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600">
            Individual study room with whiteboard, video calls, and collaboration features will be implemented here.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default StudyRoom

