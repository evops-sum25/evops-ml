use tonic::{Request, Response, Status};

use crate::pb::ml_service_server::MlService as Service; // I am not the best at naming, so ):
use crate::pb::{MlServiceGetTagsRequest, MlServiceGetTagsResponse};

use tracing::debug;

pub struct MlService {
    state: crate::AppState,
}

mod auto_tags;

#[tonic::async_trait]
impl Service for self::MlService {
    async fn get_tags(
        &self,
        request: Request<MlServiceGetTagsRequest>,
    ) -> Result<Response<MlServiceGetTagsResponse>, Status> {
        let req = request.into_inner();
        debug!("Received request for: {}", req.description);
        let tags_ids = crateget_tags(req.description)?;
        Ok(Response::new(MlServiceGetTagsResponse { tags_ids }))
    }
}
