# syntax=docker/dockerfile:1

# Python venv location and updated path
ARG VENV=/opt/venv
ARG VENV_PATH="$VENV/bin:$PATH"
ARG USER=appuser
ARG PORT=8000

# Stage 1 - Just build an image with Python and Alpine Linux
FROM python:3.13.5-alpine3.22 AS base
ARG VENV
ARG VENV_PATH
ARG USER
ARG PORT
RUN addgroup -S appgroup && adduser -S ${USER} -G appgroup

# Stage 2 - Setup to create venv and install packages
FROM base AS setup
WORKDIR /usr/app/setup
ENV VIRTUAL_ENV=${VENV}
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="${VENV_PATH}"

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Stage 3 - Create a dev environment with venv from setup
#
# Run
#
#   docker compose --profile dev up
#
# in the root folder to launch this with mongodb
FROM base AS dev
WORKDIR /usr/app/backend

# Enable venv
ENV VIRTUAL_ENV=${VENV}
ENV PATH="${VENV_PATH}"

# Run the application as a non-root user.
USER ${USER}

# Copy over the venv
COPY --from=setup ${VENV} ${VENV}

# Copy the rest of the source files into the image.
COPY . .

# Expose the port that the application listens on.
EXPOSE ${PORT}

# Run the application.
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0"]

# Stage 4 - Production environment
#
# Run
#
#   docker compose --profile prod up
#
# in the root folder to launch this with mongodb
FROM base AS prod
WORKDIR /usr/app/backend

# Enable venv
ENV VIRTUAL_ENV=${VENV}
ENV PATH="${VENV_PATH}"

# Run the application as a non-root user.
USER ${USER}

# Copy over the venv
COPY --from=setup ${VENV} ${VENV}

# Copy the rest of the source files into the image.
COPY . .

# Expose the port that the application listens on.
EXPOSE ${PORT}

# Run the application.
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0"]
