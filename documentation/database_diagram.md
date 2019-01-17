## Database diagram and schema
### Diagram
A database diagram drawn with [yuml.me](https://yuml.me). The diagram represents the relations of different database entities.

![database diagram](https://github.com/viljamiLatvala/reseptivihko/blob/master/documentation/database_diagram.png?raw=true "database diagram")

### Schema
```sql
CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	username VARCHAR(64) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	role VARCHAR(64), 
	PRIMARY KEY (id)
);
CREATE TABLE tag (
	id INTEGER NOT NULL, 
	name VARCHAR(144) NOT NULL, 
	description VARCHAR(144), 
	PRIMARY KEY (id)
);
CREATE TABLE recipe (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	instruction VARCHAR(6000), 
	preptime INTEGER, 
	account_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
);
CREATE TABLE ingredient (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	line VARCHAR(500) NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES recipe (id)
);
CREATE TABLE tags (
	tag_id INTEGER NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	PRIMARY KEY (tag_id, recipe_id), 
	FOREIGN KEY(tag_id) REFERENCES tag (id), 
	FOREIGN KEY(recipe_id) REFERENCES recipe (id)
);

```