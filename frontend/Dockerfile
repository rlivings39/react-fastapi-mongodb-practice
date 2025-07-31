# syntax=docker/dockerfile:1

ARG NODE_VERSION=22.0.0
ARG WORKDIR=/usr/app/frontend
ARG MOUNTS=--mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm

# Stage 1 - Just a base Node + Alpine Linux
FROM node:${NODE_VERSION}-alpine AS base
USER node

# Stage 2 - Dev environment launching the vite dev server
#
# Run
#
#   docker compose --profile dev up
#
# in the root folder to launch this with mongodb and the backend
#
# To launch manually
#
#   docker build -t my-react-app-dev . --target dev
#   docker run --name my_react_app_dev -d -v $(pwd)/index.html:/usr/app/frontend/index.html -v $(pwd)/src:/usr/app/frontend/src -p 5173:5173 my-react-app-dev:latest
FROM base AS dev
ARG MOUNTS
ARG WORKDIR
USER node
WORKDIR ${WORKDIR}
ENV NODE_ENV=development
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.npm to speed up subsequent builds.
# Leverage bind mounts to package.json and package-lock.json to avoid having to copy them into
# into this layer.
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --include=dev

# Run the application as a non-root user.
# USER node
EXPOSE 5173

# Copy the rest of the source files into the image.
COPY . .

CMD ["npm", "run", "dev", "--", "--host"]

# Stage 3 - Production build
# docker build -t my-react-app-build . --target build
FROM base AS build
ARG WORKDIR
ARG MOUNTS
# Run the application as a non-root user.
USER node
WORKDIR ${WORKDIR}
ENV NODE_ENV=production

# Don't mount package-lock.json as we want to overwrite it below
COPY package-lock.json package-lock.json
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --include=dev

# Copy the rest of the source files into the image.
COPY --chown=node:node . .
RUN ["npm", "run", "build"]

# Stage 4 - Production deployment with nginx
#
# Run
#
#   docker compose --profile prod up
#
# in the root folder to launch this with mongodb and the backend
#
# To launch manually
#
#   docker build -t my-react-app .
#   docker run -d --name my_react_app -p 83:80 my-react-app:latest
FROM nginx:stable-alpine AS prod
ARG WORKDIR
# Copy the rest of the source files into the image.
COPY --chown=root:root --from=build ${WORKDIR}/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
