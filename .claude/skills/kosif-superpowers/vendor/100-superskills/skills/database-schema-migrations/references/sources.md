# مصادر «مخطط قاعدة البيانات والترحيلات» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## prisma-database-setup (2930-prisma)

- الترخيص: **MIT**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/prisma
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2930-prisma/12151-prisma-database-setup
- الوصف: Guides for configuring Prisma with different database providers (PostgreSQL, MySQL, SQLite, MongoDB, etc.). Use when setting up a new project, changing databases, or troubleshooting connection issues. Triggers on "configure postgres", "connect to mysql", "setup mongodb", "sqlite setup".

```markdown
# Prisma Database Setup

Comprehensive guides for configuring Prisma ORM with various database providers.

## When to Apply

Reference this skill when:
- Initializing a new Prisma project
- Switching database providers
- Configuring connection strings and environment variables
- Troubleshooting database connection issues
- Setting up database-specific features
- Generating and instantiating Prisma Client

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Provider Guides | CRITICAL | provider names |
| 2 | Prisma Postgres | HIGH | `prisma-postgres` |
| 3 | Client Setup | CRITICAL | `prisma-client-setup` |

## System Prerequisites

- **Node.js 20.19.0+**
- **TypeScript 5.4.0+**

## Bun Runtime

If you're using Bun, run Prisma CLI commands with `bunx --bun prisma ...` so Prisma uses the Bun runtime instead of falling back to Node.js.

## Supported Databases

| Database | Provider String | Notes |
|----------|-----------------|-------|
| PostgreSQL | `postgresql` | Default, full feature support |
| MySQL | `mysql` | Widespread support, some JSON diffs |
| SQLite | `sqlite` | Local file-based, no enum/scalar lists |
| MongoDB | `mongodb` | Mongo-specific workflow; do not apply SQL driver-adapter guidance |
| SQL Server | `sqlserver` | Microsoft ecosystem |
| CockroachDB | `cockroachdb` | Distributed SQL, Postgres-compatible |
| Prisma Postgres | `postgresql` | Managed serverless database |

## Configuration Files

Your configuration shape depends on the provider and Prisma major version:

1. **All providers** use **`prisma/schema.prisma`**.
2. **Prisma 7 SQL setups** typically use **`prisma.config.ts`** for datasource URLs.
3. **MongoDB projects should stay on Prisma 6.x**, keep `url = env("DATABASE_URL")` in the schema, and continue using the classic MongoDB setup.

## Driver Adapters

The standard SQL workflow uses a driver adapter. Choose the adapter and driver for your database and pass the adapter to `PrismaClient`.

| Database | Adapter | JS Driver |
|----------|---------|-----------|
| PostgreSQL | `@prisma/adapter-pg` | `pg` |
| CockroachDB | `@prisma/adapter-pg` | `pg` |
| Prisma Postgres (Node.js) | `@prisma/adapter-pg` | `pg` |
| Prisma Postgres (edge/serverless) | `@prisma/adapter-ppg` | `@prisma/ppg` |
| MySQL / MariaDB | `@prisma/adapter-mariadb` | `mariadb` |
| SQLite | `@prisma/adapter-better-sqlite3` | `better-sqlite3` |
| SQLite (Turso/LibSQL) | `@prisma/adapter-libsql` | `@libsql/client` |
| SQL Server | `@prisma/adapter-mssql` | `node-mssql` |

MongoDB should not follow the Prisma 7 SQL adapter workflow. Use the latest Prisma 6.x release for MongoDB projects and do not install a SQL `@prisma/adapter-*` package for it.

Example (PostgreSQL):

```ts
```

## prisma-database-setup (2930-prisma)

- الترخيص: **MIT**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/prisma
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2930-prisma/12157-prisma-database-setup
- الوصف: Guides for configuring Prisma with different database providers (PostgreSQL, MySQL, SQLite, MongoDB, etc.). Use when setting up a new project, changing databases, or troubleshooting connection issues. Triggers on "configure postgres", "connect to mysql", "setup mongodb", "sqlite setup".

```markdown
# Prisma Database Setup

Comprehensive guides for configuring Prisma ORM with various database providers.

## When to Apply

Reference this skill when:
- Initializing a new Prisma project
- Switching database providers
- Configuring connection strings and environment variables
- Troubleshooting database connection issues
- Setting up database-specific features
- Generating and instantiating Prisma Client

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Provider Guides | CRITICAL | provider names |
| 2 | Prisma Postgres | HIGH | `prisma-postgres` |
| 3 | Client Setup | CRITICAL | `prisma-client-setup` |

## System Prerequisites

- **Node.js 20.19.0+**
- **TypeScript 5.4.0+**

