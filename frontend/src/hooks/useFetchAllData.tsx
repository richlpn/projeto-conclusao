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
  const queryKey = ["list", endpoint.getAll(params.skip, params.limit)];

  return useQuery({
    queryKey,
    queryFn: async () => {
      const response = await axios.get(queryKey[1]);
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
