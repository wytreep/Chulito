import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { setTimeout as delay } from 'node:timers/promises';
import { fileURLToPath } from 'node:url';

async function reservePort() {
  const server = createServer();
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  const address = server.address();
  if (!address || typeof address === 'string')
    throw new Error('Could not reserve a TCP port.');
  const port = address.port;
  await new Promise((resolve, reject) =>
    server.close((error) => (error ? reject(error) : resolve())),
  );
  return port;
}

const port = await reservePort();
const entry = fileURLToPath(new URL('../dist/main.js', import.meta.url));
const child = spawn(process.execPath, [entry], {
  env: { ...process.env, PORT: String(port) },
  stdio: ['ignore', 'pipe', 'pipe'],
});
let stderr = '';
child.stderr.setEncoding('utf8').on('data', (chunk) => {
  stderr += chunk;
});
let success = false;
try {
  for (let attempt = 0; attempt < 60; attempt += 1) {
    if (child.exitCode !== null)
      throw new Error(`Server exited early (${child.exitCode}): ${stderr}`);
    try {
      const healthResponse = await fetch(
        `http://127.0.0.1:${port}/api/health`,
        { signal: AbortSignal.timeout(1_000) },
      );
      const health = await healthResponse.json();
      if (
        !healthResponse.ok ||
        health.status !== 'ok' ||
        health.synthetic !== true
      ) {
        throw new Error(
          `Unexpected health response: ${JSON.stringify(health)}`,
        );
      }
      const openApiResponse = await fetch(
        `http://127.0.0.1:${port}/api/docs-json`,
        { signal: AbortSignal.timeout(1_000) },
      );
      const openApi = await openApiResponse.json();
      if (
        !openApiResponse.ok ||
        openApi.info?.title !== 'Chulito compatibility spike'
      ) {
        throw new Error('OpenAPI smoke response did not match expected title.');
      }
      console.log(
        JSON.stringify({
          node: process.version,
          health,
          openApiPaths: Object.keys(openApi.paths ?? {}).length,
        }),
      );
      success = true;
      break;
    } catch (error) {
      if (error instanceof SyntaxError) throw error;
      await delay(150);
    }
  }
  if (!success)
    throw new Error(
      `Server did not become ready at 127.0.0.1:${port}. ${stderr}`,
    );
} finally {
  if (child.exitCode === null) {
    child.kill('SIGTERM');
    await Promise.race([
      new Promise((resolve) => child.once('exit', resolve)),
      delay(2_000).then(() => {
        child.kill('SIGKILL');
      }),
    ]);
  }
}
