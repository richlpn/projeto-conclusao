import { EndpointType } from "@/utils/endpoints";
import { useQuery } from "@tanstack/react-query";
import { ZodSchema } from "zod";

interface FectchTypes<T extends ZodSchema> {
  schema: T;
  endpoint: EndpointType;
  skip: number;
  limit: number;
}
export const useFetchAllData = <T extends ZodSchema>(query: FectchTypes<T>) => {
  return useQuery({
    queryKey: [query.endpoint],
    queryFn: async () => {
      const response = await fetch(
        query.endpoint.getAll(query.skip, query.limit)
      );
      const data = await response.json();
      return query.schema.array().parse(data);
    },
  });
};
