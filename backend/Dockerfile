# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

FROM python:3.13.5-alpine3.22 AS base
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

FROM base AS setup
WORKDIR /usr/app/setup

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# docker build -t my-react-app-backend-dev . --target dev
# docker run --name my_react_app_backend_dev -p 8000:8000 -v (pwd):/usr/app/backend my-react-app-backend-dev:latest
FROM base AS dev
WORKDIR /usr/app/backend

# Enable venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Run the application as a non-root user.
USER appuser

# Copy over the venv
COPY --from=setup /opt/venv /opt/venv

# Copy the rest of the source files into the image.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0"]

# docker build -t my-react-app-backend-prod . --target prod
# docker run --name my_react_app_backend_dev -p 8000:8000 -d my-react-app-backend-prod:latest
FROM base AS prod
WORKDIR /usr/app/backend

# Enable venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Run the application as a non-root user.
USER appuser

# Copy over the venv
COPY --from=setup /opt/venv /opt/venv

# Copy the rest of the source files into the image.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0"]
