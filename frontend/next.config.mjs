/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',

  // This rewrites function is used to proxy requests in development.
  // It allows the frontend to make requests to '/api/...' which are then
  // forwarded to the actual backend service, avoiding CORS issues locally.
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // As requested, this proxies directly to the backend service for development.
        // In production, a similar rule should be configured on the host (e.g., Vercel rewrites).
        destination: 'https://1234-production-8dfb.up.railway.app/:path*',
      },
    ];
  },
};

export default nextConfig;
