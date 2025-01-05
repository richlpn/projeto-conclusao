import { QueryClient } from "@tanstack/react-query";
import { EndpointType } from "./endpoints";

export default async (queryClient: QueryClient, endpoint: EndpointType) => {
  const queryCache = queryClient.getQueryCache();
  const queries = queryCache.findAll({
    predicate: (query) => {
      return query.queryKey.includes(endpoint);
    },
  });
  await Promise.all(
    queries.map((query) =>
      queryClient.invalidateQueries({ queryKey: query.queryKey })
    )
  );
};
