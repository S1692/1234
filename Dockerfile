FROM node:18-alpine AS base
WORKDIR /app

# Install pnpm globally.  We'll use pnpm to manage dependencies for faster and
# more reliable installs.  The `corepack` utility comes bundled with recent
# Node.js versions but isn't available in Alpine; install pnpm via npm.
RUN npm install -g pnpm

FROM base AS builder
WORKDIR /app
COPY package.json ./
# Copy the lock file if present.  If you generate a pnpm-lock.yaml locally it
# should be included here for reproducible builds.  Otherwise `pnpm install`
# will generate a lock file on first run.
COPY pnpm-lock.yaml* ./

# Install dependencies using pnpm.  Using `--frozen-lockfile` ensures that
# dependencies match your lock file if present.
RUN pnpm install --frozen-lockfile || pnpm install

COPY . .
RUN pnpm run build

FROM base AS runtime
WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["pnpm", "start"]