use tonic::transport::Server;

use std::net::{Ipv4Addr, SocketAddr};

use crate::pb::AppState;
use crate::py_utils::PythonInterfaceBuilder;
use crate::shutdown::signal;

use crate::service::Service;

use const_format::formatcp;
use eyre::Context as _;
use tracing::{debug, info};
use tracing_subscriber::EnvFilter;
use tracing_subscriber::layer::SubscriberExt as _;
use tracing_subscriber::util::SubscriberInitExt as _;

mod config;
mod pb;
mod py_utils;
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

    let python_interface = PythonInterfaceBuilder::new(
        config.venv_path,
        config.python_modules_path,
        config.auto_tags_treshhold,
    )
    .build()
    .wrap_err("error building python interface")?;

    let state = {
        AppState::builder()
            .database_url(&config.database_url)
            .python_interface(python_interface)
            .build()
            .await?
    };

    let service = self::Service { state };

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
