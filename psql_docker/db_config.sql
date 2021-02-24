CREATE DATABASE current_setting('custom.name');

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = current_setting('custom.user')) THEN

      CREATE ROLE current_setting('custorm.user') LOGIN PASSWORD current_setting('custom.password');
   END IF;
   GRANT ALL PRIVILEGES ON current_setting('custom.name') TO current_setting('custom.user');
END
$do$;
