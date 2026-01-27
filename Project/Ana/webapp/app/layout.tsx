import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '界隈分析ダッシュボード | 北米ビジネスクラスX発話分析',
  description: '北米ビジネスクラスに関するX投稿の界隈分析ダッシュボード',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body className="antialiased">{children}</body>
    </html>
  )
}
