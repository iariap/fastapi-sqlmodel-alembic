# Project Template

This is a simple project template using the following components:
- FastAPI
- SQLModel -> SQLAlchemy
- Alembic for schema Migrations
- pytest

Also has a GenericCRUD (for interacting with the db model), GenericCrudRouter (for automatic expose rest API)


## Getting Started with the Project
Before starting up the backend or running any commands, you need to set up the environment. This can be easily done using the make command. Simply run the following command in your terminal:
```sh
make setup-environment
```
The following steps are executed:

1. **Check Docker Version**:
   - The command checks if Docker version 2 is installed on your system. If it is not installed, it will display an error message indicating that Docker version 2 is not installed.

2. **Check Python Version**:
   - It verifies whether Python version 3.12 is installed. If Python 3.12 is not found, an error message is displayed.

3. **Check and Install Poetry**:
   - The command checks for the presence of Poetry, a Python dependency management and packaging tool. If Poetry is not installed, it is automatically installed using a script from the official Poetry website.

4. **Setting Up the Environment**:
   - After performing the checks, it sets up the Python environment using Poetry. This step involves using Python 3.12 for the environment and installing all dependencies specified in the project's `pyproject.toml` file.

And then to open a terminal for the project run:
```sh
poetry shell
```

# Running locally
## vscode
## Running the Project Locally with Visual Studio Code (VSCode)

To run the project locally using VSCode, follow these steps:

1. **Open the Project in VSCode**:
   - Start by opening the main folder in VSCode.

2. **Setup the Environment**:
   - Before running the project, ensure that you have set up the environment. Run the `make setup-environment` command in the terminal to prepare your environment.

3. **Activate the Python Environment**:
   - In the VSCode terminal, activate the Python environment created by Poetry by running:
     ```sh
     poetry shell
     ```
   - This step is crucial to ensure that VSCode uses the correct Python interpreter and dependencies.

4. **Install VSCode Extensions**:
   - Install recommended VSCode extensions for Python and Docker to enhance your development experience. These extensions provide features like IntelliSense, code navigation, and Docker integration (Optional).

5. **Run the Project**:
   - Press Ctrl+`F5` to run the project.
   - Select `FastAPI` from the dropdown list of configurations.
   - Entrer `app.main:app` as the app entrypoint.
   - Optionally you could also specify to watch for code changes using the `--reload` parameter.
   Coverage should not run along with pytest  because they collide, so edit the `.vscode/launch.json` file like this:
```json
   {
      "version": "0.2.0",
      "configurations": [
         {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
               "app.main:app",
               "--reload"
            ],
            "justMyCode": false
         },
         {
            "name": "Debug Tests",
            "type": "python",
            "justMyCode": false,
            "request": "test",
            "console": "integratedTerminal",
            "env": {
               "PYTEST_ADDOPTS": "--no-cov"
            },
         }
      ]
   }
```

6. **Access the Application**:
   - Once the project is running, you can access the application through the specified URL in a web browser. The URL will depend on how the project is configured (e.g., `http://localhost:8000` for a web application).

7. **Debugging**:
   - To debug your application, you can use the debugging features provided by VSCode. Set breakpoints in your code and start a debug session using the debug panel in VSCode.


## pycharm
## Running the Project Locally in PyCharm

To run the project locally using PyCharm, follow these steps:

1. **Open the Project in PyCharm**:
   - Start by opening the main folder in PyCharm.

2. **Setup the Environment**:
   - Before running the project, ensure that you have set up the environment. In the PyCharm terminal, run the `make setup-environment` command to prepare your environment. PyCharm will suggest to use pyproject.toml, this is also valid.

3. **Activate the Python Environment**:
   - In the PyCharm terminal, activate the Python environment created by Poetry by running:
     ```sh
     poetry shell
     ```
   - This step is essential to ensure that PyCharm uses the correct Python interpreter and dependencies.

4. **Configure PyCharm for the Project**:
   - Configure your PyCharm to recognize the Python interpreter set up by Poetry. Go to `File > Settings > Project: > Python Interpreter`, and select the Python interpreter from the virtual environment created by Poetry.
   - Optionally, install PyCharm extensions or plugins that facilitate Python and FastAPI development.

5. **Run the Project**:
   - Right-click on the file containing the main entry point of your FastAPI application (typically `main.py` or similar) in PyCharm and select `Run 'filename'`.
   - To enable automatic reloading on code changes, ensure the `--reload` parameter is included in the run configuration.

6. **Access the Application**:
   - Once the project is running, access the application through the specified URL in a web browser, such as `http://localhost:8000`.


## Starting up the backend

To start the backend run the following command:

