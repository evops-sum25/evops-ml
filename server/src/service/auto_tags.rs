use std::collections::HashMap;

use evops_models::{ApiResult, Tag};

impl crate::AppState {
    async fn call_auto_tags(
        &self,
        _description: String,
        _tags_name: Vec<&String>,
    ) -> ApiResult<Vec<String>> {
        let _treshhold = self.auto_tags_treshhold();
        Ok(Vec::new())
    }

    pub async fn get_tags_et(&self, description: String) -> ApiResult<Vec<String>> {
        let tags_list = {
            let mut db = self.db().lock().await;
            db.list_tags(None, None).await
        }?;
        let tags_map: HashMap<String, Tag> = tags_list
            .into_iter()
            .map(|tag: Tag| (tag.name.to_string(), tag))
            .collect();
        let correct_tags = self
            .call_auto_tags(description, tags_map.keys().clone().collect())
            .await?;
        let result: Vec<String> = correct_tags
            .iter()
            .map(|tag| tags_map.get(tag).unwrap().id.to_string())
            .collect();
        Ok(result)
    }
}
