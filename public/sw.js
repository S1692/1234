// This file is intentionally left almost empty.  In a real application you would
// implement caching strategies here for offline support.  See the Next.js
// documentation for guidance on integrating service workers.

self.addEventListener('install', event => {
  // Perform install steps, e.g. pre‑cache assets.
  console.log('[ServiceWorker] Install');
});

self.addEventListener('fetch', event => {
  // You can intercept network requests here to provide offline behaviour.
});