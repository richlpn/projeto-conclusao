import {
  DataSource,
  DataSourceCreate,
  dataSourceCreateSchema,
  dataSourceSchema,
} from "@/types/data_source.type";
import { useState } from "react";
import { Input } from "../ui/input";
import { DataSourceSchemaList } from "./data_source_schema_list";
import { Button } from "../ui/button";
import { ScrollArea } from "../ui/scroll-area";

import { endpoints } from "@/utils/endpoints";
import { useDeleteSchema } from "@/hooks/useDeleteSchema";
import { useListSchema } from "@/hooks/useFetchAllData";
import { CreateDataSourceModal } from "./create_data_source_element";
import { FormSubmitResponse } from "./form_element";
import { useCreateSchema } from "@/hooks/useMutateSchema";
import { useToast } from "@/hooks/use-toast";
import { Toaster } from "../ui/toaster";

interface LeftPanelProps {
  onSelectSchema: (schema: DataSource) => void;
  selectedSchema: DataSource | null;
}

// Helper function to get the correct message if an error was raised during deleting a sche,a
const deleteMessage = (error: boolean) =>
  error
    ? {
        description: "Failed to remove Data Source",
        title: "Erro",
      }
    : {
        description: "Data Source removed successfully",
        title: "Success",
      };

export default function ({ onSelectSchema, selectedSchema }: LeftPanelProps) {
  // Hook to get the mutation of deleting an data source
  const {
    mutate: deleteSchema,
    error: deleteError,
    isSuccess: isDeleteSuccess,
  } = useDeleteSchema(endpoints.data_source);

  // Hook to get the query used to create a new data sources
  // Used on handleSubit and called at CreateDataSourceModal
  const {
    mutateAsync: mutateDataSourceCreate,
    isPending,
    isSuccess: isCreationSucces,
  } = useCreateSchema(
    endpoints.data_source,
    dataSourceCreateSchema,
    dataSourceSchema
  );

  // Query to fecth data sources, refetchDataSources is called on Deletion and Creation
  // Fixed amount of data sources being filtered
  const {
    data: sourcesData,
    isLoading,
    error,
    refetch: refetchDataSources,
  } = useListSchema(endpoints.data_source, dataSourceSchema, {
    limit: 100,
    skip: 0,
  });

  // Current value searched at the search bar
  const [search, setSearch] = useState<string>("");

  // Create data source modal form current state (Open/Closed)
  const [isModalOpen, setIsModalOpen] = useState(false);

  const { toast } = useToast();

  // Get the list of data sources returned from the query
  const dataSources = sourcesData?.items;

  // When the component is re-rendered and the list of data sources is changed, fetch the new list
  if (isDeleteSuccess || isCreationSucces) {
    refetchDataSources();
  }

  // Deletes an data source when called from the DataSourceSchemaList component
  const onDeleteSchema = (schema: string) => {
    deleteSchema(schema);
    toast(deleteMessage(!!deleteError));
    if (selectedSchema) onSelectSchema(selectedSchema);
  };

  // Making closeing the create data source modal more verbose
  const closeModal = () => setIsModalOpen(false);
  const openModal = () => setIsModalOpen(true);

  async function handleSubmit({
    schema,
    form,
  }: FormSubmitResponse<DataSourceCreate>) {
    form.reset();
    await mutateDataSourceCreate(schema);
    toast({ title: "Created", description: "Schema created successfully" });
    closeModal();
  }

  if (isLoading || !dataSources) return <div>Loading...</div>;
  if (error && !dataSources)
    return (
      <div>
        Error When loading Data Sources Try again latter: {error.message}
      </div>
    );

  return (
    <div className="h-full flex flex-col p-4 space-y-4 mb-5 mx-2">
      <Input
        placeholder="Search schemas..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <Button onClick={openModal}>Create Schema</Button>
      <ScrollArea className="flex-grow">
        <DataSourceSchemaList
          searchQuery={search}
          schemas={dataSources}
          onSelectSchema={onSelectSchema}
          selectedSchema={selectedSchema}
          onDeleteSchema={onDeleteSchema}
        />
      </ScrollArea>
      <CreateDataSourceModal
        onClose={closeModal}
        isLoading={isPending}
        isOpen={isModalOpen}
        handleSubmit={handleSubmit}
      />
      <Toaster />
    </div>
  );
}
