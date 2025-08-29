import React, { createContext, useContext, useState, useEffect } from "react";
import { toast } from "sonner";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

const API_BASE_URL = "http://localhost:5000/api";

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [loading, setLoading] = useState(true);

  // Helper for API calls
  const apiCall = async (endpoint, options = {}) => {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "An error occurred");
      }

      return data;
    } catch (error) {
      console.error("API call failed:", error);
      throw error;
    }
  };

  // Verify token on initial load
  useEffect(() => {
    const verifyToken = async () => {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const data = await apiCall("/auth/verify-token", { method: "POST" });
        // Ensure user is an object
        const verifiedUser = Array.isArray(data.user)
          ? data.user[0]
          : data.user;
        setUser(verifiedUser);
      } catch (error) {
        console.error("Token verification failed:", error);
        localStorage.removeItem("token");
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    verifyToken();
  }, [token]);

  // Login function
  const login = async (email, password) => {
    try {
      const data = await apiCall("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      // Ensure user is an object
      const loggedInUser = Array.isArray(data.user) ? data.user[0] : data.user;

      setToken(data.token);
      setUser(loggedInUser);
      localStorage.setItem("token", data.token);
      toast.success("Login successful!");

      return { success: true };
    } catch (error) {
      toast.error(error.message);
      return { success: false, error: error.message };
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      const data = await apiCall("/auth/register", {
        method: "POST",
        body: JSON.stringify(userData),
      });

      // Ensure user is an object
      const newUser = Array.isArray(data.user) ? data.user[0] : data.user;

      setToken(data.token);
      setUser(newUser);
      localStorage.setItem("token", data.token);
      toast.success("Registration successful!");

      return { success: true };
    } catch (error) {
      toast.error(error.message);
      return { success: false, error: error.message };
    }
  };

  // Logout function
  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    toast.success("Logged out successfully");
  };

  // Update user object
  const updateUser = (userData) => {
    setUser((prev) => ({ ...prev, ...userData }));
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    updateUser,
    apiCall,
    isAuthenticated: !!token && !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
