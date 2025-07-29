# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG NODE_VERSION=22.0.0

FROM node:${NODE_VERSION}-alpine AS base

USER node
WORKDIR /usr/app/frontend

# docker build -t my-react-app-dev . --target dev
# docker run --name my_react_app_dev -d -v (pwd):/usr/app/frontend  -p 5173:5173 my-react-app-dev:latest
FROM base AS dev
# Expose the port that the application listens on.

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.npm to speed up subsequent builds.
# Leverage a bind mounts to package.json and package-lock.json to avoid having to copy them into
# into this layer.
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --include=dev

# Run the application as a non-root user.
# USER node
EXPOSE 5173

# Don't copy as we'll use a bind mount to pull everything in
CMD ["npm", "run", "dev", "--", "--host"]

# docker build -t my-react-app-build . --target build
FROM base AS build
WORKDIR /usr/app/frontend
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.npm to speed up subsequent builds.
# Leverage a bind mounts to package.json and package-lock.json to avoid having to copy them into
# into this layer.
# Run the application as a non-root user.
USER node

RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --include=dev

# Copy the rest of the source files into the image.
COPY . .
RUN ["npm", "run", "build"]

# docker build -t my-react-app .
# docker run -d --name my_react_app -p 83:80 my-react-app:latest
FROM nginx:stable-alpine AS prod
# Copy the rest of the source files into the image.
COPY --from=build /usr/app/frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
