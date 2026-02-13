"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Loader2, CheckCircle, TrendingUp } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function RecommendPage() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<string | null>(null);
    const [formData, setFormData] = useState({
        age: "28",
        ped: "None",
        budget: "15000-20000",
        needs: "No room rent limit",
        preferences: "Wellness rewards",
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);

        try {
            const response = await fetch("/api/recommend", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (data.success) {
                setResult(data.recommendations);
            } else {
                setResult(data.recommendations || `Error: ${data.error || "Failed to get recommendations"}`);
            }
        } catch (error) {
            setResult(`Error: ${error instanceof Error ? error.message : "Unknown error occurred"}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-teal-50 py-12">
            <div className="container mx-auto px-4 max-w-5xl">
                <div className="text-center mb-12">
                    <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-teal-600 bg-clip-text text-transparent">
                        Get Your Recommendations
                    </h1>
                    <p className="text-xl text-gray-600">Fill in your details and let AI find the perfect insurance plan for you</p>
                </div>

                <Card className="mb-8 shadow-lg">
                    <CardHeader>
                        <CardTitle className="text-2xl">Your Details</CardTitle>
                        <CardDescription>Tell us about your insurance needs</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <Label htmlFor="age" className="text-base">Age</Label>
                                    <Input
                                        id="age"
                                        type="number"
                                        value={formData.age}
                                        onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                                        className="mt-2"
                                        required
                                    />
                                </div>
                                <div>
                                    <Label htmlFor="budget" className="text-base">Budget Range (₹/year)</Label>
                                    <Input
                                        id="budget"
                                        placeholder="e.g., 15000-20000"
                                        value={formData.budget}
                                        onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
                                        className="mt-2"
                                        required
                                    />
                                </div>
                            </div>

                            <div>
                                <Label htmlFor="ped" className="text-base">Pre-existing Conditions</Label>
                                <Input
                                    id="ped"
                                    placeholder="e.g., Diabetes, Hypertension or 'None'"
                                    value={formData.ped}
                                    onChange={(e) => setFormData({ ...formData, ped: e.target.value })}
                                    className="mt-2"
                                    required
                                />
                                <div className="flex flex-wrap gap-2 mt-2">
                                    <span className="text-sm text-gray-600">Common options:</span>
                                    {["None", "Diabetes", "Hypertension", "Thyroid", "Asthma", "Heart Disease"].map((condition) => (
                                        <button
                                            key={condition}
                                            type="button"
                                            onClick={() => setFormData({ ...formData, ped: condition })}
                                            className="px-3 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-blue-50 hover:border-blue-400 transition-colors"
                                        >
                                            {condition}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <Label htmlFor="needs" className="text-base">Specific Needs</Label>
                                <Textarea
                                    id="needs"
                                    placeholder="e.g., Maternity, OPD, No room rent limit"
                                    value={formData.needs}
                                    onChange={(e) => setFormData({ ...formData, needs: e.target.value })}
                                    rows={3}
                                    className="mt-2"
                                    required
                                />
                                <div className="flex flex-wrap gap-2 mt-2">
                                    <span className="text-sm text-gray-600">Common needs:</span>
                                    {["Maternity coverage", "No room rent limit", "OPD coverage", "Dental & Vision", "Mental health"].map((need) => (
                                        <button
                                            key={need}
                                            type="button"
                                            onClick={() => setFormData({ ...formData, needs: formData.needs.includes(need) ? formData.needs : (formData.needs ? formData.needs + ", " + need : need) })}
                                            className="px-3 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-teal-50 hover:border-teal-400 transition-colors"
                                        >
                                            + {need}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <Label htmlFor="preferences" className="text-base">Preferred Features</Label>
                                <Textarea
                                    id="preferences"
                                    placeholder="e.g., Wellness rewards, Quick claim settlement"
                                    value={formData.preferences}
                                    onChange={(e) => setFormData({ ...formData, preferences: e.target.value })}
                                    rows={3}
                                    className="mt-2"
                                    required
                                />
                                <div className="flex flex-wrap gap-2 mt-2">
                                    <span className="text-sm text-gray-600">Popular features:</span>
                                    {["Wellness rewards", "High CSR", "Quick claims", "Cashless hospitals", "No waiting period"].map((pref) => (
                                        <button
                                            key={pref}
                                            type="button"
                                            onClick={() => setFormData({ ...formData, preferences: formData.preferences.includes(pref) ? formData.preferences : (formData.preferences ? formData.preferences + ", " + pref : pref) })}
                                            className="px-3 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-green-50 hover:border-green-400 transition-colors"
                                        >
                                            + {pref}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <Button
                                type="submit"
                                className="w-full bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-700 hover:to-teal-700 text-white"
                                size="lg"
                                disabled={loading}
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                                        AI Analyzing Plans... (20-30 seconds)
                                    </>
                                ) : (
                                    <>
                                        <TrendingUp className="mr-2 h-5 w-5" />
                                        Get AI Recommendations
                                    </>
                                )}
                            </Button>
                        </form>
                    </CardContent>
                </Card>

                {result && (
                    <Card className="shadow-2xl border-2 border-blue-100">
                        <CardHeader className="bg-gradient-to-r from-blue-50 to-teal-50 border-b">
                            <div className="flex items-center gap-2">
                                <CheckCircle className="h-6 w-6 text-green-600" />
                                <CardTitle className="text-3xl">Your Personalized Recommendations</CardTitle>
                            </div>
                            <CardDescription className="text-base">
                                Powered by 3 AI agents analyzing {"{"}9 insurance plans{"}"}
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="pt-6">
                            <div className="markdown-content prose prose-lg max-w-none">
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    components={{
                                        h1: ({ children }) => (
                                            <h1 className="text-3xl font-bold mb-4 text-blue-600">{children}</h1>
                                        ),
                                        h2: ({ children }) => (
                                            <h2 className="text-2xl font-bold mb-3 mt-6 text-blue-700">{children}</h2>
                                        ),
                                        h3: ({ children }) => (
                                            <h3 className="text-xl font-semibold mb-2 mt-4 text-teal-600">{children}</h3>
                                        ),
                                        p: ({ children }) => (
                                            <p className="mb-3 text-gray-700 leading-relaxed">{children}</p>
                                        ),
                                        ul: ({ children }) => (
                                            <ul className="list-none space-y-2 mb-4">{children}</ul>
                                        ),
                                        li: ({ children }) => (
                                            <li className="flex items-start gap-2">
                                                <span className="text-green-500 mt-1">✓</span>
                                                <span>{children}</span>
                                            </li>
                                        ),
                                        table: ({ children }) => (
                                            <div className="overflow-x-auto my-6">
                                                <table className="min-w-full border-collapse border border-gray-300 shadow-md">
                                                    {children}
                                                </table>
                                            </div>
                                        ),
                                        thead: ({ children }) => (
                                            <thead className="bg-gradient-to-r from-blue-600 to-teal-600 text-white">
                                                {children}
                                            </thead>
                                        ),
                                        th: ({ children }) => (
                                            <th className="border border-gray-300 px-4 py-3 text-left font-semibold">
                                                {children}
                                            </th>
                                        ),
                                        td: ({ children }) => (
                                            <td className="border border-gray-300 px-4 py-3">
                                                {children}
                                            </td>
                                        ),
                                        tr: ({ children, ...props }) => {
                                            const isEven = props.node && 'position' in props.node && typeof props.node.position === 'number' && props.node.position % 2 === 0;
                                            return (
                                                <tr className={isEven ? "bg-gray-50" : "bg-white"}>
                                                    {children}
                                                </tr>
                                            );
                                        },
                                        blockquote: ({ children }) => (
                                            <blockquote className="border-l-4 border-blue-500 pl-4 italic bg-blue-50 py-2 my-4">
                                                {children}
                                            </blockquote>
                                        ),
                                        strong: ({ children }) => (
                                            <strong className="font-bold text-blue-700">{children}</strong>
                                        ),
                                        code: ({ children }) => (
                                            <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono">
                                                {children}
                                            </code>
                                        ),
                                    }}
                                >
                                    {result}
                                </ReactMarkdown>
                            </div>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    );
}
