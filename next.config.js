/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable the experimental app directory for Next.js 13+
  experimental: {
    appDir: true,
  },
  reactStrictMode: true,
  swcMinify: true,
};

module.exports = nextConfig;