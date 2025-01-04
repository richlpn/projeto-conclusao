import {
  DataSource,
  DataSourceCreate,
  dataSourceCreateSchema,
  dataSourceSchema,
} from "@/types/data_source.type";
import { useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { ScrollArea } from "../ui/scroll-area";
import { DataSourceSchemaList } from "./data_source_schema_list";

import { useDeleteSchema } from "@/hooks/useDeleteSchema";
import { useListSchema } from "@/hooks/useFetchAllData";
import { useCreateSchema } from "@/hooks/useMutateSchema";
import { endpoints } from "@/utils/endpoints";
import { CreateDataSourceModal } from "./create_data_source_element";
import { FormSubmitResponse } from "./form_element";
import { useMutateDataSourceFromFile } from "@/hooks/useMutateDataSourceFromFile";
import { Loader2 } from "lucide-react";

interface LeftPanelProps {
  onSelectSchema: (schema: DataSource) => void;
  selectedSchema: DataSource | null;
}

export default function ({ onSelectSchema, selectedSchema }: LeftPanelProps) {
  // Hook to get the mutation of deleting an data source
  const { mutate: deleteSchema } = useDeleteSchema(endpoints.data_source);

  // Hook to get the query used to create a new data sources
  // Used on handleSubit and called at CreateDataSourceModal
  const {
    mutateAsync: mutateDataSourceCreate,
    isPending: isCreateDataSourcePending,
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

  const { mutateAsync: createDataSourceFromFile } = useMutateDataSourceFromFile(
    endpoints.data_source
  );

  // Current value searched at the search bar
  const [search, setSearch] = useState<string>("");

  // Create data source modal form current state (Open/Closed)
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Get the list of data sources returned from the query
  const dataSources = sourcesData?.items;

  // Deletes an data source when called from the DataSourceSchemaList component
  const onDeleteSchema = (schema: string) => {
    deleteSchema(schema);
    if (selectedSchema) onSelectSchema(selectedSchema);
  };

  // Making closing the 'create data source' modal verbose
  const closeModal = () => setIsModalOpen(false);
  const openModal = () => setIsModalOpen(true);

  async function handleSubmit(
    response: FormSubmitResponse<DataSourceCreate> | null,
    file: FileList | null
  ) {
    closeModal();

    if (file) {
      await createDataSourceFromFile(file[0]);
    } else if (response) {
      const form = response.form;
      const schema = response.schema;

      form.reset();
      await mutateDataSourceCreate(schema);
    } else {
      throw new Error("At least one argument is required");
    }
    refetchDataSources();
  }
  if (isLoading) {
    return (
      <div className="h-full flex justify-center items-center">
        <Loader2 className="animate-spin" />
      </div>
    );
  }
  if (error || !dataSources)
    return (
      <div>
        Error When loading Data Sources Try again later
        {error?.message}
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
      <ScrollArea className="h-[600px]">
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
        isLoading={isCreateDataSourcePending}
        isOpen={isModalOpen}
        handleSubmit={handleSubmit}
      />
    </div>
  );
}
