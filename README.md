<h1>Today Progress</h1>



# create user
Post /api/v1/user/
```json
{
    "act": "create",
    "detail": {
        "username": "tom",
        "password": "123"
    }
}
```
# get-token 
Post /api/v1/get-token/

# update user
Post /api/v1/user/
```json
{
    "act": "create",
    "old username": "tom",
    "detail": {
        "username": "oom",
        "password": "1234"
    }
}
```

# check user
GET /api/v1/user/

# delete user
Post /api/v1/user/
```json
{
    "act": "delete",
    "detail": {
        "username": "tom",
        "password": "123"
    }
}
```

# create school
POST /api/v1/school/
```json
{
    "act": "create",
    "detail": {
        "name": "school a",
        "description": "this is description"
    }
}
```

# update school
POST /api/v1/school/
```json
{
    "act": "update",
    "old name": "school a",
    "detail": {
        "name": "school b",
        "description": "this is description"
    }
}
```

# check school
GET/ api/v1/school/


# delete school
POST /api/v1/school/
```json
{
    "act": "delete",
    "detail": {
        "name": "school a",
        "description": "this is description"
    }
}
```

# create grade
POST /api/v1/grade/
```json
{
    "act": "create",
    "detail": {
        "name": [{"name":"1"}, {"name":"17"}, {"name": "10"}],
        "description": "this is description"
    }
}

```

<!-- modified
```json
{
    "act": "create",
    "detail": [{
        "name": "1",
        "description": "des1"
    },
    {
        "name": "2",
        "description": "des2"
    },
    {
        "name": "3",
        "description": "des3"
    }]
}
``` -->


# update grade
POST /api/v1/grade/
```json
{
    "act": "update",
    "old name": "1",
    "detail": {
        "name": "2",
        "description": "this is description"
    }
}
```

# delete grade
POST /api/v1/grade/
```json
{
    "act": "delete",
    "detail": {
        "name": "2",
        "description": "this is description"
    }
}
```

# read grade
GET /api/v1/grade/


# create student
POST /api/v1/student/
```json
{
    "act": "create",
    "detail": {
        "first_name": "tom",
        "last_name": "tomus",
        "nick_name": "tom-tom"
    }
}
```

# update student
POST /api/v1/student/
```json
{
    "act": "update",
    "old_first_name": "tom",
    "old_last_name": "tomus",
    "old_nick_name": "tom-tom",
    "detail": {
        "first_name": "bom",
        "last_name": "bomus",
        "nick_name": "bom-bom"
    }
}
``` 

# delete student
POST /api/v1/student/
```json
{
    "act": "delete",
    "detail": {
        "first_name": "tom",
        "last_name": "tomus",
        "nick_name": "tom-tom"
    }
}
```

# reade student
GET /api/v1/student/

# create parent
POST /api/v1/parent/
```json
{
    "act": "create",
    "detail": {
        "first_name": "tom",
        "last_name": "tom-tom"
    }
}
```

# add children
Post /api/v1/parent/
```json
{
    "act": "add children",
    "parent_pk": "pk",
    "children_pk": [{"pk":"1"}, {"pk":"17"}, {"pk": "10"}]
}
```

# update parent
POST /api/v1/parent/
```json
{
    "act": "update",
    "old_first_name": "bom",
    "old_last_name": "bom-bom",
    "detail": {
        "first_name": "update-first_name",
        "last_name": "update-last_name"
    }
}
```

# delete parent
POST /api/v1/parent/
```json
{
    "act": "delete",
    "detail": {
        "first_name": "tom",
        "last_name": "tom-tom"
    }
}
```

# reade parent
GET /api/v1/parent/

