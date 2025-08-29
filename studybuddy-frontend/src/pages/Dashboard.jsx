import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import {
  Users,
  FileText,
  Bot,
  Zap,
  Clock,
  Trophy,
  Plus,
  ArrowRight,
  BookOpen,
  Target,
  TrendingUp,
  Calendar
} from 'lucide-react'

const Dashboard = () => {
  const { user, apiCall } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState({
    totalStudyTime: 0,
    roomsJoined: 0,
    documentsUploaded: 0,
    flashcardsCreated: 0,
    recentActivity: []
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // In a real app, you'd have a dashboard endpoint
        // For now, we'll simulate the data
        setStats({
          totalStudyTime: user?.total_study_time || 0,
          roomsJoined: 3,
          documentsUploaded: 5,
          flashcardsCreated: 24,
          recentActivity: [
            { type: 'study', description: 'Studied in Math Study Group', time: '2 hours ago' },
            { type: 'document', description: 'Uploaded Calculus Notes.pdf', time: '1 day ago' },
            { type: 'ai', description: 'Generated flashcards from Biology chapter', time: '2 days ago' },
            { type: 'room', description: 'Joined Physics Study Room', time: '3 days ago' }
          ]
        })
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [user])

  const quickActions = [
    {
      title: 'Create Study Room',
      description: 'Start a new collaborative study session',
      icon: Users,
      color: 'from-blue-500 to-cyan-500',
      action: () => navigate('/study-rooms')
    },
    {
      title: 'Upload Document',
      description: 'Add PDFs and create flipbooks',
      icon: FileText,
      color: 'from-green-500 to-emerald-500',
      action: () => navigate('/documents')
    },
    {
      title: 'Ask AI Tutor',
      description: 'Get instant help with your studies',
      icon: Bot,
      color: 'from-purple-500 to-pink-500',
      action: () => navigate('/ai-tutor')
    }
  ]

  const achievements = [
    { name: 'First Steps', description: 'Created your first study room', earned: true },
    { name: 'Knowledge Seeker', description: 'Uploaded 5 documents', earned: true },
    { name: 'Streak Master', description: 'Maintain a 7-day study streak', earned: user?.streak_count >= 7 },
    { name: 'Collaborator', description: 'Join 10 study rooms', earned: false },
    { name: 'AI Enthusiast', description: 'Generate 50 flashcards', earned: false }
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">
              Welcome back, {user?.first_name}! 👋
            </h1>
            <p className="text-blue-100 text-lg">
              Ready to continue your learning journey?
            </p>
          </div>
          <div className="mt-4 md:mt-0 flex items-center space-x-4">
            <div className="text-center">
              <div className="flex items-center space-x-2 bg-white/20 rounded-full px-4 py-2">
                <Zap className="h-5 w-5 text-yellow-300" />
                <span className="font-bold text-lg">{user?.streak_count || 0}</span>
              </div>
              <p className="text-sm text-blue-100 mt-1">Day Streak</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-600">Study Time</p>
                <p className="text-2xl font-bold text-blue-900">
                  {Math.floor(stats.totalStudyTime / 60)}h {stats.totalStudyTime % 60}m
                </p>
              </div>
              <Clock className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600">Study Rooms</p>
                <p className="text-2xl font-bold text-green-900">{stats.roomsJoined}</p>
              </div>
              <Users className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-purple-600">Documents</p>
                <p className="text-2xl font-bold text-purple-900">{stats.documentsUploaded}</p>
              </div>
              <FileText className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-orange-600">Flashcards</p>
                <p className="text-2xl font-bold text-orange-900">{stats.flashcardsCreated}</p>
              </div>
              <BookOpen className="h-8 w-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-2xl font-bold mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action, index) => {
            const Icon = action.icon
            return (
              <Card 
                key={index} 
                className="group hover:shadow-xl transition-all duration-300 cursor-pointer border-0 bg-gradient-to-br from-white to-gray-50"
                onClick={action.action}
              >
                <CardContent className="p-6">
                  <div className={`inline-flex p-3 rounded-xl bg-gradient-to-r ${action.color} mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2 group-hover:text-blue-600 transition-colors">
                    {action.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4">
                    {action.description}
                  </p>
                  <div className="flex items-center text-blue-600 text-sm font-medium">
                    Get Started
                    <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Recent Activity
            </CardTitle>
            <CardDescription>
              Your latest study activities
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {stats.recentActivity.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 rounded-lg bg-gray-50">
                  <div className={`p-2 rounded-full ${
                    activity.type === 'study' ? 'bg-blue-100 text-blue-600' :
                    activity.type === 'document' ? 'bg-green-100 text-green-600' :
                    activity.type === 'ai' ? 'bg-purple-100 text-purple-600' :
                    'bg-orange-100 text-orange-600'
                  }`}>
                    {activity.type === 'study' && <Clock className="h-4 w-4" />}
                    {activity.type === 'document' && <FileText className="h-4 w-4" />}
                    {activity.type === 'ai' && <Bot className="h-4 w-4" />}
                    {activity.type === 'room' && <Users className="h-4 w-4" />}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">
                      {activity.description}
                    </p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Achievements */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Trophy className="h-5 w-5 mr-2" />
              Achievements
            </CardTitle>
            <CardDescription>
              Track your learning milestones
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {achievements.map((achievement, index) => (
                <div key={index} className="flex items-center space-x-3">
                  <div className={`p-2 rounded-full ${
                    achievement.earned 
                      ? 'bg-yellow-100 text-yellow-600' 
                      : 'bg-gray-100 text-gray-400'
                  }`}>
                    <Trophy className="h-4 w-4" />
                  </div>
                  <div className="flex-1">
                    <p className={`text-sm font-medium ${
                      achievement.earned ? 'text-gray-900' : 'text-gray-500'
                    }`}>
                      {achievement.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {achievement.description}
                    </p>
                  </div>
                  {achievement.earned && (
                    <Badge className="bg-yellow-100 text-yellow-800">
                      Earned
                    </Badge>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Study Goal Progress */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="h-5 w-5 mr-2" />
            Weekly Study Goal
          </CardTitle>
          <CardDescription>
            You're doing great! Keep up the momentum.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Study Time This Week</span>
              <span className="text-sm text-gray-500">
                {Math.floor(stats.totalStudyTime / 60)}h / 20h goal
              </span>
            </div>
            <Progress 
              value={(stats.totalStudyTime / 60 / 20) * 100} 
              className="h-3"
            />
            <p className="text-xs text-gray-500">
              You need {Math.max(0, 20 - Math.floor(stats.totalStudyTime / 60))} more hours to reach your weekly goal.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

