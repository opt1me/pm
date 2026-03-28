import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Login } from "@/components/Login";
import { AuthProvider } from "@/lib/auth";

const renderLogin = () =>
  render(
    <AuthProvider>
      <Login />
    </AuthProvider>
  );

describe("Login", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("shows an error on invalid credentials", async () => {
    renderLogin();
    await userEvent.type(screen.getByLabelText("Username"), "wrong");
    await userEvent.type(screen.getByLabelText("Password"), "wrong");
    await userEvent.click(screen.getByRole("button", { name: /sign in/i }));
    expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
  });

  it("accepts valid credentials", async () => {
    renderLogin();
    await userEvent.type(screen.getByLabelText("Username"), "user");
    await userEvent.type(screen.getByLabelText("Password"), "password");
    await userEvent.click(screen.getByRole("button", { name: /sign in/i }));
    expect(screen.queryByText(/invalid credentials/i)).not.toBeInTheDocument();
    expect(localStorage.getItem("pm_auth")).toBe("true");
  });
});
