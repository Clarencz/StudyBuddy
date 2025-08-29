import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Users, Plus } from 'lucide-react'

const StudyRooms = () => {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Study Rooms</h1>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="h-5 w-5 mr-2" />
            Study Rooms Feature
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600">
            Study rooms functionality will be implemented here. Users will be able to create and join collaborative study sessions.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default StudyRooms

