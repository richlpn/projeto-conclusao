import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { EndpointType } from "@/utils/endpoints";
import { z } from "zod";

export function useListSchemaFromFields<TResponse extends z.ZodType>(
  endpoints: EndpointType,
  from: string,
  values: object,
  finalSchema: TResponse
) {
  const queryString = Object.entries(values).reduce((acc, [key, value]) => {
    acc += `?${key}=${value}`;
    return acc;
  }, "");
  const endpoint = `${endpoints.create}/${from}/${queryString}`;
  const queryKey = [endpoints, from];

  return useQuery({
    queryKey,
    queryFn: async () => {
      const response = await axios.get(endpoint);
      const parsed = finalSchema.array().parse(response.data);
      console.log("Data", parsed, queryString);
      return parsed;
    },
  });
}
