use std::collections::HashMap;

use evops_models::Tag;
use eyre::Context as _;

impl crate::AppState {
    async fn call_auto_tags(
        &self,
        description: String,
        tags_name: Vec<&String>,
    ) -> eyre::Result<Vec<String>> {
        tracing::debug!("Got a request for {}", description);
        let python_interface = self.python_interface().lock().await;
        let result = python_interface
            .predict_tags(description.as_str(), &tags_name)
            .wrap_err("error calling python auto tagger")?;
        tracing::debug!("Answer: {:?}", result);
        Ok(result)
    }

    pub async fn get_tags_et(&self, description: String) -> eyre::Result<Vec<String>> {
        let tags_list = {
            let mut db = self.db().lock().await;
            db.list_tags(None, None).await
        }?;
        if tags_list.len() < 1 {
            return Ok(Vec::new());
        }
        let tags_map: HashMap<String, Tag> = tags_list
            .into_iter()
            .map(|tag: Tag| (tag.name.to_string(), tag))
            .collect();
        let correct_tags = self
            .call_auto_tags(description, tags_map.keys().clone().collect())
            .await?;
        let result: Vec<String> = correct_tags
            .iter()
            .filter_map(|tag| {
                tags_map.get(tag).map(|val| val.id.to_string()).or_else(|| {
                    tracing::debug!("Tag '{}' not found - skipping", tag);
                    None
                })
            })
            .collect();
        Ok(result)
    }
}
