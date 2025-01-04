import { z } from "zod";

export const taskCreateSchema = z.object({
  title: z.string().min(1, "Name is required"),
  signatureFunction: z.string().min(5, "Function name is required"),
  description: z
    .string()
    .min(20, "Description requires more details")
    .max(400, "description is too long"),
  dataSourceId: z.string().uuid(),
});

export const taskSchema = taskCreateSchema.extend({
  id: z.string().uuid(),
});

export type TaskCreate = z.infer<typeof taskCreateSchema>;
export type Task = z.infer<typeof taskSchema>;
