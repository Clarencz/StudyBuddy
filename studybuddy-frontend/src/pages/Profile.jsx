import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { User } from 'lucide-react'

const Profile = () => {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Profile</h1>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <User className="h-5 w-5 mr-2" />
            User Profile Settings
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600">
            User profile management, settings, and account preferences will be implemented here.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default Profile

