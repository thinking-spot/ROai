import Head from 'next/head'
import Link from 'next/link'

export default function Home() {
  return (
    <>
      <Head>
        <title>AI ROI Analytics Platform</title>
        <meta name="description" content="Measure and demonstrate ROI from AI tool implementations" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              AI ROI Analytics Platform
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Measure and demonstrate real ROI from your AI tool implementations
            </p>

            <div className="grid md:grid-cols-3 gap-8 mt-12">
              <FeatureCard
                title="Integration Layer"
                description="Connect to GSuite, Microsoft 365, Jira, GitHub, and AI platforms"
                icon="🔗"
              />
              <FeatureCard
                title="Attribution Engine"
                description="Statistical analysis to prove causal relationship between AI usage and metrics"
                icon="📊"
              />
              <FeatureCard
                title="Multi-View Dashboards"
                description="Role-based dashboards for CFO, CHRO, CIO, and department heads"
                icon="📈"
              />
            </div>

            <div className="mt-12 space-x-4">
              <Link href="/login" className="inline-block bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition">
                Sign In
              </Link>
              <Link href="/register" className="inline-block bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition border border-primary-600">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}

function FeatureCard({ title, description, icon }: { title: string; description: string; icon: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}
