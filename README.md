# MLH API Assistant

Assistant-style project for MLH API Week, built with React, Vite, Auth0, and Backboard.

## Current status
- Auth0 login flow is integrated
- Login/logout flow is working
- Authenticated user profile is shown in the app
- Backboard setup has started
- A first simple document was added to the assistant for basic RAG-style querying

## Project direction
This repository is the base for a larger identity-aware assistant that will evolve through the MLH API Week challenges.

Current path:
- Auth0 setup
- Backboard assistant setup
- simple document-grounded assistant
- privacy-aware and context-aware behavior later

## Setup

### 1. Install dependencies
```bash
npm install
````

### 2. Create a `.env` file

Create a `.env` file in the project root and add:

```env
VITE_AUTH0_DOMAIN=your_auth0_domain
VITE_AUTH0_CLIENT_ID=your_auth0_client_id
VITE_AUTH0_CALLBACK_URL=http://localhost:5173
```

If your current app also uses additional API values later, add them there as needed.

### 3. Run the app

```bash
npm run dev
```

## Notes

This project is still in progress and intentionally simple for now. The current goal is to keep one clean project and gradually extend it into a stronger privacy-aware assistant.

````

