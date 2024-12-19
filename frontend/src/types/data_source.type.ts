import { z } from "zod";
import { DataSourceColumnSchema } from "./data_source_column.type";
import { DataSourceTypeSchema } from "./data_source_type.type";

export const dataSourceCreateSchema = z.object({
  name: z.string().min(1, "Name is required"),
  type: z.string().uuid(),
  separator: z.string().optional().nullable(),
});

export const dataSourceSchema = dataSourceCreateSchema.extend({
  id: z.string().uuid(),
  columns: z.array(DataSourceColumnSchema).default([]),
  type: DataSourceTypeSchema,
});

export type DataSourceCreate = z.infer<typeof dataSourceCreateSchema>;
export type DataSource = z.infer<typeof dataSourceSchema>;
