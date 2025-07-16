# Settings / Flags

| Argument | Description | Default Setting | Environment Variable |
| :--- | :--- | :--- | :--- |
| `--debug` | Enable debug environment | `Off` | LT_DEBUG |
| `--ssl` | Whether to enable SSL | `Off` | LT_SSL |
| `--api-keys` | Enable the API key database for per-client rate limits when --req-limit is reached | `Do not use API keys` | LT_API_KEYS |
| `--require-api-key-origin` | Require API key for programmatic access, unless the request origin matches this domain | `No restriction on domain origin` | LT_REQUIRE_API_KEY_ORIGIN |
| `--require-api-key-secret` | Require API key for programmatic access, unless the client also sends a matching secret | `No secrets required` | LT_REQUIRE_API_KEY_SECRET |
| `--require-api-key-fingerprint` | Require API key for programmatic access, unless the client also matches a fingerprint | `No fingerprints required` | LT_REQUIRE_API_KEY_FINGERPRINT |
| `--under-attack` | Enable under-attack mode. When enabled, requests must be made with an API key. | `Off` | LT_UNDER_ATTACK |
| `--suggestions` | Allow user suggestions | `Off` | LT_SUGGESTIONS |
| `--disable-files-translation`| Disable file translation | `File translation is allowed` | LT_DISABLE_FILES_TRANSLATION |
| `--disable-web-ui` | Disable the web interface | `Web UI enabled` | LT_DISABLE_WEB_UI |
| `--update-models` | Update language models on startup | `Only triggered if no models are found` | LT_UPDATE_MODELS |
| `--metrics` | Enable the /metrics endpoint to export [Prometheus](https://prometheus.io/) usage metrics | `Off` | LT_METRICS |

# Configuration Parameters

| Argument | Description | Default Parameter | Environment Variable |
| :--- | :--- | :--- | :--- |
| `--host` | Set the host for the server to bind to | `127.0.0.1` | LT_HOST |
| `--port` | Set the port for the server to bind to | `5000` | LT_PORT |
| `--char-limit` | Set character limit | `No Limit` | LT_CHAR_LIMIT |
| `--req-limit` | Set the maximum number of requests per minute per client (outside of limits set by API keys) | `No Limit` | LT_REQ_LIMIT |
| `--req-limit-storage` | Storage URI for rate-limiting request data. See [Flask Limiter](https://flask-limiter.readthedocs.io/en/stable/configuration.html) | `memory://` | LT_REQ_LIMIT_STORAGE |
| `--req-time-cost` | Considers the time cost (in seconds) to rate limit requests. If a request takes 10s and this is 5, the request cost is 2 or the actual cost (whichever is higher). | `No time cost` | LT_REQ_TIME_COST |
| `--batch-limit` | Set the maximum number of texts to translate in a batch request | `No Limit` | LT_BATCH_LIMIT |
| `--ga-id` | Enable Google Analytics on the client API page by providing an ID | `Empty (no tracking)` | LT_GA_ID |
| `--frontend-language-source` | Set the default frontend language - source | `auto` | LT_FRONTEND_LANGUAGE_SOURCE |
| `--frontend-language-target` | Set the default frontend language - target | `locale` (matches site locale) | LT_FRONTEND_LANGUAGE_TARGET |
| `--frontend-timeout` | Set the frontend translation timeout | `500` | LT_FRONTEND_TIMEOUT |
| `--api-keys-db-path` | Use a specific path inside the container for the local database. Can be absolute or relative. | `db/api_keys.db` | LT_API_KEYS_DB_PATH |
| `--api-keys-remote` | Use this remote endpoint to query valid API keys instead of using the local DB | `Empty (uses local db instead)` | LT_API_KEYS_REMOTE |
| `--get-api-key-link` | Display a link in the UI to direct users to get an API key | `Empty (no link shown in UI)` | LT_GET_API_KEY_LINK |
| `--shared-storage` | Shared storage URI to be used for sharing data between multiple processes (e.g., when using gunicorn) | `memory://` | LT_SHARED_STORAGE |
| `--secondary` | Mark this instance as a secondary instance to avoid conflicts with the primary node in multi-node setups | `Primary node` | LT_SECONDARY |
| `--load-only` | Set available languages | `Empty (use all from argostranslate)` | LT_LOAD_ONLY |
| `--threads` | Set number of threads | `4` | LT_THREADS |
| `--metrics-auth-token` | Protect the /metrics endpoint by only allowing clients with a valid authorization bearer token | `Empty (no auth required)` | LT_METRICS_AUTH_TOKEN |
| `--url-prefix` | Add a prefix to the URL: example.com:5000/url-prefix/ | `/` | LT_URL_PREFIX |
