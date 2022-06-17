import React, { createContext, useState } from "react";
import { NEXT_BACKEND_URL } from "../config/app";

const AuthContext = createContext();

const AuthContextProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [authError, setAuthError] = useState(null);
  const [authReady, setIsAuthReady] = useState(false);

  const signup = async (email, password, name) => {
    const res = await fetch(`${NEXT_BACKEND_URL}/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password, name }),
    });

    const data = await res.json();

    if (res.ok) {
      await login({ email, password });
    } else {
      if (data.name) {
        setAuthError(data.name[0]);
      } else if (data.email) {
        setAuthError(data.email[0]);
      } else {
        setAuthError(data.password.join("\n"));
      }
    }
  };

  const login = async ({ email, password }) => {
    const res = await fetch(`${NEXT_BACKEND_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      await checkUserLoggedIn();
    } else {
      setAuthError(data.detail);
    }
  };

  const logout = async () => {
    const res = await fetch(`${NEXT_BACKEND_URL}/logout`, {
      method: "POST",
    });

    if (res.ok) {
      setUser(null);
    }
  };

  const checkUserLoggedIn = async () => {
    const res = await fetch(`${NEXT_BACKEND_URL}/user`);

    if (res.ok) {
      const data = await res.json();
      setUser(data);
      // update user in redux
    } else {
      // set user null in redux

      setUser(null);
    }
  };

  const clearUser = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, authError, signup, login, logout, clearUser }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;
