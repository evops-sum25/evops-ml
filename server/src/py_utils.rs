use pyo3::{Bound, Py, prelude::*, types::PyList};
use std::ffi::CString;
use std::path::{Path, PathBuf};

#[derive(Debug)]
pub struct PythonInterface {
    auto_tagger: AutoTagger,
}

pub struct PythonInterfaceBuilder {
    modules_path: PathBuf,
}

impl PythonInterfaceBuilder {
    pub fn new(
        modules_path: impl AsRef<Path>,
        _auto_tagger_treshhold: Option<f32>, // FIXME: Yep, I am to lazy to implement this now -_-
    ) -> Self {
        Self {
            modules_path: modules_path.as_ref().to_path_buf(),
        }
    }

    pub fn build(self) -> PyResult<PythonInterface> {
        tracing::debug!("Initializing python interface");
        self.initialize_python()?;

        tracing::debug!("Loading python modules");
        let result_r: PyResult<PythonInterface> = Python::with_gil(|py| {
            Ok(PythonInterface {
                auto_tagger: AutoTagger::initialize(py)?,
            })
        });
        let result = result_r?;
        tracing::debug!("Finished initializing python interface");
        Ok(result)
    }

    fn initialize_python(&self) -> PyResult<()> {
        pyo3::prepare_freethreaded_python();
        let abs_module_dir = self.modules_path.canonicalize().map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!(
                "Failed to resolve module directory: {}\nError: {}",
                self.modules_path.display(),
                e
            ))
        })?;

        Python::with_gil(|py| -> PyResult<()> {
            let code = format!(
                include_str!("py_utils/add_path.py"),
                abs_module_dir.display()
            );
            py.run(
                CString::new(code)
                    .expect("Failed to convert string")
                    .as_c_str(),
                None,
                None,
            )?;
            Ok(())
        })
    }
}

impl PythonInterface {
    pub fn predict_tags(
        &self,
        description: &str,
        tags_list: &Vec<&String>,
    ) -> PyResult<Vec<String>> {
        Python::with_gil(|py| self.auto_tagger.predict(py, description, tags_list))
    }
}

#[derive(Debug)]
struct AutoTagger {
    instance: Py<PyAny>,
}

impl AutoTagger {
    fn initialize(py: Python<'_>) -> PyResult<Self> {
        let module = py.import("auto_tagging")?;
        let class = module.getattr("ZeroShotTagger")?;
        let instance = class.call0()?.unbind();
        Ok(Self { instance })
    }

    fn predict(
        &self,
        py: Python<'_>,
        text: &str,
        tags_list: &Vec<&String>,
    ) -> PyResult<Vec<String>> {
        let result_buf = self
            .instance
            .bind(py)
            .call_method1("predict", (text, tags_list))?;
        let result: &Bound<'_, PyList> = result_buf.downcast()?;
        result.iter().map(|item| item.extract()).collect()
    }
}
