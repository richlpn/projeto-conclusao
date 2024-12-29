import { useQuery } from "@tanstack/react-query";
import { z } from "zod";
import axios from "axios";
import { EndpointType } from "@/utils/endpoints";

interface PaginationParams {
  skip: number;
  limit: number;
}

export function useListSchema<TResponse extends z.ZodType>(
  endpoint: EndpointType,
  definiteSchema: TResponse,
  params: PaginationParams
) {
  const endpoint_str = endpoint.getAll(params.skip, params.limit);
  const queryKey = [endpoint];

  return useQuery({
    queryKey,
    queryFn: async () => {
      const response = await axios.get(endpoint_str);
      const parsed = definiteSchema.array().parse(response.data);
      return parsed;
    },
    select: (data) => ({
      items: data,
      pagination: {
        skip: params.skip,
        limit: params.limit,
        total: data.length,
      },
    }),
  });
}
