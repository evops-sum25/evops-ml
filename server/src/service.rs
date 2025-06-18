use tonic::{Request, Response, Status};

use crate::evops_ml::ml_service_server::MlService;
use crate::evops_ml::{MlServiceAskRequest, MlServiceAskResponse};

#[derive(Debug, Default)]
pub struct MlServiceStruct;

#[tonic::async_trait]
impl MlService for MlServiceStruct {
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