## Bun Runtime

If you're using Bun, run Prisma CLI commands with `bunx --bun prisma ...` so Prisma uses the Bun runtime instead of falling back to Node.js.

## Supported Databases

| Database | Provider String | Notes |
|----------|-----------------|-------|
| PostgreSQL | `postgresql` | Default, full feature support |
| MySQL | `mysql` | Widespread support, some JSON diffs |
| SQLite | `sqlite` | Local file-based, no enum/scalar lists |
| MongoDB | `mongodb` | Mongo-specific workflow; do not apply SQL driver-adapter guidance |
| SQL Server | `sqlserver` | Microsoft ecosystem |
| CockroachDB | `cockroachdb` | Distributed SQL, Postgres-compatible |
| Prisma Postgres | `postgresql` | Managed serverless database |

## Configuration Files

Your configuration shape depends on the provider and Prisma major version:

1. **All providers** use **`prisma/schema.prisma`**.
2. **Prisma 7 SQL setups** typically use **`prisma.config.ts`** for datasource URLs.
3. **MongoDB projects should stay on Prisma 6.x**, keep `url = env("DATABASE_URL")` in the schema, and continue using the classic MongoDB setup.

## Driver Adapters

The standard SQL workflow uses a driver adapter. Choose the adapter and driver for your database and pass the adapter to `PrismaClient`.

| Database | Adapter | JS Driver |
|----------|---------|-----------|
| PostgreSQL | `@prisma/adapter-pg` | `pg` |
| CockroachDB | `@prisma/adapter-pg` | `pg` |
| Prisma Postgres (Node.js) | `@prisma/adapter-pg` | `pg` |
| Prisma Postgres (edge/serverless) | `@prisma/adapter-ppg` | `@prisma/ppg` |
| MySQL / MariaDB | `@prisma/adapter-mariadb` | `mariadb` |
| SQLite | `@prisma/adapter-better-sqlite3` | `better-sqlite3` |
| SQLite (Turso/LibSQL) | `@prisma/adapter-libsql` | `@libsql/client` |
| SQL Server | `@prisma/adapter-mssql` | `node-mssql` |

MongoDB should not follow the Prisma 7 SQL adapter workflow. Use the latest Prisma 6.x release for MongoDB projects and do not install a SQL `@prisma/adapter-*` package for it.

Example (PostgreSQL):

```ts
```

## azuresql-db-schema-migration (2512-azure-sql-database-container)

- الترخيص: **MIT**  ·  الأصل: https://github.com/microsoft/azure-sql-database-container/tree/c1e8167e4c1d5979d7fc4a6ea11a6ce885a9398b
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2512-azure-sql-database-container/9780-azuresql-db-schema-migration
- الوصف: Runs database schema migrations against the local Azure SQL Database container so the same migrations apply identically on the local engine and in the Azure cloud. Use when asked to "run my migrations against the local SQL", "apply schema to the container", "apply EF Core / dotnet ef database update", "Prisma migrate dev / deploy", "Alembic upgrade head", or deploy a DACPAC / SqlPackage to the con

```markdown
# Schema migrations on the Azure SQL Database container

Apply schema migrations to the local **Azure SQL Database** container the same way
you would against the cloud, so dev and prod stay identical. This is the Azure SQL
Database engine (`SELECT SERVERPROPERTY('EngineEdition')` returns **5**,
`Edition` returns **'SQL Azure'**), **not** the SQL Server image
`mcr.microsoft.com/mssql/server`. If a tool or template points at the SQL Server image,
stop and use the image below instead.

Verified on 2026-09-05 against the container image
`sqldbpreview-dpgaeqhmgphzd4bk.azurecr.io/azure-sql/db-dev:latest`, reporting `EngineEdition`
5, Edition `SQL Azure`, build `12.0.2000.8`. All six executable checks behind this skill
passed: the engine identity, `Msg 40508` for `USE`, a `VECTOR(n)` column in migration DDL, the
three SqlPackage `Publish` parameters and `/TargetTrustServerCertificate` present in
SqlPackage 170.4.83.3's own help, and `dotnet ef database update` on Entity Framework Core
.NET command-line tools 9.0.19.

## The one rule that breaks every migration tool

The engine does **NOT** auto-create databases on connect. Every migration tool
assumes the target database already exists. So:

1. Provision `appdb` on a **master** connection FIRST.
2. Then point the migration tool at the **user** database (`Database=appdb`).

Avoid `USE` to switch databases. In a user-database session (the
Azure-faithful context where you develop), `USE` returns `Msg 40508`, exactly as in
Azure SQL Database in the cloud. A `master` connection is a provisioning
session where the Azure statement filter is not enforced, so `USE` appears to
work there, but `master` is for provisioning only, not
application work. Always select the target database in the connection string
(`Database=appdb`, or `-d appdb` for sqlcmd). A `master` connection is for
provisioning only; run migrations against `appdb`.

## Start the container and provision appdb (canonical recipe)

The engine is not ready the instant `docker run` returns. Wait with a retry loop
and create `appdb` inside that same loop. Image is x64 only; on a non-x64 host the
recipe adds `--platform linux/amd64` automatically. The registry is private during
Private Preview, so sign in first.

```bash
docker login sqldbpreview-dpgaeqhmgphzd4bk.azurecr.io   # pull-only creds by signing up at https://aka.ms/sqldbcontainerpreview-signup

