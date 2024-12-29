import { EndpointType } from "@/utils/endpoints";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "./use-toast";
import axios, { AxiosError } from "axios";
import { Label } from "@/components/ui/label";
import { CheckCircleIcon } from "lucide-react";

export function useDeleteSchema(endpoint: EndpointType) {
  const queryClient = useQueryClient();

  const deleteSchema = async (id: string) => {
    const response = await axios.delete(endpoint.delete(id));
    return response.status;
  };
  const { toast } = useToast();

  return useMutation({
    mutationFn: deleteSchema,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [endpoint] });
      toast({
        description: <Label> Removed successfully</Label>,
        title: "Success",
        action: <CheckCircleIcon className="text-green-600" />,
      });
    },

    onError: (error: AxiosError) => {
      toast({
        description: (
          <div>
            Falied to remove object
            <div>Status Code: {error.response?.status}</div>
          </div>
        ),
        title: "Error",
        variant: "destructive",
      });
    },
  });
}
