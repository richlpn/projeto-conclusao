import axios from "axios";
import { EndpointWithGenerate } from "@/utils/endpoints";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { dataSourceSchema } from "@/types/data_source.type";
import { useToast } from "./use-toast";
import { CheckCircleIcon, Loader2 } from "lucide-react";

export function useMutateDataSourceFromFile(endpoint: EndpointWithGenerate) {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const key = [dataSourceSchema];

  return useMutation({
    mutationKey: key,
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      const response = await axios.post(endpoint.generate(), formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      return dataSourceSchema.parse(response.data);
    },
    onMutate: () => {
      // Show initial loading toast
      return toast({
        title: "Creating...",
        description: "The object is being created",
        duration: Infinity, // Keep toast alive
        action: <Loader2 className="animate-spin h-4 w-4" />,
      });
    },
    onSuccess: (_, __, context) => {
      // Dismiss loading toast and show success
      context?.dismiss();
      toast({
        title: "Success",
        description: "Operation completed successfully",
        duration: 3000,
        action: <CheckCircleIcon className="text-green-600" />,
      });
      queryClient.invalidateQueries({ queryKey: [endpoint] });
    },
    onError: (__, _, context) => {
      // Dismiss loading toast and show error
      context?.dismiss();
      toast({
        variant: "destructive",
        title: "Error",
        description: "Something went wrong...",
        duration: 3000,
      });
    },
  });
}
