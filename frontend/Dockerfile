# Build stage
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# We can inject production API URL here if needed: ENV VITE_API_URL=https://api.yourdomain.com
RUN npm run build

# Production stage
FROM nginx:alpine
# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html
# Notice: For a real deployment, provide an nginx.conf to route /api traffic to the backend, or rely on absolute VITE_API_URL.
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
