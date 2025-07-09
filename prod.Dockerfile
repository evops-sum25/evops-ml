FROM rust:1.87.0-bookworm AS builder
RUN apt-get update && apt-get install --assume-yes protobuf-compiler python3-dev
COPY ./ ./
RUN cargo install --path=server/

FROM debian:bookworm-slim
RUN apt-get update && \
    apt-get install -y libpq-dev python3 curl python3-dev && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ENV PATH="/root/.local/bin:$PATH"
COPY ./requirements.txt ./requirements.txt
RUN uv venv && \
    uv pip install --upgrade pip setuptools wheel && \
    uv pip install -r requirements.txt
COPY --from=builder /usr/local/cargo/bin/evops-ml /usr/local/bin/
ENTRYPOINT ["evops-ml"]
