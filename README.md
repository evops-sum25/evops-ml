# EvOps / Machine Learning

## Build Instructions

1. Create a [`.env`](`/.env.example`).

   ```shell
   cp .env.example .env
   ```
2. Make sure you have python exetuble in your envirement with python modules pre-installed.
3. Run the server.
   ```shell
   cd server
   ```
   - Development mode:

     ```shell
     bacon
     ```

   - Release mode:

     ```shell
     cargo run --release
     ```

3. gRPC server should be available on http://0.0.0.0:50051 by
   default.
