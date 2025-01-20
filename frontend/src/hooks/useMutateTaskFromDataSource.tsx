import axios from "axios";
import { EndpointWithGenerate } from "@/utils/endpoints";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "./use-toast";
import { Loader2 } from "lucide-react";
import { taskSchema } from "@/types/task.type";

export function useMutateGenerateTasks(endpoint: EndpointWithGenerate) {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const key = [taskSchema];

  return useMutation({
    mutationKey: key,
    mutationFn: async (dataSourceId: string) => {
      const response = await axios.post(endpoint.generate(dataSourceId));
      return taskSchema.array().parse(response.data);
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
