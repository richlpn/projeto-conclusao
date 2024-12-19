import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { FormField, FormSubmitResponse, GenericForm } from "./form_element";
import {
  CreateDataSourceColumn,
  CreateDataSourceColumnSchema,
} from "@/types/data_source_column.type";
import { endpoints } from "@/utils/endpoints";
import { Path } from "react-hook-form";
import useCreateSchema from "@/hooks/useMutateSchema";
import { useToast } from "@/hooks/use-toast";

interface CreateColumnModalProps {
  dataSourceId: string;
  onSuccess?: () => void;
  isOpen: boolean;
  onClose: () => void;
}
const fields: FormField<CreateDataSourceColumn>[] = [
  {
    name: "name" as Path<CreateDataSourceColumn>,
    label: "Column Name",
    placeholder: "Enter column name",
  },
  {
    name: "type" as Path<CreateDataSourceColumn>,
    label: "Column Type",
    placeholder: "Enter column type",
  },
  {
    name: "description" as Path<CreateDataSourceColumn>,
    label: "Description",
    placeholder: "Enter column description",
  },
];

export function CreateColumnModal({
  dataSourceId,
  isOpen,
  onClose,
}: CreateColumnModalProps) {
  const { mutateAsync, error, isPending, isSuccess } = useCreateSchema(
    endpoints.data_source_columns,
    CreateDataSourceColumnSchema
  );
  const { toast } = useToast();

  async function onSubmit(
    response: FormSubmitResponse<CreateDataSourceColumn>
  ): Promise<void> {
    const { schema, form } = response;
    form.reset();
    mutateAsync;
    await mutateAsync(schema);

    onClose();
  }
  if (isSuccess) {
    toast({
      title: "Success",
      description: "Form submitted successfully",
    });
  }
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogTrigger asChild></DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Column</DialogTitle>
        </DialogHeader>
        <GenericForm
          schema={CreateDataSourceColumnSchema}
          fields={fields}
          onSubmit={onSubmit}
          isLoading={isPending}
          defaultValues={{ dataSourceId: dataSourceId }}
        />
      </DialogContent>
    </Dialog>
  );
}
