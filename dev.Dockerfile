FROM lukemathwalker/cargo-chef:0.1.71-rust-1.87.0-slim-bookworm AS chef
RUN apt-get update && apt-get install --assume-yes libpq-dev protobuf-compiler
WORKDIR /app/

FROM chef AS planner
COPY ./ ./
WORKDIR server/
RUN cargo chef prepare

FROM chef AS dev
COPY --from=planner /app/server/recipe.json ./
RUN cargo chef cook
COPY ./ ./
CMD ["cargo", "run"]
