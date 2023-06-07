## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.

## Debugging

Add `debugger;` in JavaScript or `{@debug variable}` in HTML portion of `.svelte` files.
Browser will stop at that line and bring you to console where you can interactively inspect variables in the scope.

### console.log Arrow (Proxy Objects)

```js
// console log the entire table
JSON.parse(JSON.stringify(table.toArray()));

// get a row by index
JSON.parse(JSON.stringify(table.get(1)));

// get first 10 rows as a Table
JSON.parse(JSON.stringify(table.slice(0, 10).toArray()));

// Pretty print JSON as a table
console.table(JSON.parse(JSON.stringify(table.toArray())));
```
