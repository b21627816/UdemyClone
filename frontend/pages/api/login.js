import { BACKEND_URL } from "../../config/app";
import cookie from "cookie";

export default async (req, res) => {
  if (req.method === "POST") {
    const { email, password } = req.body;

    const resAPI = await fetch(`${BACKEND_URL}/auth/jwt/create/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await resAPI.json();

    if (resAPI.ok) {
      res.setHeader("Set-Cookie", [
        cookie.serialize("refresh_token", data.refresh, {
          httpOnly: true,
          secure: process.env.NODE_ENV !== "development",
          maxAge: 60 * 60 * 24,
          sameSite: "strict",
          path: "/",
        }),
        cookie.serialize("access_token", data.access, {
          httpOnly: true,
          secure: process.env.NODE_ENV !== "development",
          maxAge: 60,
          sameSite: "strict",
          path: "/",
        }),
      ]);
      res.status(200).json({});
      return;
    } else {
      res.status(401).json(data);
      return;
    }
  } else {
    res.setHeader("Allow", ["POST"]);
    res.status(400).json({
      message: `${req.method} is not allowed`,
    });
    return;
  }
};
