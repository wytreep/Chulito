import { Pool, type PoolConfig } from 'pg';

/**
 * NO INTEGRADO — Compatibility-only factory, not wired into the application.
 * Nothing imports this module: the API does not create the pool at boot because
 * ADR-0001 deliberately does not select an ORM or a database architecture. It
 * exists only so the `pg` client and its types are compiled and type-checked.
 */
export function createPostgresPool(connectionString: string): Pool {
  const config: PoolConfig = {
    connectionString,
    connectionTimeoutMillis: 3_000,
    max: 2,
  };
  return new Pool(config);
}
