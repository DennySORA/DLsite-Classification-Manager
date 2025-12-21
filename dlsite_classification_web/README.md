# DLsite Classification Web

Frontend for DLsite Classification Manager (Nuxt 3 + Tailwind CSS). It consumes
the FastAPI server in the repo root.

## Requirements

- Node.js 18+
- Yarn 1.x (recommended)

## Setup

```
cd dlsite_classification_web
yarn install
```

## Development

```
yarn dev
```

Open `http://localhost:3000` (or `http://localhost:3001` if 3000 is taken).

Backend API (in repo root):

```
uv run python server.py
```

The UI expects the API at `http://localhost:8001`.

## Production

```
yarn build
yarn preview
```

## API Base URL

The base URL is currently hard-coded to `http://localhost:8001`. Search for
`API_BASE` or `localhost:8001` in the frontend source if you need to change it.
