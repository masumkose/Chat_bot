# frontend/Dockerfile

# 1. Build Stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# This command builds your Next.js app for production
RUN npm run build

# 2. Production Stage
FROM node:20-alpine
WORKDIR /app
# Only copy necessary production dependencies
COPY --from=builder /app/package*.json ./
RUN npm install --omit=dev

# Copy the built app from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/next.config.ts ./next.config.ts

EXPOSE 3000
# The command to run the production server
CMD ["npm", "start"]