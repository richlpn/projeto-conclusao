import { EndpointType } from "@/utils/endpoints";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "./use-toast";
import axios from "axios";
import { Label } from "@/components/ui/label";
import { CheckCircleIcon } from "lucide-react";
import invalidateQueries from "@/utils/invalidateQueries";

export function useDeleteSchema(endpoint: EndpointType) {
  const queryClient = useQueryClient();

  const deleteSchema = async (id: string) => {
    await axios.delete(endpoint.delete(id));
    return id;
  };
  const { toast } = useToast();

  return useMutation({
    mutationFn: deleteSchema,
    onSuccess: () => {
      invalidateQueries(queryClient, endpoint);
      toast({
        description: <Label> Removed successfully</Label>,
        title: "Success",
        action: <CheckCircleIcon className="text-green-600" />,
      });
    },

    onError: (error) => {
      toast({
        description: (
          <div>
            Falied to remove object
            <div>
              Status Code:{" "}
              {error instanceof Error
                ? error.message
                : "Failed to delete schema"}
            </div>
          </div>
        ),
        title: "Error",
        variant: "destructive",
      });
    },
  });
}
