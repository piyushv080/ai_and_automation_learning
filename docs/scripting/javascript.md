# JavaScript for Automation

JavaScript runs in web browsers and, through Node.js, can also power command-line tools and API integrations. JSON is a natural fit for JavaScript because it maps to common JavaScript objects and arrays.

## Variables and collections

Use `const` when a binding will not be reassigned and `let` when it will. Prefer `===` for strict equality.

```javascript
const servers = [
  { name: "web-01", environment: "prod", healthy: true },
  { name: "web-02", environment: "dev", healthy: false },
];

const productionServers = servers.filter(
  (server) => server.environment === "prod"
);

console.log(productionServers.map((server) => server.name));
```

## Functions and asynchronous work

```javascript
async function getHealth(url) {
  const response = await fetch(url, { signal: AbortSignal.timeout(10000) });

  if (!response.ok) {
    throw new Error(`Health request failed: HTTP ${response.status}`);
  }

  return response.json();
}
```

`async` functions return promises. Use `await` to wait for asynchronous work and `try`/`catch` to handle expected failures. Keep timeouts, status checks, and error reporting in API clients.

## Browser and Node.js use

- In a browser, JavaScript can update page content and call APIs using `fetch`.
- In Node.js, JavaScript can create scripts and services, read files, and use packages from npm.
- Browser and Node.js APIs differ; use the documentation for the runtime you target.

Never put a private API token in browser code: browser-delivered code is visible to users. Keep secrets on a protected server or use an approved authentication flow.

## Practice project

Create a small Node.js command that calls an authorized test health endpoint, checks the HTTP status, prints a concise result, and exits with a non-zero code on failure.

## Further reading

- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [Node.js documentation](https://nodejs.org/docs/latest/api/)
