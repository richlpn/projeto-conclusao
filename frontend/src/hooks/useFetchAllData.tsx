import { useQuery } from "@tanstack/react-query";
import { ZodSchema } from "zod";

interface FectchTypes<T extends ZodSchema> {
  schema: T;
  endpoint: {
    getAll: (skip: number, limit: number) => string;
    getById: (id: string) => string;
    create: string;
    update: (id: string) => string;
    delete: (id: string) => string;
  };
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
