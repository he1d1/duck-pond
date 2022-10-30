# Duck Pond backend

## Endpoints

### GET `/entries`

Gets a list of all the duck ponds in the database.

### POST `/entry/<id>/new`

Creates a new duck pond entry.

JSON body arguments:
* `name` - reqiured
* `location` - required, in the form 
    ```json
    {
        "lat": -1.2345,
        "long": 33.56643
    }
    ```
* `imageURL`

Votes will be initialised as zero.

Return sample:

```json
{
    "id": "uuid"
}
```

### PATCH `/entry/<id>`

Updates an entry with the ID `id`.

JSON body arguments:
* `name`
* `location`
* `imageURL`
* `votes`

### GET `/entry/<id>`

Gets the JSON of the pond.

```json
{
    "id": "uuid",
    "name": "The Pondiest Pond",
    "location": {
        "lat": -1.2345,
        "long": 33.56643
    },
    "imageURL": "https://example.com"
}
```

### DELETE `/entry/<id>`

Deletes the entry with ID `id`