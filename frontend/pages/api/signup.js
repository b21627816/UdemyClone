import { BACKEND_URL } from "../../config/app";

export default async (req, res) => {
  if (req.method === "POST") {
    const { email, password, name } = req.body;

    const resAPI = await fetch(`${BACKEND_URL}/auth/user/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password, name }),
    });

    const data = await resAPI.json();

    if (resAPI.ok) {
      res.status(200).json(data);
      return;
    } else {
      res.status(400).json(data);
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
