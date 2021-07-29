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
    "detail": {
        "school_pk": "1",
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
        "school_pk": "1"
    }
}
```

# create grade
POST /api/v1/grade/
```json
{
    "act": "create",
    "detail":[
        {
            "name": "grade 1",
            "description": "this is description for grade 1"
        },
        {
            "name": "grade 2",
            "description": "this is description for grade 2"
        },
        {
            "name": "grade 3",
            "description": "this is description for grade 3"
        }
    ]
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
<!-- ```json
{
    "act": "update",
    "pks": ["1", "2", "3"],
    "detail": {
        "names": ["grade a1", "grade a2", "grade a3"],
        "description": ["this is description", ""]
    }
}
``` -->

```json
{
    "act": "update",
    "detail":[
        {
            "pk": "1",
            "name": "grade a1 (new name)",
            "description": "this is description for grade a1"
        },
        {
            "pk": "2",
            "name": "grade a2 (new name)",
            "description": "this is description for grade a2"
        },
        {
            "pk": "3",
            "name": "grade a3 (new name)",
            "description": "this is description for grade a3"
        }
    ]
}
```

# delete grade
POST /api/v1/grade/
```json
{
    "act": "delete",
    "detail": {
        "pk": "1"
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
        "grade" : "1",
        "first_name": "tom",
        "last_name": "tomus",
        "nick_name": "tom-tom"
    }
}
```

# update student
POST /api/v1/student/
<!-- ```json
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
```  -->
```json
{
    "act": "update",
    "detail": {
        "student_pk": "1",
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
        "student_pk": "1"
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
    "detail": {
        "parent_pk": "pk",
        "children_pk": [{"pk":"1"}, {"pk":"17"}, {"pk": "10"}]
    }
    // "parent_pk": "pk",
    // "children_pk": [{"pk":"1"}, {"pk":"17"}, {"pk": "10"}]
}
```

# update parent
POST /api/v1/parent/
```json
{
    "act": "update",
    "detail": {
        "parent_pk": "1",
        "first_name": "tom (this is new name [first_name])",
        "last_name": "tom-tom (this is new [last_name])"
    }
}
```

# delete parent
POST /api/v1/parent/
```json
{
    "act": "delete",
    "detail": {
        "parent_pk": "1"
    }
}
```

# reade parent
GET /api/v1/parent/