```sh
make up
```

To stop the aplication run the folowwing command:

```sh
make down
```
## Testing
To run the tests the database is used and each test case is wrapped in a transaction. This ensures that all databases operations are rollbacked after the tests are completed. To run all the tests execute this command:
```sh
make tests
```

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

class Song(SongBase, TimestampModel, UUIDModel, SoftDeleteModel, table=True):
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

## Understanding the Models: `TimestampModel`, `UUIDModel`, and `SoftDeleteModel`

In the given code, three models are defined: `TimestampModel`, `UUIDModel`, and `SoftDeleteModel`. Each model serves a specific purpose.

### `UUIDModel`

- **Purpose**: The `UUIDModel` is designed to provide a unique identifier for each record in a database table.
- **Attributes**:
  - `id`: A field that stores a unique identifier for each record. It uses the UUID (Universally Unique Identifier) format.
- **Characteristics**:
  - The UUID is generated using Python's `uuid.uuid4()` function, which creates a random, unique UUID.
  - The `id` field is marked as a primary key and is indexed for faster queries.
  - The field is non-nullable, meaning it must always have a value.
  - It is set to be unique across the model.

### `TimestampModel`

- **Purpose**: The `TimestampModel` provides timestamp fields for tracking the creation and last update times of a record.
- **Attributes**:
  - `created_at`: The datetime when the record was created.
  - `updated_at`: The datetime when the record was last updated.
- **Characteristics**:
  - Both fields use `datetime.utcnow` as the default value, which sets the time to the current UTC time when the record is created.
  - The fields are non-nullable.
  - The `updated_at` field is designed to be updated whenever the record is modified, though the mechanism for this update (e.g., database triggers) might need to be enabled separately.

### `SoftDeleteModel`

- **Purpose**: The `SoftDeleteModel` is used for soft deletion of records, a technique where records are not physically deleted from the database but are marked as deleted.
- **Attributes**:
  - `deleted_at`: The datetime when the record was marked as deleted.
- **Characteristics**:
  - This field is nullable, meaning it can hold a null value to indicate the record has not been deleted.
  - When a record is "soft deleted," this field is set to the current datetime.
  - Queries can then be written to exclude records where `deleted_at` is not null, effectively hiding soft-deleted records from normal use.

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

## Testing
When writing tests:
- **`test_api_some_entity.py`**: This file should contain tests that focus on the API layer of the songs functionality. Here, you should write tests that make requests to your API endpoints and assert the responses.
- **`test_some_entity.py`**: This file is intended for unit tests that directly interact with the model or services functionalities, independent of the API layer. These tests are crucial for ensuring the internal logic of your application works as expected.

### Testing
## Writting tests
Suppose we want to write tests for the Song model you could have a folder structure like this:
```
tests
└── songs
    ├── factories.py
    ├── test_api_songs.py
    └── test_songs.py
```
Where:
- **factories.py**: Contains the factories for creating instances of your Pydantic models with test data.
   ```python
   from app.songs.models import SongCreate


   class SongCreationFactory(ModelFactory[SongCreate]):
      __model__ = SongCreate

   ```
- **test_api_songs.py**: Contains tests that make requests to your API endpoints and assert the responses.
   ```python
   async def test_create(api_client: TestClient):
      result = api_client.get("/songs")
      assert result
      assert result.status_code == 200

      result = result.json()
      assert len(result["items"]) == 0
      assert result["total"] == 0
      assert result["limit"] == 50
      assert result["offset"] == 0
   ```
   `api_client` is injected by pytest dependency injection.
-
- **test_songs.py**: Contains tests that directly interact with the model or services functionalities, independent of the API layer. These tests are crucial for ensuring the internal logic of your application works as expected.
   ```python
   @pytest.mark.asyncio
   async def test_crud_create(db: AsyncSession):
      song_data = SongCreationFactory.build()
      result = await song_crud.create(
         db,
         obj_in=song_data.model_dump(),
      )
      assert result
      assert result.id
   ```

## Running tests
The Makefile of the project includes commands to facilitate running tests easily.

1. **Running All Tests**:
   - To run all tests, use the following command in the terminal:
     ```sh
     make test
     ```
   - This will execute all test cases, including both unit tests and API tests.

2. **Running API Tests**:
   - If you want to run only the API tests, use:
     ```sh
     make test-api
     ```
   - This command runs tests with a naming pattern that matches 'test_api', ensuring only API tests are executed.

3. **Running Models Tests**:
   - If you want to run only the API tests, use:
     ```sh
     make test-model
     ```
   - This command runs tests with a naming pattern that does not matches 'test_api', ensuring only model tests are executed.


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
