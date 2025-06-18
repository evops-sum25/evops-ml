use eyre::Context as _;

const SERVER_PORT: &str = "SERVER_PORT";

pub struct Config {
    pub port: u16,
}

pub fn from_env() -> eyre::Result<self::Config> {
    let port = {
        let raw = std::env::var(SERVER_PORT).wrap_err(SERVER_PORT)?;
        raw.parse::<u16>().wrap_err(const_format::formatcp!(
            "variable {SERVER_PORT} is malformed",
        ))?
    };

    Ok(self::Config { port })
}
