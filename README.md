<h1>Today Progress</h1>

21/6
* make token for user
* make update for school

#

# create school
POST /api/v1/school/
```json
{
	"act": "create",
    "detail": {
        "name": "create-name",
        "description": "create-description"
    }
}
```

# update school
POST /api/v1/school/
```json
{
    "act": "update",
    "detail": {
        "name": "update-name",
        "description": "update-description"
    }
}
```

# read school
GET/ api/v1/school/


# delete school


# create grade
POST /api/v1/grade/
```json
{
    "act": "create",
    "detail": {
        "name": "create-grade",
        "detail": "create-description"
    }
}
```

# update grade
POST /api/v1/grade/
```json
{
    "act": "update",
    "detail": {
        "name": "update-grade",
        "description": "update-description"
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
        "first_name": "create-first_name",
        "last_name": "create-last_name",
        "nick_name": "create-nick_name"
    }
}
```

# update student
POST /api/v1/student/
```json
{
    "act": "update",
    "pk": "5",
    "detail": {
        "first_name": "update-first_name",
        "last_name": "update-last_name",
        "nick_name": "update-nick_name"
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