# Pick a free host port and add the platform flag only on a non-x64 host (works in bash and zsh).
HOST_PORT=1433; while lsof -nP -iTCP:"$HOST_PORT" -sTCP:LISTEN >/dev/null 2>&1; do HOST_PORT=$((HOST_PORT+1)); done
PLATFORM=(); case "$(docker info -f '{{.Architecture}}' 2>/dev/null)" in x86_64|amd64) ;; *) PLATFORM=(--platform linux/amd64);; esac
docker rm -f sqldb 2>/dev/null
```

## prisma-schema (x4918-ts-backend-dev)

- الترخيص: **WTFPL**  ·  الأصل: https://github.com/widnyana/eyay-toolkits/tree/50e222e396d3ea0b9a9cc65c4a5cf58d3c1cfa39/plugins/ts-backend-dev
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/x4918-ts-backend-dev/x20314-prisma-schema
- الوصف: Create or modify Prisma schema for new entities using multi-schema by default. Use this skill when the user wants to define database models, add tables, create migrations, or design a schema with proper field types, relations, indexes, and conventions. Triggers on "prisma schema", "add model", "create table", "database schema", "define entity", or when the user mentions Prisma and needs a model de

```markdown
# Prisma Schema

Create/modify schema for: $ARGUMENTS

## Multi-Schema Setup

Always define `schemas` in the datasource block. This enables organizing models into logical namespaces and is supported by PostgreSQL, CockroachDB, and SQL Server.

```prisma
generator client {
  provider = "prisma-client"
  output   = "./generated"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  schemas  = ["base", "billing", "inventory"]
}
```

Every model and enum must declare its schema with `@@schema("name")`. Pick the schema that matches the model's domain. If only one schema is needed, use a single entry like `schemas = ["public"]`.

## Schema Pattern

```prisma
model EntityName {
  id        String    @id @default(uuid())
  createdAt DateTime  @default(now()) @map("created_at")
  updatedAt DateTime  @updatedAt @map("updated_at")
  deletedAt DateTime? @map("deleted_at")

  // Business fields
  status EntityStatus @default(ACTIVE)
  name   String
  amount Decimal      @db.Decimal(36, 18)

  // Relations
  accountId String  @map("account_id")
  account   Account @relation(fields: [accountId], references: [id])

  // Indexes
  @@index([accountId])
  @@index([status])
  @@index([createdAt])

  // Table and schema mapping
  @@map("entity_names")
  @@schema("base")
}

enum EntityStatus {
  ACTIVE
  INACTIVE
  DELETED

  @@schema("base")
}
```

### Cross-Schema Relations

Models in different schemas can reference each other. Both schemas must be listed in `schemas`.

```prisma
// schema: "base"
model User {
  id     Int     @id
  orders Order[]

  @@schema("base")
}

// schema: "billing"
model Order {
  id     Int  @id
  user   User @relation(fields: [userId], references: [id])
  userId Int

  @@schema("billing")
}
```

### Same Table Name, Different Schema

When two schemas have tables with the same name, use unique model names and `@@map` to disambiguate:

```prisma
model BaseConfig {
  id Int @id

  @@map("Config")
  @@schema("base")
}

model UserConfig {
  id Int @id

  @@map("Config")
  @@schema("users")
}
```

## Conventions

### Naming

- Model: PascalCase (`InvoicePayment`)
- Fields: camelCase (`accountId`)
- DB columns: snake_case via `@map("account_id")`
- Table: snake_case plural via `@@map("invoice_payments")`
- Schema: lowercase, domain-based (`"billing"`, `"inventory"`, `"auth"`)

### Common Fields

```prisma
id        String   @id @default(uuid())
createdAt DateTime @default(now()) @map("created_at")
updatedAt DateTime @updatedAt @map("updated_at")
deletedAt DateTime? @map("deleted_at")  // Soft delete
```

### Decimal for Money / Crypto

```prisma
amount Decimal @db.Decimal(36, 18)  // High precision
```

