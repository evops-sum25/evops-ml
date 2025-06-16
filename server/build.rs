use std::env;
use std::path::PathBuf;

fn main() -> eyre::Result<()> {
    let out_dir = PathBuf::from(env::var("OUT_DIR")?);
    tonic_build::configure()
        .file_descriptor_set_path(out_dir.join("ml-descriptor.bin"))
        .compile_protos(
            &["../server-ext/proto/evops/ml/v1/ml.proto"],
            &["../server-ext/proto/"],
        )?;
    Ok(())
}
