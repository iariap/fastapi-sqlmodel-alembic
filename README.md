# funspark

## Generic CRUD

The GenericCRUD class provides a set of standard CRUD (Create, Read, Update, Delete) operations for a given SQLAlchemy model. This class simplifies the process of interfacing with the database by abstracting common operations.

### Usage

To use the GenericCRUD class, you need to define a SQLAlchemy model and corresponding Pydantic schema classes for create and update operations. Here's an example for a hypothetical Item model:

```python
from sqlmodel import SQLModel

from base.models import TimestampModel, UUIDModel


class SongBase(SQLModel):
    name: str
    artist: str
    year: int | None = None

class Song(SongBase, TimestampModel, UUIDModel, table=True):
    ...

class SongCreate(SongBase):
    ...

class SongUpdate(SongBase):
    ...

```

### Creating a CRUD Object

```python
item_crud = GenericCRUD[Item, ItemCreate, ItemUpdate](Item)
```

## Generic Router

### Overview

The `GenericCrudRouter` class is a customizable router for creating CRUD (Create, Read, Update, Delete) endpoints in a FastAPI application. It simplifies the process of setting up standard CRUD operations for a given SQLAlchemy model and corresponding Pydantic schemas.

### Features

- **Automated Route Creation**: Automatically creates standard CRUD routes for a specified SQLAlchemy model.
- **Customizable**: Easily define custom Pydantic schemas for different operations (Create, Read, Update).
- **Pagination**: Supports pagination for retrieving lists of items.

### How It Works

The `GenericCrudRouter` class takes a SQLAlchemy model and Pydantic schema classes as inputs and generates standard CRUD routes. These routes include:

- `GET /<model_name>s`: Retrieve a paginated list of items.
- `GET /<model_name>s/{id}`: Retrieve a single item by ID.
- `POST /<model_name>s`: Create a new item.
- `PUT /<model_name>s/{id}`: Update an existing item by ID.
- `DELETE /<model_name>s/{id}`: Delete an existing item by ID.

### Usage

To use the `GenericCrudRouter`, import the class and create an instance by passing the SQLAlchemy model and the Pydantic schema classes for the Create, Update, and Read operations.

Here is an example of using the `GenericCrudRouter` for a `Song` model:

```python
from base.routers import GenericCrudRouter
from songs.models import Song, SongCreate, SongUpdate

# Create a CRUD router for the Song model
router = GenericCrudRouter(Song, Song, SongUpdate, SongCreate)
```

## Setting Up Ruff for Code Linting

### Installation

To improve code quality and consistency, we use `ruff` as a linting tool in our project. Follow these steps to install and configure `ruff`:

### Configuring Pre-Commit Hook

After installing project dependencies, you need to set it up as a pre-commit hook:

**Install the Pre-Commit Hook**: Run the following command to set up the git hook scripts:

```bash
pre-commit install
```

This command installs the pre-commit hook into your `.git/hooks/pre-commit`.

### Running Ruff

With the pre-commit hook installed, `ruff` will automatically run on the staged files each time you commit. To manually run `ruff` on all files in the project, you can use the following command:

```bash
pre-commit run ruff --all-files
```

### Updating Ruff Version

To update to a newer version of `ruff`, change the `rev` value in the `.pre-commit-config.yaml` file to the desired version, and then update the pre-commit hooks with:

```bash
pre-commit autoupdate
```

This will update your hooks to the latest versions specified in the configuration file.

## Alembic Workflow

Using Alembic involves several common steps for managing database migrations in your FastAPI application. Here's a general workflow you can follow:

1. Initial Setup
   Ensure Docker is running.
2. Starting the Services
   Run `make up` to start all services defined in your docker-compose.yml, including your database service.
3. Creating a New Migration
   Whenever you make changes to your database models, you'll need to create a new migration script.
   Run `make alembic-revision m="description_of_changes"` to create a new migration script. Replace `description_of_changes` with a brief description of the changes your migration introduces.
4. Reviewing the Migration Script
   Alembic will generate a new migration script in your migrations directory (versions folder under the alembic directory).
   Review and, if necessary, manually edit the generated script to ensure it accurately represents the desired database schema changes.
5. Applying Migrations
   Run `make alembic-upgrade` to apply the latest migration to your database. This will bring your database schema up to date with your current model definitions.
6. Checking Migration Status
   You can check the current state of migrations in your database by running `make alembic-current`. This will show you the current revision of the database.
7. Rolling Back Migrations
   If you need to undo the last migration, you can run `make alembic-downgrade`. This command reverts the last applied migration.
8. Stopping the Services
   Once you're done, you can stop all services by running `make down`.
