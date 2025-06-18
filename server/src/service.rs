use tonic::{Request, Response, Status};

use crate::evops_ml::ml_service_server::MlService as Service; // I am not the best at naming, so ):
use crate::evops_ml::{MlServiceAskRequest, MlServiceAskResponse};

#[derive(Debug, Default)]
pub struct MlService;

#[tonic::async_trait]
impl Service for self::MlService {
    async fn ask(
        &self,
        request: Request<MlServiceAskRequest>,
    ) -> Result<Response<MlServiceAskResponse>, Status> {
        let req = request.into_inner();
        println!("Received request for: {}", req.name);

        let response = MlServiceAskResponse {
            name: req.name,
            description: req.description,
        };

        Ok(Response::new(response))
    }
}
