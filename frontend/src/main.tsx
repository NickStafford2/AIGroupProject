import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./main.css";
import Example from "./example";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <h1 className="text-3xl font-bold underline">Hello world!</h1>
    <Example></Example>
  </StrictMode>,
);
