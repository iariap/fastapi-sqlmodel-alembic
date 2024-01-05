# funspark

# Alembic

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
