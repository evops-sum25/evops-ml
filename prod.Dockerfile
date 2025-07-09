FROM rust:1.87.0-bookworm AS builder
RUN apt-get update && apt-get install --assume-yes protobuf-compiler python3.11-dev
COPY ./ ./
RUN cargo install --path=server/

FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
COPY --from=builder /usr/local/cargo/bin/evops-ml /usr/local/bin/
RUN apt-get update && apt-get install --assume-yes libpq-dev
WORKDIR /app/
COPY core/ ./core/
WORKDIR /app/core/
ENV UV_PROJECT_ENVIRONMENT=/usr/local/
RUN uv sync --frozen --no-dev
WORKDIR /app/server/
ENTRYPOINT ["evops-ml"]
