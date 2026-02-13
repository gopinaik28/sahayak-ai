import Hero from "@/components/Hero";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Bot, Zap, Target, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-xl text-gray-600">Three simple steps to find your perfect insurance plan</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Card className="border-2 hover:shadow-lg transition-shadow">
              <CardContent className="pt-6">
                <div className="h-16 w-16 bg-blue-600 rounded-full flex items-center justify-center mb-4 mx-auto">
                  <Bot className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-2xl font-semibold mb-3 text-center">1. Tell Us About You</h3>
                <p className="text-gray-600 text-center">
                  Share your age, budget, health needs, and preferences through our simple form
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 hover:shadow-lg transition-shadow">
              <CardContent className="pt-6">
                <div className="h-16 w-16 bg-teal-600 rounded-full flex items-center justify-center mb-4 mx-auto">
                  <Zap className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-2xl font-semibold mb-3 text-center">2. AI Analyzes Plans</h3>
                <p className="text-gray-600 text-center">
                  Our 3 specialized AI agents analyze 9 plans from 6 major insurers
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 hover:shadow-lg transition-shadow">
              <CardContent className="pt-6">
                <div className="h-16 w-16 bg-green-600 rounded-full flex items-center justify-center mb-4 mx-auto">
                  <Target className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-2xl font-semibold mb-3 text-center">3. Get Recommendations</h3>
                <p className="text-gray-600 text-center">
                  Receive top 3 personalized plans with detailed comparison and reasoning
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="text-center mt-12">
            <Link href="/recommend">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-lg px-8 py-6">
                Start Now <ArrowRight className="ml-2" />
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
