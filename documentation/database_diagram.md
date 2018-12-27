# Database diagram
A database diagram drawn with [yuml.me](http://www.yuml.me). The diagram represents the relations of different database entities, some of which are still unimplemented. Note that the diagram is still in its beginning phases, and lacks information such as many-to-many junction tables and id-keys.

![database diagram](https://github.com/viljamiLatvala/reseptivihko/blob/master/documentation/database_diagram.png?raw=true "database diagram")

```%2F%2F Recipe Book, [Recipe| name:varchar;instruction:varchar;prep. time:integer],[User|username: varchar; passphrase:varchar],[Ingredient|name:varchar],[Rating|stars:Integer],[Category tag|name:varchar]
[User]1-*[Recipe]
[Recipe]1-*[Rating]
[Recipe]*-*[Ingredient]
[User]1-*[Rating]
[Category tag] *-* [Recipe]```
