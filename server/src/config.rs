use eyre::Context as _;
use url::Url;

const SERVER_PORT: &str = "SERVER_PORT";
const DATABASE_URL: &str = "DATABASE_URL";
const AUTO_TAGS_TRESHHOLD: &str = "AUTO_TAGS_TRESHHOLD";
const VENV_PATH: &str = "VENV_PATH";
const PYTHON_MODULES_PATH: &str = "PYTHON_MODULES_PATH";

pub struct Config {
    pub port: u16,
    pub database_url: Url,
    pub venv_path: String,
    pub python_modules_path: String,
    pub auto_tags_treshhold: Option<f32>,
}

pub fn from_env() -> eyre::Result<self::Config> {
    let port = {
        let raw = std::env::var(SERVER_PORT).wrap_err(SERVER_PORT)?;
        raw.parse::<u16>().wrap_err(const_format::formatcp!(
            "variable {SERVER_PORT} is malformed",
        ))?
    };
    let database_url = {
        let raw = std::env::var(DATABASE_URL).wrap_err(DATABASE_URL)?;
        raw.parse::<Url>().wrap_err(const_format::formatcp!(
            "variable {DATABASE_URL} is malformed"
        ))?
    };
    let auto_tags_treshhold = {
        let raw = std::env::var(AUTO_TAGS_TRESHHOLD).wrap_err(AUTO_TAGS_TRESHHOLD)?;
        raw.parse::<f32>()
            .wrap_err(const_format::formatcp!(
                "variable {AUTO_TAGS_TRESHHOLD} is malformed, using default value"
            ))
            .ok()
    };
    let venv_path = {
        let raw = std::env::var(VENV_PATH).wrap_err(VENV_PATH)?;
        raw.parse::<String>()
            .wrap_err(const_format::formatcp!("variable {VENV_PATH} is malformed"))?
    };
    let python_modules_path = {
        let raw = std::env::var(PYTHON_MODULES_PATH).wrap_err(PYTHON_MODULES_PATH)?;
        raw.parse::<String>().wrap_err(const_format::formatcp!(
            "variable {PYTHON_MODULES_PATH} is malformed"
        ))?
    };

    Ok(self::Config {
        port,
        database_url,
        venv_path,
        python_modules_path,
        auto_tags_treshhold,
    })
}
