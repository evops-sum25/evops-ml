use std::collections::HashMap;

use evops_models::{ApiResult, Tag};

use uuid::Uuid;

impl crate::AppState {
    async fn call_auto_tags(
        &self,
        description: String,
        tags_name: Vec<&String>,
    ) -> ApiResult<Vec<String>> {
        Ok(Vec::new())
    }

    pub async fn get_tags_et(&self, description: String) -> ApiResult<Vec<Uuid>> {
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
        let result = correct_tags.into_iter().map(|tag| tag);
        Ok(Vec::new())
    }
}
