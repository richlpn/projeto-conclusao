import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

interface QueryType {
  endpoint: {
    getAll?: (skip: number, limit: number) => string;
    getById?: (id: string) => string;
    create?: string;
    update?: (id: string) => string;
    delete: (id: string) => string;
  };
}

export function useDeleteSchema(query: QueryType) {
  const queryClient = useQueryClient();

  const deleteSchema = async (id: string) => {
    const response = await axios.delete(query.endpoint.delete(id));
    return response.status;
  };

  return useMutation({
    mutationFn: deleteSchema,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [query.endpoint] });
    },
  });
}
