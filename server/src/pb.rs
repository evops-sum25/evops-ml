tonic::include_proto!("evops.ml.v1");

use std::sync::Arc;

use bon::bon;
use eyre::Context as _;
use url::Url;

struct State {
    db: tokio::sync::Mutex<evops_db::Database>,
}

#[derive(Clone)]
pub struct AppState {
    // Here, the `State` struct, defined above, only gets wrapped in an `Arc` once.
    shared_state: Arc<self::State>,
    auto_tags_treshhold: Option<f32>,
}

#[bon]
impl AppState {
    #[builder]
    pub async fn new(database_url: &Url, auto_tags_treshhold: Option<f32>) -> eyre::Result<Self> {
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
            auto_tags_treshhold,
        })
    }
    pub fn auto_tags_treshhold(&self) -> Option<f32> {
        self.auto_tags_treshhold
    }
    pub fn db(&self) -> &tokio::sync::Mutex<evops_db::Database> {
        &self.shared_state.db
    }
}
