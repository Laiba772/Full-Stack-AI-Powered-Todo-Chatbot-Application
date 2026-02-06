import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function TestimonialsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white">
      {/* Header */}
      <header className="py-6 px-6 sm:px-8 lg:px-12 border-b border-gray-800">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-cyan-400">
            ✨ TaskWiz
          </Link>
          <Link href="/">
            <Button className="bg-transparent border border-purple-500 text-white hover:bg-purple-500/10 transition-all">
              ← Back to Home
            </Button>
          </Link>
        </div>
      </header>

      <main className="py-20 px-6 sm:px-8 lg:px-12">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Customer <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-cyan-400">Testimonials</span>
          </h1>
          <p className="text-xl text-gray-400 mb-16 max-w-3xl mx-auto">
            Hear from our satisfied customers who have transformed their productivity
          </p>

          {/* Coming Soon Section */}
          <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-12 max-w-4xl mx-auto">
            <div className="flex flex-col items-center justify-center">
              <div className="w-24 h-24 bg-gradient-to-r from-purple-600 to-cyan-500 rounded-full flex items-center justify-center mb-8">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 className="text-3xl font-bold mb-4">Coming Soon</h2>
              <p className="text-gray-400 text-lg mb-8 max-w-md">
                We're gathering authentic testimonials from our amazing users. Check back soon to see what they have to say about TaskWiz!
              </p>
              <div className="flex space-x-4">
                <Link href="/">
                  <Button className="bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-700 hover:to-cyan-600 text-white px-6 py-3 rounded-lg transition-all">
                    Back to Home
                  </Button>
                </Link>
                <Link href="/#contact">
                  <Button className="bg-transparent border border-gray-600 text-white hover:bg-gray-800/50 px-6 py-3 rounded-lg transition-all">
                    Contact Us
                  </Button>
                </Link>
              </div>
            </div>
          </div>

          {/* Placeholder for future testimonials */}
          <div className="mt-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map((item) => (
              <div key={item} className="bg-gray-900/30 backdrop-blur-sm border border-gray-800 rounded-xl p-6 opacity-50">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center mr-4">
                    <div className="bg-gray-600 rounded-full w-8 h-8"></div>
                  </div>
                  <div>
                    <div className="h-4 bg-gray-700 rounded w-24 mb-2"></div>
                    <div className="h-3 bg-gray-700 rounded w-16"></div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="h-3 bg-gray-700 rounded"></div>
                  <div className="h-3 bg-gray-700 rounded w-5/6"></div>
                  <div className="h-3 bg-gray-700 rounded w-4/6"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>

      <footer className="py-8 text-center text-gray-500 text-sm border-t border-gray-800">
        <p>&copy; 2026 TaskWiz. All rights reserved.</p>
      </footer>
    </div>
  );
}