# PostgreSQL Database Query Results

## Database Schema Information

### Available Schemas
1. **information_schema** (Owner: postgres, Type: System Information Schema)
2. **pg_catalog** (Owner: postgres, Type: System Schema)  
3. **pg_toast** (Owner: postgres, Type: System Schema)
4. **public** (Owner: pg_database_owner, Type: User Schema)

### Objects in Public Schema
1. **projects** (BASE TABLE)
2. **test_users** (BASE TABLE)

## Test Users Table Structure

| Column Name | Data Type | Nullable | Default Value |
|------------|-----------|----------|---------------|
| **id** | integer | NO | nextval('test_users_id_seq'::regclass) |
| **name** | character varying | YES | - |
| **email** | character varying | YES | - |
| **created_at** | timestamp without time zone | YES | CURRENT_TIMESTAMP |

## Query Results: SELECT * FROM test_users

| ID | Name | Email | Created At |
|----|------|-------|------------|
| 1 | John Doe | john@example.com | 2025-07-27 19:05:18.452064 |
| 2 | Jane Smith | jane@example.com | 2025-07-27 19:05:18.452064 |

### Summary
- **Total Records**: 2
- **Query Executed**: `SELECT * FROM test_users;`
- **Executed At**: 2025-07-27 20:17:04Z
- **Tool Used**: MCP PostgreSQL Client (`execute_sql`)

### Notes
- The table contains user information with auto-incrementing IDs
- Both records were created at the same timestamp
- Email and name fields are nullable varchar columns
- The `created_at` field uses PostgreSQL's `CURRENT_TIMESTAMP` as default
