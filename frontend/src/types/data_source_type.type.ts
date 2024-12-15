import { z } from "zod";

export const DataSourceTypeCreateSchema = z.object({
  name: z.string().min(1),
});

export const DataSourceTypeSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1, "Name is required"),
});

export type DataSourceType = z.infer<typeof DataSourceTypeSchema>;
export type DataSourceTypeCreate = z.infer<typeof DataSourceTypeCreateSchema>;
