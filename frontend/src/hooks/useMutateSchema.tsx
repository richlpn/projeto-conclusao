import { EndpointType } from "@/utils/endpoints";
import {
  useMutation,
  UseMutationResult,
  useQueryClient,
} from "@tanstack/react-query";
import axios from "axios";
import { z, ZodType } from "zod";

const createSchema = async <T extends ZodType, C extends ZodType>(
  schema: T,
  data: z.infer<C>,
  endpoint: EndpointType
): Promise<z.infer<T>> => {
  try {
    const resp = await axios.post<z.infer<T>>(endpoint.create, data);
    return schema.parse(resp.data);
  } catch (error) {
    console.error("Error in createSchema:", error);
    throw error;
  }
};

export default function useCreateSchema<T extends ZodType, C extends ZodType>(
  endpoint: EndpointType,
  schema: T
): UseMutationResult<z.infer<T>, Error, z.infer<C>> {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationKey: [endpoint],
    mutationFn: (data: z.infer<C>) =>
      createSchema<T, C>(schema, data, endpoint),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [endpoint] });
    },
  });
}
