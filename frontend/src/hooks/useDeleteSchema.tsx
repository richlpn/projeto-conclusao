import { EndpointType } from "@/utils/endpoints";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

export function useDeleteSchema(endpoint: EndpointType) {
  const queryClient = useQueryClient();

  const deleteSchema = async (id: string) => {
    const response = await axios.delete(endpoint.delete(id));
    return response.status;
  };

  return useMutation({
    mutationFn: deleteSchema,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [endpoint] });
    },
  });
}
