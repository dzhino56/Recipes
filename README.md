# Recipe Service

## Usage

All responses will have the form 

'''json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
'''

Subsequent response definitions will only detail the expected value of the 'data field'

### List all recipes

'GET /recipes'

**Response**

- '200 OK' on success

'''json
[
    {
        "recipe_id": "1",
        "author": "1",
        "datetime": "2021-03-28 19:16:59.729997",
        "recipe_name": "boiled eggs",
        "info": "really tasty boiled eggs",
        "food_type": "second course",
        "likes_count": "100",
        "hashtag_set": "egg, water"
    },
    {
        "recipe_id": "2",
        "author": "5",
        "datetime": "2021-03-28 19:23:22.913573",
        "recipe_name": "fried eggs",
        "info": "really tasty fried eggs",
        "food_type": "second course",
        "likes_count": "500",
        "hashtag_set": "egg, oil, sausage, cheese"
    }
]
'''

### Creating a new recipe

**Definition**

'POST /recipes'

**Arguments**

- '"author": int' unique identifier of user which is creating recipe
- '"recipe_name": string' name of recipe
- '"info": string' short description of recipe
- '"cooking_steps": string' description how to cook this dish
- '"food_type": string' type of food (for example: first course, second course, salad)
- '"hashtag_set": string' tags which user gives to food

**Response**

- '201 CREATED' on success

'''json
{
    "recipe_id": "1",
    "author": "1",
    "datetime": "2021-03-28 19:16:59.729997",
    "recipe_name": "boiled eggs",
    "info": "really tasty boiled eggs",
    "food_type": "second course",
    "likes_count": "100",
    "hashtag_set": "egg, water"
}
'''

### Lookup recipe details

**Definition**

'GET /recipes/<recipe_id>'

**Response**

- '404 Not Found' if the recipe does not exist
- '200 OK' on success

'''json
{
    "recipe_id": "1",
    "author": "1",
    "datetime": "2021-03-28 19:16:59.729997",
    "recipe_name": "boiled eggs",
    "info": "really tasty boiled eggs",
    "cooking_steps": "Pour oil on pan, Heat up pan, Break two eggs up on pan, Add salt and pepper",
    "food_type": "second course",
    "likes_count": "100",
    "hashtag_set": "egg, water"
    "status": "True"
}
'''

### Block recipe

**Definition**

'PUT /recipes/block_recipe'

**Arguments**

- '"recipe_id": int' unique identifier of recipe

**Response**

- '404 Not Found' if the recipe does not exist
- '200 OK' on success

'''json
{
    "recipe_id": "1",
    "author": "1",
    "datetime": "2021-03-28 19:16:59.729997",
    "recipe_name": "boiled eggs",
    "info": "really tasty boiled eggs",
    "cooking_steps": "Pour oil on pan, Heat up pan, Break two eggs up on pan, Add salt and pepper",
    "food_type": "second course",
    "likes_count": "100",
    "hashtag_set": "egg, water"
    "status": "False"
}
'''

### Unblock recipe

**Definition**

'PUT /recipes/unblock_recipe'

**Arguments**

- '"recipe_id": int' unique identifier of recipe

**Response**

- '404 Not Found' if the recipe does not exist
- '200 OK' on success

'''json
{
    "recipe_id": "1",
    "author": "1",
    "datetime": "2021-03-28 19:16:59.729997",
    "recipe_name": "boiled eggs",
    "info": "really tasty boiled eggs",
    "cooking_steps": "Pour oil on pan, Heat up pan, Break two eggs up on pan, Add salt and pepper",
    "food_type": "second course",
    "likes_count": "100",
    "hashtag_set": "egg, water"
    "status": "True"
}
'''

### Block User

**Definition**

'PUT /users/block_user'

**Arguments**

- '"user_id": int' unique identifier of user

**Response**

- '404 Not Found' if the user does not exist
- '200 OK' on success

'''json
{
    "user_id": "1",
    "nickname": "John",
    "status": "False",
    "favourite": "fried eggs, boiled eggs")
}
'''

### Unblock User

**Definition**

'PUT /users/unblock_user'

**Arguments**

- '"user_id": int' unique identifier of user

**Response**

- '404 Not Found' if the user does not exist
- '200 OK' on success

'''json
{
    "user_id": "1",
    "nickname": "John",
    "status": "True",
    "favourite": "fried eggs, boiled eggs")
}
'''

### Lookup details user profile

**Definition**

'GET /users/<user_id>'

**Response**

- '404 Not Found' if the user does not exist
- '200 OK' on success

'''json
{
    "user_id": "1",
    "nickname": "John",
    "status": "True",
    "favourite": "fried eggs, boiled eggs")
}
'''

### Lookup best ten users

**Definition**

'GET /users'

**Arguments**

- '"user_id": int' unique identifier of user

**Response**

- '200 OK' on success

'''json
[
    {
        "user_id": "1",
        "nickname": "John",
        "status": "True",
        "favourite": "fried potato, boiled potato")
    },
    {
        "user_id": "1",
        "nickname": "John",
        "status": "True",
        "favourite": "fried eggs, boiled eggs")
    }
]
'''

### Registration

**Definition**

'POST /users'

**Arguments**

- '"nickname": string' unique identifier of user

**Response**

- '201 Created' on success

'''json
{
    "user_id": "1",
    "nickname": "John",
    "status": "True",
    "favourite": "fried eggs, boiled eggs")
}
'''



























