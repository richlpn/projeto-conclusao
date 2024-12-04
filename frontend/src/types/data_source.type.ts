import { z } from "zod";
import { DataSourceColumnSchema } from "./data_source_column.type";

export const dataSourceCreateSchema = z.object({
  name: z.string().min(1, "Name is required"),
  type: z.string().min(1),
  separator: z.string().optional().nullable(),
});

export const dataSourceSchema = dataSourceCreateSchema.extend({
  id: z.string().uuid(),
  columns: z.array(DataSourceColumnSchema).default([]),
});

export type DataSourceCreateSchema = z.infer<typeof dataSourceCreateSchema>;
export type DataSourceSchema = z.infer<typeof dataSourceSchema>;
