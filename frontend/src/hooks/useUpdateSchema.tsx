import axios from "axios";
import { EndpointType } from "@/utils/endpoints";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { z } from "zod";
import invalidateQueries from "@/utils/invalidateQueries";
import { CheckCircleIcon, Loader2 } from "lucide-react";
import { useToast } from "./use-toast";

export function useUpdateSchema<
  TSchema extends z.ZodType,
  TResponse extends z.ZodType
>(endpoint: EndpointType, updateSchema: TSchema, finalSchema: TResponse) {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: async ({
      data,
      id,
    }: {
      data: z.infer<TSchema>;
      id: string;
    }) => {
      const validated = updateSchema.parse(data);
      const response = await axios.patch(endpoint.update(id), validated);
      return finalSchema.parse(response.data);
    },
    onMutate: () => {
      // Show initial loading toast
      return toast({
        title: "Upading...",
        description: "Wating to update confirmation",
        duration: Infinity, // Keep toast alive
        action: <Loader2 className="animate-spin h-4 w-4" />,
      });
    },
    onSuccess: (_, __, context) => {
      // Dismiss loading toast and show success
      context?.dismiss();
      invalidateQueries(queryClient, endpoint);

      toast({
        title: "Success",
        description: "The column is up to date!",
        duration: 3000,
        action: <CheckCircleIcon className="text-green-600" />,
      });
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
