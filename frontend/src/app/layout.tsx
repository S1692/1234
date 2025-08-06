import '../styles/globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'Items App',
  description: 'Full stack template for items management',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900">
        {children}
      </body>
    </html>
  );
}
