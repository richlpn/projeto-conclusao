import { DataSourceSchema } from "@/types/data_source.type";
import { useState } from "react";
import { Input } from "../ui/input";
import { DataSourceSchemaList } from "./data_source_schema_list";
import { Button } from "../ui/button";
import { ScrollArea } from "../ui/scroll-area";
import { CreateSchemaModal } from "./create_schema_modal";
import { useDataSources } from "@/context/data_sources_context";
import { endpoints } from "@/utils/endpoints";
import { useDeleteSchema } from "@/hooks/useDeleteSchema";
import { FloatingNotification } from "./floating_notification_element";

interface LeftPanelProps {
  onSelectSchema: (schema: DataSourceSchema) => void;
  selectedSchema: DataSourceSchema | null;
}
interface Message {
  type: "error" | "success";
  message: string;
  title: string;
}
export default function ({ onSelectSchema, selectedSchema }: LeftPanelProps) {
  const { dataSources, isLoading, error } = useDataSources();
  const { mutate: deleteSchema, error: deleteError } = useDeleteSchema({
    endpoint: endpoints.data_source,
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const [search, setSearch] = useState<string>("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  if (isLoading || !dataSources) return <div>Loading...</div>;
  if (error && dataSources == null)
    return <div>Error When loading Data Sources Try again latter: {error}</div>;

  const onDeleteSchema = (schema: string) => {
    deleteSchema(schema);
  };

  const deleteMessage: Message = deleteError
    ? {
        type: "error",
        message: "Failed to remove Data Source",
        title: "Erro",
      }
    : {
        type: "success",
        message: "Data Source removed successfully",
        title: "Success",
      };

  return (
    <div className="h-full flex flex-col p-4 space-y-4 mb-5 mx-2">
      <Input
        placeholder="Search schemas..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <Button onClick={() => setIsModalOpen(true)}>Create Schema</Button>
      <ScrollArea className="flex-grow">
        <DataSourceSchemaList
          searchQuery={search}
          schemas={dataSources}
          onSelectSchema={onSelectSchema}
          selectedSchema={selectedSchema}
          onDeleteSchema={onDeleteSchema}
        />
      </ScrollArea>
      <CreateSchemaModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
      {deleteError ? <FloatingNotification {...deleteMessage} /> : null}
    </div>
  );
}
