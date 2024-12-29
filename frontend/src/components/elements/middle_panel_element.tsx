import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { DataSource } from "@/types/data_source.type";
import { ColumnListElement } from "./column_list_element";
import { useState } from "react";
import { Button } from "../ui/button";
import { PlusIcon, PlayIcon } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { FormSubmitResponse, GenericForm } from "./form_element";
import { Path } from "react-hook-form";
import {
  CreateDataSourceColumn,
  CreateDataSourceColumnSchema,
  DataSourceColumnSchema,
} from "@/types/data_source_column.type";
import { FormFieldInterface } from "./generic_form_item_element";
import { endpoints } from "@/utils/endpoints";
import { useCreateSchema } from "@/hooks/useMutateSchema";
import { useListColumnsFromDataSource } from "@/hooks/useListDataSourceColumns";
import { useDeleteSchema } from "@/hooks/useDeleteSchema";
import { useToast } from "@/hooks/use-toast";
import { Toaster } from "../ui/toaster";

interface MiddlePanelProps {
  selectedSchema: DataSource;
}
const fields: FormFieldInterface<CreateDataSourceColumn>[] = [
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

export function MiddlePanel({ selectedSchema }: MiddlePanelProps) {
  // State of the create column form modal (Open/Closed)
  const [openColumnForm, setOpenColumnForm] = useState(false);

  const { toast } = useToast();

  const {
    data: deletedColumn,
    mutateAsync: deleteColumn,
    error,
    isSuccess: isDeleteSuccess,
  } = useDeleteSchema(endpoints.data_source_columns);

  const {
    data: columns,
    error: colErro,
    refetch: refetchColumns,
  } = useListColumnsFromDataSource(
    selectedSchema.id,
    endpoints.data_source_columns
  );

  // Prepare mutation to create new columns
  const {
    mutateAsync,
    isPending,
    data: newColumn,
  } = useCreateSchema(
    endpoints.data_source_columns,
    CreateDataSourceColumnSchema,
    DataSourceColumnSchema
  );

  // Takes the fields of the form as an schema and request the creation of a new schema
  async function onSubmit(
    response: FormSubmitResponse<CreateDataSourceColumn>
  ): Promise<void> {
    const { schema, form } = response;

    // Request the creation of the new schema
    await mutateAsync(schema);

    // Clean the form fields
    form.reset();
    // Close the form modal
    setOpenColumnForm(false);
    refetchColumns();
  }

  async function onDeleteColumn(id: string) {
    deleteColumn(id);
    refetchColumns();
  }

  return (
    <div className="h-full p-4 flex flex-col gap-2">
      <div className="flex flex-row-reverse gap-2">
        <Button variant="outline">
          {<PlayIcon className="text-green-600" />}
        </Button>
        <Button onClick={() => setOpenColumnForm(true)}>{<PlusIcon />}</Button>
      </div>
      {columns ? (
        <ScrollArea className="h-full">
          <ColumnListElement
            columns={columns}
            onCreateColumn={onSubmit}
            data_source_id={selectedSchema.id}
            createColumnFields={fields}
            isColumnCreationPending={isPending}
            onDeleteColumn={onDeleteColumn}
          />
          <Dialog
            open={openColumnForm}
            onOpenChange={() => setOpenColumnForm(false)}
          >
            <DialogTrigger asChild></DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Add New Column</DialogTitle>
                <DialogDescription>Describe the new column</DialogDescription>
              </DialogHeader>
              <GenericForm
                schema={CreateDataSourceColumnSchema}
                fields={fields}
                onSubmit={onSubmit}
                isLoading={isPending}
                defaultValues={{ dataSourceId: selectedSchema.id, name: "" }}
              />
            </DialogContent>
          </Dialog>
        </ScrollArea>
      ) : (
        <h1 className="h-full flex items-center justify-center text-muted-foreground">
          Select a schema to view tasks
        </h1>
      )}
      <Toaster />
    </div>
  );
}
