import axios from "axios";
import { EndpointType } from "@/utils/endpoints";
import { useMutation } from "@tanstack/react-query";
import { z } from "zod";

export function useUpdateSchema<
  TSchema extends z.ZodType,
  TResponse extends z.ZodType
>(endpoint: EndpointType, updateSchema: TSchema, finalSchema: TResponse) {
  const key = [endpoint];

  return useMutation({
    mutationKey: key,
    mutationFn: async ({
      data,
      id,
  }: {
      data: z.infer<TSchema>;
      id: string;
    }) => {
      const validated = updateSchema.parse(data);
      const response = await axios.patch(endpoint.update(id), validated);
      return finalSchema.parse(response.data);
    },
  });
}
