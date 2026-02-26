# Frontend Code Overview

This document describes the existing frontend code provided for the Project Management MVP.

## Tech Stack

- **Framework**: Next.js (Version 16.1.6) with the App Router (`src/app`).
- **Language**: TypeScript (`tsconfig.json`).
- **Styling**: Tailwind CSS (v4) with PostCSS, leveraging `clsx` for conditional class names.
- **Drag and Drop**: `@dnd-kit/core`, `@dnd-kit/sortable`, `@dnd-kit/utilities` for robust, accessible drag-and-drop Kanban functionality.
- **Testing**:
  - Unit Tests: Vitest and React Testing Library (`@testing-library/react`, `@testing-library/jest-dom`, `@testing-library/user-event`).
  - E2E Tests: Playwright (`@playwright/test`).

## Core Components

Located in `src/components/`, the app is structured around a classic Kanban board:

- `KanbanBoard.tsx`: The main container managing the state of the columns and cards, and handling the drag-and-drop contexts and sensors.
- `KanbanColumn.tsx`: Represents a single column (e.g., Todo, In Progress, Done). Acts as a droppable area for cards.
- `KanbanCard.tsx`: An individual task card, visually draggable, containing the task title, description, and actions.
- `KanbanCardPreview.tsx`: The visual overlay shown while a card is actively being dragged.
- `NewCardForm.tsx`: A UI component for adding new cards to a column.

## Application Structure

- `src/app/page.tsx`: The entry point rendering the `KanbanBoard` component.
- `src/app/layout.tsx`: The root layout defining the standard HTML structure and global styles from `globals.css`.

## Next Steps for the Frontend Pipeline

Currently, this frontend serves as a standalone React application. As part of this overall project, we will need to adapt it for full static export (`output: 'export'`) when integrating with the FastAPI backend, and subsequently remove the mock/hardcoded state in favor of making API calls to our backend endpoints.
