import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Gluide - Academic Planning Platform',
  description: 'AI-powered academic planning and course guidance platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
