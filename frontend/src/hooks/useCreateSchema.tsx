import axios from "axios";
import { EndpointType } from "@/utils/endpoints";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { z } from "zod";
import invalidateQueries from "@/utils/invalidateQueries";

export function useCreateSchema<
  TSchema extends z.ZodType,
  TResponse extends z.ZodType
>(
  endpoint: EndpointType,
  operationalSchema: TSchema,
  definiteSchema: TResponse
) {
  const key = [endpoint];
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: key,
    mutationFn: async (data: z.infer<TSchema>) => {
      const validated = operationalSchema.parse(data);
      const response = await axios.post(endpoint.create, validated);
      return definiteSchema.parse(response.data);
    },
    onSuccess: async () => {
      invalidateQueries(queryClient, endpoint);
    },
  });
}
