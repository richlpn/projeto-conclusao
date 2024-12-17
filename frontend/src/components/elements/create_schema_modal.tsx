import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DataSourceTypeSchema } from "@/types/data_source_type.type";
import { endpoints } from "@/utils/endpoints";
import { useFetchAllData } from "@/hooks/useFetchAllData";
import { Controller, useForm } from "react-hook-form";
import {
  dataSourceCreateSchema,
  DataSourceCreateSchema,
  dataSourceSchema,
} from "@/types/data_source.type";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  Form,
} from "../ui/form";
import useCreateSchema from "@/hooks/useMutateSchema";
import { useDataSources } from "@/context/data_sources_context";

interface CreateSchemaModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CreateSchemaModal({ isOpen, onClose }: CreateSchemaModalProps) {
  const { data, isLoading, error } = useFetchAllData(
    DataSourceTypeSchema,
    endpoints.data_source_type.getAll(0, 100)
  );
  const { refetch } = useDataSources();
  const mutateDataSourceCreate = useCreateSchema(
    endpoints.data_source.create,
    dataSourceSchema
  );

  const form = useForm<DataSourceCreateSchema>({
    resolver: zodResolver(dataSourceCreateSchema),
    defaultValues: {
      name: "",
      type: "",
    },
  });

  const typePlaceHolder = isLoading ? "Loading..." : "Select a type";

  async function handleSubmit(schema: DataSourceCreateSchema) {
    form.reset();
    try {
      let resp = await mutateDataSourceCreate.mutateAsync(schema);
    } catch (error) {
      console.error("Error creating schema:", error);
    }
    refetch();
    onClose();
  }
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        className="rounded-3xl"
        aria-describedby="form create schema"
      >
        <DialogHeader>
          <DialogTitle>Create New Schema</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)}>
            <Controller
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter schema name" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="type"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Type</FormLabel>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder={typePlaceHolder} />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {data?.map((val) => (
                        <SelectItem key={val.id} value={val.id}>
                          {val.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter className="mt-4">
              <Button type="submit">Create Schema</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
