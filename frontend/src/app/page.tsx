"use client";

import Link from "next/link";
import { Button } from "@/components/ui/Button";
import FloatingChat from "@/components/chat/FloatingChat";
import {
  FaLinkedin,
  FaTwitter,
  FaYoutube,
  FaInstagram,
  FaGithub,
  FaRocket,
  FaShieldAlt,
  FaMobileAlt,
  FaChartLine,
  FaLightbulb,
  FaSyncAlt
} from "react-icons/fa";

export default function LandingPage() {
  return (
    <div className="relative min-h-screen text-white overflow-hidden">
      {/* ================== Professional Background ================== */}
      <div className="absolute inset-0 -z-10">
        {/* Dynamic gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-purple-900/20 to-cyan-900/20"></div>

        {/* Animated grid pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] opacity-20"></div>

        {/* Floating animated shapes */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/3 right-1/4 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
        <div className="absolute top-1/3 right-1/3 w-48 h-48 bg-pink-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '4s'}}></div>
      </div>

      {/* ================== Main Content ================== */}
      <div className="relative max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        {/* Navigation */}
        <nav className="flex justify-between items-center py-8">
          <Link href="/" className="flex items-center space-x-2 group">
            <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-r from-purple-600 to-cyan-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
              <FaRocket className="text-white text-sm sm:text-base" />
            </div>
            <h1 className="text-xl sm:text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-cyan-400">
              TaskWiz
            </h1>
          </Link>

          <div className="hidden md:flex items-center space-x-6 lg:space-x-8">
            <Link href="#features" className="text-gray-300 hover:text-white transition-colors text-sm sm:text-base">Features</Link>
            <Link href="#how-it-works" className="text-gray-300 hover:text-white transition-colors text-sm sm:text-base">How It Works</Link>
            <Link href="/testimonials" className="text-gray-300 hover:text-white transition-colors text-sm sm:text-base">Testimonials</Link>
            <Link href="/pricing" className="text-gray-300 hover:text-white transition-colors text-sm sm:text-base">Pricing</Link>
          </div>

          <div className="flex items-center space-x-2 sm:space-x-4">
            <Link href="/signin">
              <Button className="bg-transparent border border-purple-500 text-white hover:bg-purple-500/10 transition-all duration-300 text-sm">
                Sign In
              </Button>
            </Link>
            <Link href="/signup">
              <Button className="bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-700 hover:to-cyan-600 text-white px-4 py-2 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-purple-500/30 text-sm">
                Get Started
              </Button>
            </Link>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="py-20 md:py-32 flex flex-col items-center text-center">
          <div className="inline-flex items-center px-4 py-2 bg-purple-900/30 rounded-full border border-purple-500/30 mb-6">
            <span className="mr-2">🚀</span>
            <span className="text-sm font-medium text-purple-300">Productivity Redefined</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight max-w-4xl">
            Transform Your <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-cyan-400">Tasks</span> Into <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-pink-400">Achievements</span>
          </h1>

          <p className="text-xl text-gray-300 mb-12 max-w-2xl leading-relaxed">
            The ultimate AI-powered task management platform that learns your habits, predicts your needs, and helps you achieve more with less effort.
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <Link href="/signup">
              <Button className="bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-700 hover:to-cyan-600 text-white px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-purple-500/30">
                Start Free Trial
              </Button>
            </Link>
            <Link href="#features">
              <Button className="bg-transparent border border-gray-600 text-white hover:bg-gray-800/50 px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300">
                Explore Features
              </Button>
            </Link>
          </div>

          <div className="mt-12 flex items-center space-x-8 text-sm text-gray-400">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              <span>Trusted by 10,000+ users</span>
            </div>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              <span>99.9% uptime</span>
            </div>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              <span>Enterprise-grade security</span>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Powerful Features</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Everything you need to boost productivity and stay organized
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <FaRocket className="text-2xl text-purple-400" />,
                title: "AI-Powered Insights",
                description: "Smart suggestions based on your work patterns and priorities"
              },
              {
                icon: <FaShieldAlt className="text-2xl text-cyan-400" />,
                title: "Military-Grade Security",
                description: "Your data is encrypted and protected with the highest standards"
              },
              {
                icon: <FaMobileAlt className="text-2xl text-pink-400" />,
                title: "Cross-Platform Sync",
                description: "Access your tasks anywhere, anytime on any device"
              },
              {
                icon: <FaChartLine className="text-2xl text-yellow-400" />,
                title: "Progress Analytics",
                description: "Track your productivity and see your achievements grow"
              },
              {
                icon: <FaLightbulb className="text-2xl text-green-400" />,
                title: "Smart Automation",
                description: "Automate repetitive tasks and focus on what matters"
              },
              {
                icon: <FaSyncAlt className="text-2xl text-blue-400" />,
                title: "Real-Time Collaboration",
                description: "Work seamlessly with your team in real-time"
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-xl p-6 hover:border-purple-500/50 transition-all duration-300 hover:transform hover:scale-105"
              >
                <div className="w-12 h-12 bg-gray-800 rounded-lg flex items-center justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* How It Works */}
        <section id="how-it-works" className="py-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Get started in minutes and transform your productivity
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                step: "01",
                title: "Sign Up",
                description: "Create your account in seconds with our simple signup process"
              },
              {
                step: "02",
                title: "Add Tasks",
                description: "Quickly add tasks with our intuitive interface or AI voice commands"
              },
              {
                step: "03",
                title: "Achieve More",
                description: "Watch as our AI helps you prioritize and accomplish your goals"
              }
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-cyan-500 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                <p className="text-gray-400">{item.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 text-center">
          <div className="bg-gradient-to-r from-purple-900/30 to-cyan-900/30 border border-purple-500/30 rounded-2xl p-12 max-w-4xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Transform Your Productivity?</h2>
            <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
              Join thousands of professionals who have revolutionized their workflow with TaskWiz
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link href="/signup">
                <Button className="bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-700 hover:to-cyan-600 text-white px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-purple-500/30">
                  Start Free Trial
                </Button>
              </Link>
              <Link href="/demo">
                <Button className="bg-transparent border border-gray-600 text-white hover:bg-gray-800/50 px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300">
                  Watch Demo
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="py-12 border-t border-gray-800 mt-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-cyan-500 rounded-lg flex items-center justify-center">
                  <FaRocket className="text-white text-sm" />
                </div>
                <h3 className="text-xl font-bold">TaskWiz</h3>
              </div>
              <p className="text-gray-400 text-sm">
                The future of task management is here. Boost your productivity with AI.
              </p>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Integrations</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Roadmap</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-4">Connect</h4>
              <div className="flex space-x-4">
                <a href="https://www.linkedin.com/in/laiba-naz-643b192b5/" target="_blank" className="text-gray-400 hover:text-white transition-colors">
                  <FaLinkedin size={20} />
                </a>
                <a href="https://x.com/RajLaiba" target="_blank" className="text-gray-400 hover:text-white transition-colors">
                  <FaTwitter size={20} />
                </a>
                <a href="https://www.youtube.com/@motivate-l9v" target="_blank" className="text-gray-400 hover:text-white transition-colors">
                  <FaYoutube size={20} />
                </a>
                <a href="https://www.instagram.com/laibanaz012/" target="_blank" className="text-gray-400 hover:text-white transition-colors">
                  <FaInstagram size={20} />
                </a>
                <a href="https://github.com/Laiba772" target="_blank" className="text-gray-400 hover:text-white transition-colors">
                  <FaGithub size={20} />
                </a>
              </div>
            </div>
          </div>

          <div className="pt-8 border-t border-gray-800 text-center text-gray-500 text-sm">
            <p>&copy; 2026 TaskWiz. All rights reserved. Built with ❤️ by LAIBA NAZ.</p>
          </div>
        </footer>
      </div>

      {/* ================== Floating Chat Button ================== */}
      <FloatingChat />
    </div>
  );
}
