import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Users,
  Bot,
  FileText,
  Video,
  Zap,
  Shield,
  Crown,
  ArrowRight,
  CheckCircle,
  Star,
  Brain,
  Sparkles,
} from "lucide-react";
import studyBuddyLogo from "../assets/studybuddy_logo.png";

const LandingPage = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const features = [
    {
      icon: Users,
      title: "Collaborative Study Rooms",
      description:
        "Create or join study rooms with peers, share resources, and learn together in real-time.",
      color: "from-blue-500 to-cyan-500",
    },
    {
      icon: Bot,
      title: "AI-Powered Tutor",
      description:
        "Get instant help with Q&A, summaries, flashcards, and practice tests from our advanced AI.",
      color: "from-purple-500 to-pink-500",
    },
    {
      icon: FileText,
      title: "Smart Document Processing",
      description:
        "Upload PDFs and convert them to interactive flipbooks with AI-powered content extraction.",
      color: "from-green-500 to-emerald-500",
    },
    {
      icon: Video,
      title: "Integrated Video Calls",
      description:
        "Seamlessly connect with Google Meet or Zoom directly from your study rooms.",
      color: "from-orange-500 to-red-500",
    },
    {
      icon: Zap,
      title: "Gamified Learning",
      description:
        "Build study streaks, earn badges, and track your progress with engaging gamification.",
      color: "from-yellow-500 to-orange-500",
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description:
        "Your data is protected with JWT authentication, encryption, and advanced security measures.",
      color: "from-indigo-500 to-purple-500",
    },
  ];

  const testimonials = [
    {
      name: "Sarah Johnson",
      role: "Computer Science Student",
      content:
        "StudyBuddy transformed how I study. The AI tutor helps me understand complex concepts instantly!",
      rating: 5,
    },
    {
      name: "Michael Chen",
      role: "Medical Student",
      content:
        "The collaborative study rooms are amazing. I can study with classmates even when we're apart.",
      rating: 5,
    },
    {
      name: "Emily Rodriguez",
      role: "Engineering Student",
      content:
        "The PDF flipbook feature is incredible. It makes reading research papers so much more engaging.",
      rating: 5,
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-purple-600/10 to-pink-600/10" />
        <div className="relative container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto">
            <Badge className="mb-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2">
              <Sparkles className="h-4 w-4 mr-2" />
              AI-Powered Collaborative Learning
            </Badge>

            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              Study Smarter, Together
            </h1>

            <p className="text-xl md:text-2xl text-gray-600 mb-8 leading-relaxed">
              Join the future of education with StudyBuddy - where AI meets
              collaboration. Create study rooms, get instant AI tutoring, and
              transform your learning experience.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              {isAuthenticated ? (
                <Button
                  size="lg"
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-lg px-8 py-4"
                  onClick={() => navigate("/dashboard")}
                >
                  Go to Dashboard
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              ) : (
                <>
                  <Button
                    size="lg"
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-lg px-8 py-4"
                    onClick={() => navigate("/register")}
                  >
                    Start Learning Free
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                  <Button
                    variant="outline"
                    size="lg"
                    className="text-lg px-8 py-4 border-2"
                    onClick={() => navigate("/login")}
                  >
                    Sign In
                  </Button>
                </>
              )}
            </div>

            <div className="flex items-center justify-center space-x-8 text-sm text-gray-500">
              <div className="flex items-center">
                <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                Free to start
              </div>
              <div className="flex items-center">
                <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                No credit card required
              </div>
              <div className="flex items-center">
                <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                Secure & private
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Everything You Need to
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                {" "}
                Excel
              </span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              StudyBuddy combines the power of AI with collaborative learning to
              create the ultimate educational experience.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card
                  key={index}
                  className="group hover:shadow-xl transition-all duration-300 border-0 bg-gradient-to-br from-white to-gray-50"
                >
                  <CardContent className="p-8">
                    <div
                      className={`inline-flex p-3 rounded-xl bg-gradient-to-r ${feature.color} mb-6 group-hover:scale-110 transition-transform duration-300`}
                    >
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="text-xl font-bold mb-4 group-hover:text-blue-600 transition-colors">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {feature.description}
                    </p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Loved by
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                {" "}
                Students
              </span>
            </h2>
            <p className="text-xl text-gray-600">
              See what students are saying about StudyBuddy
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card
                key={index}
                className="bg-white/80 backdrop-blur-sm border-0 shadow-lg"
              >
                <CardContent className="p-8">
                  <div className="flex mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star
                        key={i}
                        className="h-5 w-5 text-yellow-400 fill-current"
                      />
                    ))}
                  </div>
                  <p className="text-gray-700 mb-6 italic">
                    "{testimonial.content}"
                  </p>
                  <div>
                    <p className="font-semibold text-gray-900">
                      {testimonial.name}
                    </p>
                    <p className="text-sm text-gray-500">{testimonial.role}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-3xl mx-auto">
            <Brain className="h-16 w-16 text-white mx-auto mb-6" />
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Transform Your Learning?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Join thousands of students who are already studying smarter with
              StudyBuddy.
            </p>
            {!isAuthenticated && (
              <Button
                size="lg"
                className="bg-white text-blue-600 hover:bg-gray-100 text-lg px-8 py-4"
                onClick={() => navigate("/register")}
              >
                Get Started Free Today
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            )}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-3 mb-4 md:mb-0">
              <img
                src={studyBuddyLogo}
                alt="StudyBuddy"
                className="h-8 w-auto"
              />
              <span className="text-lg font-semibold">StudyBuddy</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2025 StudyBuddy. All rights reserved. Built with ❤️ for
              students.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
