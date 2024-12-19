import { z } from "zod";

export const taskCreateSchema = z.object({
  name: z.string().min(1, "Name is required"),
  type: z.string().uuid(),
  separator: z.string().optional().nullable(),
});