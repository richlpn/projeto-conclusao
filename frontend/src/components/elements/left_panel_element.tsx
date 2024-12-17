import { DataSourceSchema } from "@/types/data_source.type";
import { useState } from "react";
import { Input } from "../ui/input";
import { DataSourceSchemaList } from "./data_source_schema_list";
import { Button } from "../ui/button";
import { ScrollArea } from "../ui/scroll-area";
import { CreateSchemaModal } from "./create_schema_modal";
import { useDataSources } from "@/context/data_sources_context";

interface LeftPanelProps {
  onSelectSchema: (schema: DataSourceSchema) => void;
  selectedSchema: DataSourceSchema | null;
}

export default function ({ onSelectSchema, selectedSchema }: LeftPanelProps) {
  const { dataSources, isLoading, error } = useDataSources();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const [search, setSearch] = useState<string>("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  if (isLoading || !dataSources) return <div>Loading...</div>;
  if (error && dataSources == null)
    return <div>Error When loading Data Sources Try again latter: {error}</div>;

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
        />
      </ScrollArea>
      <CreateSchemaModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
}
