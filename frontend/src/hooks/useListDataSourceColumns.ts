import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { EndpointType } from "@/utils/endpoints";
import { DataSourceColumnSchema } from "@/types/data_source_column.type";

export function useListColumnsFromDataSource(
  data_source_id: string,
  endpoints: EndpointType
) {
  const endpoint = `${endpoints.create}/data-source/${data_source_id}`;
  const queryKey = ["list", "columns", endpoints.create];

  return useQuery({
    queryKey,
    queryFn: async () => {
      const response = await axios.get(endpoint);
      const parsed = DataSourceColumnSchema.array().parse(response.data);
      return parsed;
    },
  });
}
