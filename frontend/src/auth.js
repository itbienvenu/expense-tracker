import api from "./api"

// Register
export async function register(username, email, password) {
  try {
    const response = await api.post("/auth/register", { username, email, password });
    if (response.data?.success === false) {
      let msg = response.data.detail || "Registration failed";
      alert(response.data.detail.suggestions[0])
      if (response.data.errors) msg += ": " + response.data.errors.join("; ");
      if (response.data.suggestions) msg += " | Suggestions: " + response.data.suggestions.join("; ");
      throw new Error(msg);
    }

    return response.data;
  } catch (err) {
    if (err.response && err.response.data) {
      const data = err.response.data;
      if (data.detail) throw new Error(data.detail);
    }
    throw new Error(err.response.detail.detail || "Registration failed");
  }
}

export async function login(email, password) {
  try {
    const response = await api.post("/auth/login", {
      email,
      hashed_password: password,
    });
    localStorage.setItem("token", response.data.access_token);
    return response.data;
  } catch (err) {
    // Axios wraps errors in err.response
    if (err.response && err.response.data) {
      const data = err.response.data;

      // Handle validation errors from FastAPI
      if (Array.isArray(data)) {
        // Combine all error messages into one string
        const messages = data.map(e => `${e.loc.join(" -> ")}: ${e.msg}`);
        throw new Error(messages.join("; "));
      }

      // Handle normal error detail (like invalid credentials)
      if (data.detail) {
        throw new Error(data.detail);
      }
    }

    // Fallback generic error
    throw new Error("Login failed. Please try again.");
  }
}


export async function getCurrentUser() {
  const token = localStorage.getItem("token");
  if (!token) return null;

  const response = await api.get("/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
}

