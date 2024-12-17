import "@/index.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App.tsx";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { DataSourceProvider } from "./context/data_sources_context.tsx";

const queryClient = new QueryClient();
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <DataSourceProvider>
        <App />
      </DataSourceProvider>
    </QueryClientProvider>
  </StrictMode>
);
