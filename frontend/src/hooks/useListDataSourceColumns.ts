import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { endpoints } from "@/utils/endpoints";
import { DataSourceColumnSchema } from "@/types/data_source_column.type";

export function useListColumnsFromDataSource(data_source_id: string) {
  const endpoint = `${endpoints.data_source_columns.create}/data-source/${data_source_id}`;
  const queryKey = ["list", "columns", endpoint];

  return useQuery({
    queryKey,
    queryFn: async () => {
      const response = await axios.get(endpoint);
      const parsed = DataSourceColumnSchema.array().parse(response.data);
      return parsed;
    },
  });
}
