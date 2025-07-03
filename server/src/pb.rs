tonic::include_proto!("evops.ml.v1");

use std::sync::Arc;

use crate::py_utils::PythonInterface;
use bon::bon;
use eyre::Context as _;
use url::Url;

struct State {
    db: tokio::sync::Mutex<evops_db::Database>,
    python_interface: tokio::sync::Mutex<PythonInterface>,
}

#[derive(Clone)]
pub struct AppState {
    // Here, the `State` struct, defined above, only gets wrapped in an `Arc` once.
    shared_state: Arc<self::State>,
}

#[bon]
impl AppState {
    #[builder]
    pub async fn new(database_url: &Url, python_interface: PythonInterface) -> eyre::Result<Self> {
        let db = {
            evops_db::Database::establish_connection(database_url)
                .await
                .wrap_err("error connecting to db")?
        };
        Ok(Self {
            shared_state: Arc::new(self::State {
                db: tokio::sync::Mutex::new(db),
                python_interface: tokio::sync::Mutex::new(python_interface),
            }),
        })
    }

    pub fn python_interface(&self) -> &tokio::sync::Mutex<PythonInterface> {
        &self.shared_state.python_interface
    }

    pub fn db(&self) -> &tokio::sync::Mutex<evops_db::Database> {
        &self.shared_state.db
    }
}