Use `Decimal` for any financial value. `Float` is not acceptable for money.

### Relations

```prisma
// One-to-Many
```

## database-migration (3095-framework-migration)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/framework-migration
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3095-framework-migration/13261-database-migration
- الوصف: Execute database migrations across ORMs and platforms with zero-downtime strategies, data transformation, and rollback procedures. Use when migrating databases, changing schemas, performing data transformations, or implementing zero-downtime deployment strategies.

```markdown
# Database Migration

Master database schema and data migrations across ORMs (Sequelize, TypeORM, Prisma), including rollback strategies and zero-downtime deployments.

## When to Use This Skill

- Migrating between different ORMs
- Performing schema transformations
- Moving data between databases
- Implementing rollback procedures
- Zero-downtime deployments
- Database version upgrades
- Data model refactoring

## ORM Migrations

### Sequelize Migrations

```javascript
// migrations/20231201-create-users.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable("users", {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true,
      },
      email: {
        type: Sequelize.STRING,
        unique: true,
        allowNull: false,
      },
      createdAt: Sequelize.DATE,
      updatedAt: Sequelize.DATE,
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable("users");
  },
};

// Run: npx sequelize-cli db:migrate
// Rollback: npx sequelize-cli db:migrate:undo
```

### TypeORM Migrations

```typescript
// migrations/1701234567-CreateUsers.ts
import { MigrationInterface, QueryRunner, Table } from "typeorm";

export class CreateUsers1701234567 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: "users",
        columns: [
          {
            name: "id",
            type: "int",
            isPrimary: true,
            isGenerated: true,
            generationStrategy: "increment",
          },
          {
            name: "email",
            type: "varchar",
            isUnique: true,
          },
          {
            name: "created_at",
            type: "timestamp",
            default: "CURRENT_TIMESTAMP",
          },
        ],
      }),
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable("users");
  }
}

// Run: npm run typeorm migration:run
// Rollback: npm run typeorm migration:revert
```

### Prisma Migrations

```prisma
// schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  createdAt DateTime @default(now())
}

// Generate migration: npx prisma migrate dev --name create_users
// Apply: npx prisma migrate deploy
```

## Schema Transformations

### Adding Columns with Defaults

```javascript
// Safe migration: add column with default
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn("users", "status", {
      type: Sequelize.STRING,
      defaultValue: "active",
      allowNull: false,
    });
  },

  down: async (queryInterface) => {
```

## database-migration (3485-framework-migration)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/framework-migration
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3485-framework-migration/14205-database-migration
- الوصف: Execute database migrations across ORMs and platforms with zero-downtime strategies, data transformation, and rollback procedures. Use when migrating databases, changing schemas, performing data transformations, or implementing zero-downtime deployment strategies.

```markdown
# Database Migration

Master database schema and data migrations across ORMs (Sequelize, TypeORM, Prisma), including rollback strategies and zero-downtime deployments.

## When to Use This Skill

- Migrating between different ORMs
- Performing schema transformations
- Moving data between databases
- Implementing rollback procedures
- Zero-downtime deployments
- Database version upgrades
- Data model refactoring

## ORM Migrations

### Sequelize Migrations

```javascript
// migrations/20231201-create-users.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable("users", {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true,
      },
      email: {
        type: Sequelize.STRING,
        unique: true,
        allowNull: false,
      },
      createdAt: Sequelize.DATE,
      updatedAt: Sequelize.DATE,
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable("users");
  },
};

// Run: npx sequelize-cli db:migrate
// Rollback: npx sequelize-cli db:migrate:undo
```

### TypeORM Migrations

```typescript
// migrations/1701234567-CreateUsers.ts
import { MigrationInterface, QueryRunner, Table } from "typeorm";

export class CreateUsers1701234567 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: "users",
        columns: [
          {
            name: "id",
            type: "int",
            isPrimary: true,
            isGenerated: true,
            generationStrategy: "increment",
          },
          {
            name: "email",
            type: "varchar",
            isUnique: true,
          },
          {
            name: "created_at",
            type: "timestamp",
            default: "CURRENT_TIMESTAMP",
          },
        ],
      }),
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable("users");
  }
}

// Run: npm run typeorm migration:run
// Rollback: npm run typeorm migration:revert
```

### Prisma Migrations

```prisma
// schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  createdAt DateTime @default(now())
}

// Generate migration: npx prisma migrate dev --name create_users
// Apply: npx prisma migrate deploy
```

## Schema Transformations

### Adding Columns with Defaults

```javascript
// Safe migration: add column with default
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn("users", "status", {
      type: Sequelize.STRING,
      defaultValue: "active",
      allowNull: false,
    });
  },

  down: async (queryInterface) => {
```
