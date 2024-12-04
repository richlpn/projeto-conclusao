import { DataSourceSchema } from "@/types/data_source.type";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import React, { useCallback, useContext, useMemo, useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { DataContext } from "@/providers/data_sources_provider";

export default function () {
  const { data, isLoading, error } = useContext(DataContext);
  const [selectedSchema, setSelectedSchema] = useState<DataSourceSchema | null>(
    null
  );
  const [search, setSearch] = useState<string>("");

  const filteredSchemas = useMemo(
    () => data?.filter((source) => source.name.includes(search)),
    [data, search]
  );
  const handleSearchChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => setSearch(e.target.value),
    []
  );
  console.log("filteredSchemas", filteredSchemas, search);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="w-1/4 border-r p-4">
      <div className="flex flex-row gap-4">
        <Input
          type="text"
          placeholder="Search DataSourceSchemas..."
          onChange={handleSearchChange}
          className="mb-4 text-white "
        />
      </div>
      <ScrollArea className="h-[calc(100vh-120px)]">
        {filteredSchemas?.map((schema) => (
          <Button
            key={schema.id}
            variant={selectedSchema?.id === schema.id ? "secondary" : "default"}
            className="w-full justify-start mb-2"
            onClick={() => setSelectedSchema(schema)}
          >
            {schema.name} ({schema.type})
          </Button>
        ))}
      </ScrollArea>
    </div>
  );
}
