import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "HealthAI - AI-Powered Health Insurance Recommendations",
  description: "Get personalized health insurance recommendations using advanced AI technology. Compare 9 plans from 6 major insurers instantly.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-teal-600 bg-clip-text text-transparent">
                🏥 HealthAI
              </Link>
              <div className="flex gap-6">
                <Link href="/" className="text-gray-700 hover:text-blue-600 font-medium">
                  Home
                </Link>
                <Link href="/recommend" className="text-gray-700 hover:text-blue-600 font-medium">
                  Get Recommendations
                </Link>
              </div>
            </div>
          </div>
        </nav>
        {children}
        <footer className="bg-gray-900 text-white py-12">
          <div className="container mx-auto px-4 text-center">
            <p className="text-lg mb-4">🏥 HealthAI Recommender</p>
            <p className="text-gray-400 mb-4">AI-Powered Health Insurance Recommendations</p>
            <p className="text-sm text-gray-500">Powered by CrewAI + Ollama | © 2026</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
