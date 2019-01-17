## User stories

|As a/an | I want to    | so that   | related SQL-query | 
|--------|--------------|-----------|-------------------|
| user | be able to create an account | I can add recipes | `INSERT INTO account(username, password, role) VALUES(*name*,*pw*,'user')`
| user | be able to add recipes | other people can enjoy the recipes that I come up with |
`INSERT INTO recipe(name, preptime, instruction, account_id) VALUES ('*name*',*time*,'*instruction*,*id*)`
| user | be able to edit my recipe instructions, |I can correct any mistakes | `UPDATE recipe SET *column name* = *value* WHERE id=*id*`
| user | be able to edit my recipe ingredients, |I can adjust the amounts after coming up with better ones | `UPDATE ingredient SET line = '*line*' WHERE id = *id*`
| user | be able to anticipate how long it takes to make a dish by following a spesific recipe | I can manage my time better | `SELECT name,preptime FROM recipe` 
| user | search recipes by category | I can find recipes to suit my mood and taste | `SELECT * FROM recipe, tags, tag WHERE tags.recipe_id=recipe.id AND tags.tag_id = tag.id AND tag.name ='*Category*';`
| user | be able to delete a recipe | I don't have to share anything I dont want to online | `DELETE FROM recipe WHERE id = *id*`
| user | be able to see the most user tags | I can see whats popular | `SELECT tag.id, tag.name, COUNT(tag_id) AS count FROM tag LEFT JOIN tags ON tags.tag_id = tag.id GROUP BY tag.id, tag.name ORDER BY COUNT(tag_id) DESC`
| user | see statistics about added recipes | I can see how much information this site has | `SELECT COUNT(recipe.id), COALESCE (AVG(recipe.preptime),0), COUNT(DISTINCT account_id) FROM recipe`
| admin | Be able to edit any recipe on the platform | I can remove any explicit language | `UPDATE recipe SET instruction = *instruction* WHERE id = *id*` 
| admin | Be able to remove any recipe | I can weed out possible spam | `DELETE FROM recipe WHERE id = *id*`
| admin | Manage which recipes belong to which tag | Make sure tags contain only recipes that belog to it | `DELETE FROM tags WHERE tags.recipe_id = *id*`
| admin | add descriptive information for tags | I can describe what sorts of recipes a tag should contain | `UPDATE tag SET description='*Description* WHERE tag.id = *id*'`