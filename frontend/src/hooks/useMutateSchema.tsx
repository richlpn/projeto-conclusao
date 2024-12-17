import { useMutation, UseMutationResult } from "@tanstack/react-query";
import axios from "axios";
import { z, ZodType } from "zod";

const createSchema = async <T extends ZodType, C extends ZodType>(
  schema: T,
  data: z.infer<C>,
  endpoint: string
): Promise<z.infer<T>> => {
  try {
    const resp = await axios.post<z.infer<T>>(endpoint, data);
    return schema.parse(resp.data);
  } catch (error) {
    console.error("Error in createSchema:", error);
    throw error;
  }
};

export default function useCreateSchema<T extends ZodType, C extends ZodType>(
  endpoint: string,
  schema: T
): UseMutationResult<z.infer<T>, Error, z.infer<C>> {
  return useMutation({
    mutationFn: (data: z.infer<C>) =>
      createSchema<T, C>(schema, data, endpoint),
  });
}
