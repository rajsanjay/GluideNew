import { API_ENDPOINTS } from '@/constants/api'

export default function Home() {
  const isTestMode = process.env.NEXT_PUBLIC_USE_TEST_MODE === 'true'

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-4">
          Welcome to Gluide
        </h1>

        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded">
          <p className="text-sm">
            <strong>Mode:</strong> {isTestMode ? 'Test Mode (Synthetic Data)' : 'Database Mode (Live Data)'}
          </p>
          <p className="text-sm">
            <strong>API URL:</strong> {process.env.NEXT_PUBLIC_API_URL}
          </p>
        </div>

        <div className="space-y-4">
          <section>
            <h2 className="text-2xl font-semibold mb-2">Features</h2>
            <ul className="list-disc list-inside space-y-1">
              <li>AI-powered transcript parsing</li>
              <li>Course recommendations</li>
              <li>Academic planning</li>
              <li>Counselor guidance tools</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-2">API Endpoints</h2>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Students: {API_ENDPOINTS.students}</li>
              <li>Transcripts: {API_ENDPOINTS.transcripts}</li>
              <li>Courses: {API_ENDPOINTS.courses}</li>
              <li>Counselors: {API_ENDPOINTS.counselors}</li>
            </ul>
          </section>
        </div>
      </div>
    </main>
  )
}
