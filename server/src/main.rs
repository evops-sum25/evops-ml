use tonic::transport::Server;

use std::net::{Ipv4Addr, SocketAddr};

use crate::service::MlService;
use crate::shutdown::signal;

use std::sync::Arc;

use bon::bon;
use eyre::Context as _;
use url::Url;

use const_format::formatcp;
use tracing::{debug, info};
use tracing_subscriber::EnvFilter;
use tracing_subscriber::layer::SubscriberExt as _;
use tracing_subscriber::util::SubscriberInitExt as _;

mod config;
mod pb;
mod service;
mod shutdown;

#[tokio::main]
async fn main() -> eyre::Result<()> {
    color_eyre::install()?;
    let dotenv_path = dotenvy::dotenv().ok();
    self::init_logging();

    if let Some(path) = dotenv_path {
        debug!("found .env: {}", path.display());
    } else {
        debug!(".env not found, using environment variables");
    }
    let config = self::config::from_env()?;
    let service = self::MlService::default();

    let addr = SocketAddr::new(Ipv4Addr::UNSPECIFIED.into(), config.port);
    info!("listening on port {}", config.port);
    Server::builder()
        .add_service(pb::ml_service_server::MlServiceServer::new(service))
        .serve_with_shutdown(addr, self::signal())
        .await?;

    Ok(())
}

fn init_logging() {
    let env_filter = {
        EnvFilter::try_from_default_env().unwrap_or_else(|_| {
            EnvFilter::new(formatcp!(
                "info,tower_http=trace,{}=trace",
                env!("CARGO_CRATE_NAME"),
            ))
        })
    };

    let fmt_layer = {
        tracing_subscriber::fmt::layer()
            .pretty()
            .with_file(false)
            .with_line_number(false)
            .with_target(false)
            .without_time()
    };

    tracing_subscriber::registry()
        .with(env_filter)
        .with(fmt_layer)
        .init();
}

struct State {
    db: tokio::sync::Mutex<evops_db::Database>,
}

#[derive(Clone)]
pub struct AppState {
    // Here, the `State` struct, defined above, only gets wrapped in an `Arc` once.
    shared_state: Arc<self::State>,
}

#[bon]
impl AppState {
    #[builder]
    pub async fn new(database_url: &Url) -> eyre::Result<Self> {
        let db = {
            evops_db::Database::establish_connection(database_url)
                .await
                .wrap_err("error connecting to db")?
        };
        Ok(Self {
            shared_state: {
                Arc::new(self::State {
                    db: tokio::sync::Mutex::new(db),
                })
            },
        })
    }

    /// Does the same thing as `self.clone()`,
    /// but the method name explicitly tells that the new object
    /// will point to the same memory location.
    #[must_use]
    pub fn arc_clone(&self) -> Self {
        Self {
            shared_state: Arc::clone(&self.shared_state),
        }
    }
}
