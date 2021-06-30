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

# check user
GET /api/v1/user/

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


# create grade
POST /api/v1/grade/
```json
{
    "act": "create",
    "detail": {
        "name": "1",
        "detail": "this is description"
    }
}
```

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

# reade student
GET /api/v1/student/

# create parent
POST /api/v1/parent/
```json
{
    "act": "create",
    "detail": {
        "first_name": "create-first_name",
        "last_name": "create-last_name"
    }
}
```

# update parent
POST /api/v1/parent/
```json
{
    "act": "update",
    "detail": {
        "first_name": "update-first_name",
        "last_name": "update-last_name"
    }
}
```

# delete parent

# reade parent
GET /api/v1/parent/

