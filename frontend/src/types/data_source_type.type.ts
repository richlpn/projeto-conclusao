import { z } from 'zod';

export const DataSourceTypeSchema = z.object({
  name: z.string().min(1, 'Name is required'),
});

export type DataSourceType = z.infer<typeof DataSourceTypeSchema>
