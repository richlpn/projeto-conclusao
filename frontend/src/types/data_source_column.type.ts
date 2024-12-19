import { z } from "zod";

export const CreateDataSourceColumnSchema = z.object({
  type: z.string(),
  name: z.string(),
  description: z.string(),
  dataSourceId: z.string().uuid(),
});

export const DataSourceColumnSchema = CreateDataSourceColumnSchema.extend({
  id: z.string().uuid(),
});

export type DataSourceColumn = z.infer<typeof DataSourceColumnSchema>;
export type CreateDataSourceColumn = z.infer<
  typeof CreateDataSourceColumnSchema
>;
