"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles, Zap, Target } from "lucide-react";
import Link from "next/link";

// Static particle positions to avoid hydration mismatch
const particles = [
    { id: 0, left: 15, top: 25, duration: 4.2, delay: 0.3 },
    { id: 1, left: 85, top: 65, duration: 3.8, delay: 1.2 },
    { id: 2, left: 45, top: 15, duration: 4.5, delay: 0.8 },
    { id: 3, left: 70, top: 80, duration: 3.5, delay: 1.5 },
    { id: 4, left: 20, top: 55, duration: 4.0, delay: 0.5 },
    { id: 5, left: 60, top: 35, duration: 3.9, delay: 1.0 },
    { id: 6, left: 35, top: 70, duration: 4.3, delay: 0.7 },
    { id: 7, left: 90, top: 20, duration: 3.7, delay: 1.3 },
    { id: 8, left: 10, top: 45, duration: 4.1, delay: 0.4 },
    { id: 9, left: 75, top: 55, duration: 3.6, delay: 1.1 },
    { id: 10, left: 50, top: 85, duration: 4.4, delay: 0.6 },
    { id: 11, left: 25, top: 30, duration: 3.8, delay: 1.4 },
    { id: 12, left: 80, top: 40, duration: 4.2, delay: 0.9 },
    { id: 13, left: 40, top: 60, duration: 3.5, delay: 1.2 },
    { id: 14, left: 65, top: 10, duration: 4.0, delay: 0.5 },
    { id: 15, left: 30, top: 75, duration: 3.9, delay: 1.0 },
    { id: 16, left: 85, top: 50, duration: 4.3, delay: 0.8 },
    { id: 17, left: 15, top: 90, duration: 3.7, delay: 1.5 },
    { id: 18, left: 55, top: 20, duration: 4.1, delay: 0.7 },
    { id: 19, left: 5, top: 65, duration: 3.6, delay: 1.1 },
];

export default function Hero() {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-blue-600 via-blue-700 to-teal-600">
            {/* Animated background elements */}
            <div className="absolute inset-0 opacity-20">
                {particles.map((particle) => (
                    <motion.div
                        key={particle.id}
                        className="absolute h-2 w-2 bg-white rounded-full"
                        style={{
                            left: `${particle.left}%`,
                            top: `${particle.top}%`,
                        }}
                        animate={{
                            y: [0, -30, 0],
                            opacity: [0.3, 0.8, 0.3],
                        }}
                        transition={{
                            duration: particle.duration,
                            repeat: Infinity,
                            delay: particle.delay,
                        }}
                    />
                ))}
            </div>

            <div className="container mx-auto px-4 relative z-10">
                <div className="max-w-4xl mx-auto text-center text-white">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                    >
                        <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
                            Find Your Perfect
                            <span className="block bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">
                                Health Insurance Plan
                            </span>
                        </h1>
                    </motion.div>

                    <motion.p
                        className="text-xl md:text-2xl mb-8 text-blue-100"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                    >
                        AI-Powered Personalized Recommendations in Minutes
                    </motion.p>

                    <motion.div
                        className="flex flex-col sm:flex-row gap-4 justify-center mb-12"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.4 }}
                    >
                        <Link href="/recommend">
                            <Button size="lg" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold text-lg px-8 py-6">
                                Get Started <ArrowRight className="ml-2 h-5 w-5" />
                            </Button>
                        </Link>
                    </motion.div>

                    <motion.div
                        className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.6 }}
                    >
                        <div className="flex items-center justify-center gap-2">
                            <Sparkles className="h-5 w-5 text-yellow-300" />
                            <span className="text-lg">Smart AI Analysis</span>
                        </div>
                        <div className="flex items-center justify-center gap-2">
                            <Zap className="h-5 w-5 text-yellow-300" />
                            <span className="text-lg">9 Insurance Plans</span>
                        </div>
                        <div className="flex items-center justify-center gap-2">
                            <Target className="h-5 w-5 text-yellow-300" />
                            <span className="text-lg">Instant Results</span>
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Scroll indicator */}
            <motion.div
                className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
            >
                <div className="h-12 w-8 border-2 border-white/50 rounded-full flex items-start justify-center p-2">
                    <div className="h-2 w-2 bg-white rounded-full" />
                </div>
            </motion.div>
        </section>
    );
}
