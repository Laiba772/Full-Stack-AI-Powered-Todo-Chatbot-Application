import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function PricingPage() {
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
            Our <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-cyan-400">Pricing</span>
          </h1>
          <p className="text-xl text-gray-400 mb-16 max-w-3xl mx-auto">
            Flexible plans to suit your productivity needs. All plans include our core features.
          </p>

          {/* Coming Soon Section */}
          <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-12 max-w-4xl mx-auto">
            <div className="flex flex-col items-center justify-center">
              <div className="w-24 h-24 bg-gradient-to-r from-purple-600 to-cyan-500 rounded-full flex items-center justify-center mb-8">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 className="text-3xl font-bold mb-4">Coming Soon</h2>
              <p className="text-gray-400 text-lg mb-8 max-w-md">
                We're crafting the perfect pricing plans to maximize your productivity. Check back soon for our launch offers!
              </p>
              <div className="flex space-x-4">
                <Link href="/">
                  <Button className="bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-700 hover:to-cyan-600 text-white px-6 py-3 rounded-lg transition-all">
                    Back to Home
                  </Button>
                </Link>
                <Link href="/#contact">
                  <Button className="bg-transparent border border-gray-600 text-white hover:bg-gray-800/50 px-6 py-3 rounded-lg transition-all">
                    Contact Sales
                  </Button>
                </Link>
              </div>
            </div>
          </div>

          {/* Placeholder for future pricing tiers */}
          <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { name: "Starter", price: "$9", features: ["Up to 5 projects", "Basic analytics", "Email support"] },
              { name: "Professional", price: "$29", features: ["Unlimited projects", "Advanced analytics", "Priority support"], highlighted: true },
              { name: "Enterprise", price: "Custom", features: ["White-label options", "Dedicated account manager", "Custom integrations"] }
            ].map((tier, index) => (
              <div 
                key={index} 
                className={`bg-gray-900/30 backdrop-blur-sm border rounded-xl p-8 opacity-50 ${tier.highlighted ? 'border-purple-500 ring-2 ring-purple-500/30' : 'border-gray-800'}`}
              >
                <h3 className="text-2xl font-bold mb-4">{tier.name}</h3>
                <div className="text-4xl font-bold mb-6">{tier.price}<span className="text-lg text-gray-400">/month</span></div>
                <ul className="space-y-3 mb-8">
                  {tier.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center">
                      <div className="w-2 h-2 bg-gray-600 rounded-full mr-3"></div>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
                <div className="h-10 bg-gray-800 rounded-lg"></div>
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