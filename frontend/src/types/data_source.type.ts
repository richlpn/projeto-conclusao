// data_source.schema.ts
import { z } from 'zod';
import { DataSourceColumnSchema } from './data_source_column.type';
import { DataSourceTypeSchema } from './data_source_type.type';

export const dataSourceCreateSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  type: DataSourceTypeSchema,
  separator: z.string().optional().nullable(),
});

export const dataSourceSchema = dataSourceCreateSchema.extend({
  id: z.string().uuid(),
  columns: z.array(DataSourceColumnSchema).default([]),
});

type DataSourceCreateSchema = z.infer<typeof dataSourceCreateSchema>;
type DataSourceSchema = z.infer<typeof dataSourceSchema>;