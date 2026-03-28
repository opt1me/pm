import { expect, test } from "@playwright/test";
import { initialData } from "../src/lib/kanban";

test("board state persists across page reload", async ({ page }) => {
  // Stateful mock: tracks PUT requests and returns updated state on GET
  let boardState = JSON.parse(JSON.stringify(initialData));

  await page.route("/api/board", async (route) => {
    if (route.request().method() === "GET") {
      await route.fulfill({ json: boardState });
    } else if (route.request().method() === "PUT") {
      const body = JSON.parse(route.request().postData() ?? "{}");
      boardState = body.board_data;
      await route.fulfill({ json: { status: "success" } });
    } else {
      await route.continue();
    }
  });

  await page.goto("/");
  await page.getByLabel("Username").fill("user");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: "Sign In" }).click();
  await expect(page.getByRole("heading", { name: "Kanban Studio" })).toBeVisible();

  // Add a new card
  const firstColumn = page.locator('[data-testid^="column-"]').first();
  await firstColumn.getByRole("button", { name: /add a card/i }).click();
  await firstColumn.getByPlaceholder("Card title").fill("Persistence test card");
  await firstColumn.getByPlaceholder("Details").fill("Should survive reload.");
  await firstColumn.getByRole("button", { name: /add card/i }).click();
  await expect(firstColumn.getByText("Persistence test card")).toBeVisible();

  // Reload — routes persist, localStorage auth persists, board should re-fetch updated state
  await page.reload();
  await expect(page.getByRole("heading", { name: "Kanban Studio" })).toBeVisible();
  await expect(firstColumn.getByText("Persistence test card")).toBeVisible();
});
