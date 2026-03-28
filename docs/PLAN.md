# High Level Steps for Project

## Part 1: Plan

- [x] Analyze the frontend source code.
- [x] Create `docs/frontend.md` documenting the existing codebase.
- [x] Enrich `docs/PLAN.md` with detailed substeps, tests, and success criteria.
- [ ] User checks and approves the enriched plan.
- **Tests**: None (Documentation phase).
- **Success Criteria**: User responds affirmatively to the proposed plan.

## Part 2: Scaffolding

- [x] Initialize Python backend with FastAPI and `uv` in `backend/`.
- [x] Create `Dockerfile` and `docker-compose.yml` encapsulating both backend and statically served frontend.
- [x] Set up basic FastAPI route to serve a tiny "Hello World" static HTML file.
- [x] Set up a `/api/health` FastAPI route returning `{"status": "ok"}`.
- [x] Write `scripts/start.sh`, `scripts/start.bat`, `scripts/stop.sh`, `scripts/stop.bat` to manage Docker Compose lifecycle.
- **Tests**: Manually run the start scripts on different OS environments. Hit `/api/health` with `curl` or browser.
- **Success Criteria**: Running `start` opens a local server that successfully serves "Hello World" HTML on `/` and JSON on `/api/health`.

## Part 3: Add in Frontend

- [x] Configure `next.config.ts` for static export (`output: 'export'`).
- [x] Build the NextJS frontend to `out/`.
- [x] Configure FastAPI to mount the NextJS `out/` directory as static files on `/`.
- [x] Ensure the NextJS assets and the Next.js router load properly without SSR.
- **Tests**: Run `npm run test:all` in the `frontend` to ensure existing components pass. Run Docker container and visit `/`.
- **Success Criteria**: The beautiful Tailwind Kanban board from `frontend/` loads completely locally when navigating to `http://localhost:8000/`.

## Part 4: Add in a fake user sign in experience

- [x] Create a Login page/modal in the frontend matching the project's aesthetics.
  - *Implemented a full-screen, glassmorphism login UI matching the deep navy (`#032147`) and purple radial gradients of the main Kanban board.*
- [x] Add simple frontend state to block access to the Kanban board unless `user` and `password` are provided.
- [x] Implement a "Sign Out" button in the frontend header.
  - *Styled the "Sign Out" button prominently with the project's secondary purple (`#753991`) to contrast against the white board background.*
- **Tests**: Unit tests for the login component verifying invalid inputs are rejected and valid ones pass. Playwright E2E test to navigate from login to the board.
- **Success Criteria**: Unauthenticated users visiting `/` only see the login prompt. Logging in reveals the board. Refreshing the page keeps you logged in (using `localStorage` or similar simple persist for MVP).

## Part 5: Database modeling

- [x] Design SQLite DB schema (e.g., `users`, `boards`, `columns`, `cards`).
  - *Simplified to a single `boards` table mapping `username` (PK) to `board_data` (JSON string) for the MVP.*
- [x] Document the schema in `docs/database_schema.md`.
- [x] Implement database initialization in FastAPI (creating `kanban.db` if it doesn't exist) using `sqlite3` or an ORM like SQLModel.
  - *Ensured the default SQLite initialization JSON strictly mirrors the frontend `BoardData` React interface (where columns contain `cardIds` arrays referencing a top-level `cards` dictionary) to prevent hydration crashes.*
- **Tests**: Backend unit test to verify that `kanban.db` is correctly instantiated with empty tables.
- **Success Criteria**: A document clearly explaining how Kanban JSON will be persisted across tables/rows, and user sign-off on the DB layout.

## Part 6: Backend

- [x] Add CRUD API routes for Kanban state specific to the signed-in user (`GET /api/board`, `PUT /api/board`, etc.).
- [x] Ensure SQLite operations successfully read and update the stored data layout.
- **Tests**: Comprehensive `pytest` suite for all CRUD operations, leveraging a mocked or in-memory SQLite database.
- **Success Criteria**: All endpoints work perfectly via HTTP requests. Updating a card correctly mutates only that card in the database without destroying other data.

## Part 7: Frontend + Backend

- [x] Replace hardcoded Kanban state in the React components with `fetch` calls to the FastAPI endpoints.
- [x] Implement optimistic UI updates when dragging/dropping cards.
- [x] Handle error states gracefully in the UI if an API call fails.
- **Tests**: Playwright tests to visibly drag a card, release it, and verify via network interception that the correct `PUT` request was dispatched.
- **Success Criteria**: After moving a card, refreshing the browser manually still shows the card in its new position (indicating successful DB persistence).

## Part 8: AI connectivity

- [x] Add `python-dotenv` and OpenAI/OpenRouter generic client to the backend to use the requested `openai/gpt-oss-120b` model.
- [x] Create an internal testing endpoint `/api/ai_test` that sends a simple "2+2" math question and returns the string result.
- **Tests**: Wait for backend server to run, call `/api/ai_test`, and assert the result block contains "4".
- **Success Criteria**: OpenRouter API key correctly authenticates, and the backend can successfully tunnel questions to the LLM and receive the raw string response.

## Part 9: AI with Kanban Context

- [x] Define Structured Outputs schema (JSON format) or function calling bindings allowing the LLM to optionally return Kanban updates alongside a message.
- [x] Update the AI service so it injects the current complete JSON Kanban board state into the system prompt context.
- [x] Expose an endpoint `/api/chat` that takes a user message, queries the LLM, updates the DB if structured output indicates an update, and finally returns the LLM text response.
- **Tests**: Send a sample human prompt like "Rename the first column to 'To Do Today'" and programmatically verify the DB gets updated appropriately and the text response makes sense.
- **Success Criteria**: The backend successfully parses the LLM's structured output into precise database operations (with graceful error handling if the output format breaks).

## Part 10: AI Chat Sidebar widget

- [x] Build a sleek, modern UI sidebar component matching the app's rich aesthetics (dark navy, yellow accents, beautiful typography).
- [x] Hook the sidebar up to the updated `/api/chat` endpoint.
- [x] Implement automatic re-fetching of the board or return updated state directly from `/api/chat` to auto-refresh the UI if the AI altered the board layout.
- **Tests**: Full E2E Playwright test mapping the flow: type in sidebar -> API call executes -> Board UI re-renders automatically with new cards/titles.
- **Success Criteria**: A visually stunning side chat where commanding the AI to "add a card to buy milk" seamlessly causes a card to slide into existence on the Kanban board without a manual page refresh.
