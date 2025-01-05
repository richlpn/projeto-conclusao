import { ScrollArea } from "@/components/ui/scroll-area";
import { useDeleteSchema } from "@/hooks/useDeleteSchema";
import { useListColumnsFromDataSource } from "@/hooks/useListDataSourceColumns";
import { endpoints } from "@/utils/endpoints";
import { ColumnListElement } from "./column_list_element";
import { CreateColumnModal } from "./create_column_element";
import { FormSubmitResponse } from "./form_element";
import {
  CreateDataSourceColumn,
  CreateDataSourceColumnSchema,
  DataSourceColumnSchema,
} from "@/types/data_source_column.type";
import { useCreateSchema } from "@/hooks/useCreateSchema";

interface ColumnPanelProps {
  onCloseColumnForm: () => void;
  selectedSchemaID: string;
  isFormOpen: boolean;
}
export function ColumnPanel({
  onCloseColumnForm,
  selectedSchemaID,
  isFormOpen,
}: ColumnPanelProps) {
  const { mutateAsync: deleteColumn } = useDeleteSchema(
    endpoints.data_source_columns
  );

  const { data: columns, refetch: refetchColumns } =
    useListColumnsFromDataSource(
      selectedSchemaID,
      endpoints.data_source_columns
    );
  const { mutateAsync: createColumn } = useCreateSchema(
    endpoints.data_source_columns,
    CreateDataSourceColumnSchema,
    DataSourceColumnSchema
  );

  // Takes the fields of the form as an schema and request the creation of a new schema
  async function afterSubmit(): Promise<void> {
    onCloseColumnForm();
    await refetchColumns();
  }
  async function onDeleteColumn(id: string) {
    await deleteColumn(id);
    await refetchColumns();
  }
  async function submitForm(
    response: FormSubmitResponse<CreateDataSourceColumn>
  ) {
    await createColumn(response.schema);
    response.form.reset();
    onCloseColumnForm();
    await refetchColumns();
  }

  if (!columns)
    return (
      <h1 className="h-full flex items-center justify-center text-muted-foreground">
        Select a schema to view tasks
      </h1>
    );
  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <ScrollArea className="h-[700px] pr-4">
        <ColumnListElement
          onDeleteColumn={onDeleteColumn}
          dataSourceId={selectedSchemaID}
          afterSubmit={afterSubmit}
          columns={columns}
        />
      </ScrollArea>
      <CreateColumnModal
        isColumnFormOpen={isFormOpen}
        onCloseColumnForm={onCloseColumnForm}
        formProps={{
          onSubmit: submitForm,
          dataSourceSchemaId: selectedSchemaID,
          isPending: false,
        }}
      />
    </div>
  );
}
