// Professional Sign in page with enhanced design

import React from 'react';
import Link from 'next/link';
import { SignInForm } from '@/components/auth/SignInForm';
import { FaLock, FaEnvelope, FaArrowRight, FaUserPlus } from 'react-icons/fa';

export default function SignInPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900/20 to-black px-4 py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-cyan-500/5 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
        <div className="absolute top-1/3 right-1/3 w-64 h-64 bg-pink-500/5 rounded-full blur-3xl animate-pulse" style={{animationDelay: '4s'}}></div>
      </div>

      <div className="max-w-md w-full space-y-8 relative z-10">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-cyan-500 rounded-2xl flex items-center justify-center">
              <FaLock className="text-white text-2xl" />
            </div>
          </div>
          <h2 className="mt-6 text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-cyan-400">
            Welcome Back
          </h2>
          <p className="mt-2 text-base text-gray-400">
            Sign in to access your personalized task dashboard
          </p>
        </div>

        <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-8 shadow-xl">
          <div className="flex items-center mb-6">
            <div className="w-10 h-1 bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full mr-3"></div>
            <h3 className="text-xl font-semibold text-gray-200">Sign In</h3>
          </div>

          <SignInForm />

          <div className="mt-8 pt-6 border-t border-gray-800">
            <div className="text-center text-sm">
              <p className="text-gray-400 mb-3">New to TaskWiz?</p>
              <Link
                href="/signup"
                className="inline-flex items-center font-medium text-cyan-400 hover:text-cyan-300 transition-colors"
              >
                Create an account <FaUserPlus className="ml-2 text-sm" />
              </Link>
            </div>
          </div>
        </div>

        <div className="text-center text-xs text-gray-500 mt-8">
          <p>Secured with military-grade encryption</p>
          <div className="flex justify-center mt-2 space-x-4">
            <span className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
              <span>256-bit SSL</span>
            </span>
            <span className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
              <span>GDPR Compliant</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}