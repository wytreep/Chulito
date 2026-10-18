import pg from 'pg';

const { Pool } = pg;
const connectionString = process.env.DATABASE_URL;

if (!connectionString) {
  console.error('DATABASE_URL is required; no database has been contacted.');
  process.exit(2);
}

const pool = new Pool({
  connectionString,
  connectionTimeoutMillis: 5_000,
  max: 2,
});

try {
  const result = await pool.query(
    'SELECT $1::text AS marker, current_setting($2) AS server_version',
    ['chulito-tbd8-synthetic', 'server_version'],
  );
  if (result.rows[0]?.marker !== 'chulito-tbd8-synthetic') {
    throw new Error('Unexpected PostgreSQL smoke response.');
  }
  console.log(
    JSON.stringify(
      {
        connected: true,
        marker: result.rows[0].marker,
        server_version: result.rows[0].server_version,
      },
      null,
      2,
    ),
  );
} finally {
  await pool.end();
}
