# Frontend


## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Project Structure

- **`app/`**: Next.js App Router directory. Contains pages and layouts.
- **`proxies/`**: Contains proxy/middleware logic.
    - **`proxy.ts`**: Clerk authentication middleware configuration.
- **`utils/`**: Utility functions (e.g., `apiTester.ts`).
- **`public/`**: Static assets.
- **`proxy.ts`**: Entry point for Next.js Proxy (Middleare). Re-exports configuration from `proxies/proxy.ts`.

## Tech Stack
- **Framework**: Next.js 16 (Turbopack)
- **Styling**: Tailwind CSS 4
- **Auth**: Clerk
- **Language**: TypeScript

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
