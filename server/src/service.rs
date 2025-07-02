use tonic::{Request, Response, Status};
use tracing::debug;

use crate::pb::ml_service_server::MlService;
use crate::pb::{MlServiceGetTagsRequest, MlServiceGetTagsResponse};
use evops_models::ApiError;

mod auto_tags;

pub struct Service {
    pub state: crate::AppState,
}

#[tonic::async_trait]
impl MlService for Service {
    async fn get_tags(
        &self,
        request: Request<MlServiceGetTagsRequest>,
    ) -> Result<Response<MlServiceGetTagsResponse>, Status> {
        let req = request.into_inner();
        debug!("Received request for: {}", req.description);
        let tags_ids = self.state.get_tags_et(req.description).await?;

        Ok(Response::new(MlServiceGetTagsResponse { tags_ids }))
    }
}
