import { useQuery } from "@tanstack/react-query";
import { ZodSchema } from "zod";

export const useFetchAllData = <T extends ZodSchema>(
  schema: T,
  endpoint: string
) => {
  return useQuery({
    queryKey: [endpoint],
    queryFn: async () => {
      const response = await fetch(endpoint);
      const data = await response.json();
      return schema.array().parse(data);
    },
  });
};
