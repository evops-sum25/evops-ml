#[derive(Debug, Default)]
pub struct MlServiceStruct {}

pub mod evops_ml {
    tonic::include_proto!("evops.ml.v1");
}

use evops_ml::ml_service_server::{MlService, MlServiceServer};
use evops_ml::{MlServiceAskRequest, MlServiceAskResponse};

use tonic::{Request, Response, Status, transport::Server};

#[tonic::async_trait]
impl MlService for MlServiceStruct {
    async fn ask(
        &self,
        _request: Request<MlServiceAskRequest>,
    ) -> Result<Response<MlServiceAskResponse>, Status> {

        println!("Received!");
        let req = _request.into_inner();
        Ok(Response::new(MlServiceAskResponse {
            name: req.name,
            description: req.description,
        }))
    }
}

#[tokio::main]
async fn main() -> eyre::Result<()> {
    let addr = "127.0.0.1:50051".parse()?;
    let server = MlServiceStruct::default();

    Server::builder()
        .add_service(MlServiceServer::new(server))
        .serve(addr)
        .await?;

    Ok(())
}
