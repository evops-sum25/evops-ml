use std::collections::HashMap;

use evops_models::{ApiResult, Tag};

impl crate::AppState {
    async fn call_auto_tags(
        &self,
        description: String,
        tags_name: Vec<&String>,
    ) -> ApiResult<Vec<String>> {
        Ok(Vec::new())
    }

    pub async fn get_tags(&self, description: String) -> ApiResult<Vec<String>> {
        let tags_list = {
            let mut db = self.shared_state.db.lock().await;
            db.list_tags(None, None).await
        }?;
        let tags_map: HashMap<String, Tag> = tags_list
            .into_iter()
            .map(|tag: Tag| (tag.name.to_string(), tag))
            .collect();
        let correct_tags = self
            .call_auto_tags(description, tags_map.keys().clone().collect())
            .await?;
        Ok(Vec::new())
    }
}
