"use client";

import type { Metadata } from "next";
import { Geist_Mono } from "next/font/google"; // Correct imports
import "./globals.css";
import { BetterAuthProvider } from "@/components/auth/BetterAuthProvider";
import { useEffect, useState } from "react";
import { isDomainAllowed } from "@/lib/domainCheck";

import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const metadata: Metadata = {
  title: "Todo App | Manage Your Tasks",
  description: "A simple and efficient task management application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [domainCheckPassed, setDomainCheckPassed] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const currentDomain = window.location.host;
      const allowedDomainsEnv = process.env.NEXT_PUBLIC_CHAT_DOMAIN_KEY;

      if (!isDomainAllowed(currentDomain, allowedDomainsEnv)) {
        setError("Access Denied: This chat is not available on this domain.");
      } else {
        setDomainCheckPassed(true);
      }
    } else {
      setDomainCheckPassed(true); // SSR fallback
    }
  }, []);

  if (error) {
    return (
      <html lang="en">
        <body
          className={`${inter.variable} ${geistMono.variable} antialiased flex items-center justify-center h-screen bg-gray-100`}
        >
          <div className="text-red-600 text-lg p-4 bg-white rounded-lg shadow-md">
            {error}
          </div>
        </body>
      </html>
    );
  }

  if (!domainCheckPassed) {
    return (
      <html lang="en">
        <body
          className={`${inter.variable} ${geistMono.variable} antialiased flex items-center justify-center h-screen bg-gray-100`}
        >
          <div className="text-gray-600 text-lg">Verifying domain access...</div>
        </body>
      </html>
    );
  }

  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${geistMono.variable} antialiased`}
      >
        <BetterAuthProvider>{children}</BetterAuthProvider>
      </body>
    </html>
  );
}
