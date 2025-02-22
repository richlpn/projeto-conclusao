import axios from "axios";
import { EndpointType } from "@/utils/endpoints";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { z } from "zod";
import invalidateQueries from "@/utils/invalidateQueries";
import { useToast } from "./use-toast";
import { CheckCircleIcon, Loader2 } from "lucide-react";

export function useCreateSchema<
  TSchema extends z.ZodType,
  TResponse extends z.ZodType
>(
  endpoint: EndpointType,
  operationalSchema: TSchema,
  definiteSchema: TResponse
) {
  const key = [endpoint];
  const queryClient = useQueryClient();
  const { toast } = useToast();
  return useMutation({
    mutationKey: key,
    mutationFn: async (data: z.infer<TSchema>) => {
      const validated = operationalSchema.parse(data);
      const response = await axios.post(endpoint.create, validated);
      return definiteSchema.parse(response.data);
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
      invalidateQueries(queryClient, endpoint);
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
