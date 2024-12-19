import { Button } from "@/components/ui/button";
import { DataSourceSchema } from "@/types/data_source.type";
import { Trash2 } from "lucide-react";
import { useState } from "react";

interface DataSourceSchemaListProps {
  schemas: DataSourceSchema[];
  searchQuery: string;
  onSelectSchema: (schema: DataSourceSchema) => void;
  selectedSchema: DataSourceSchema | null;
  onDeleteSchema: (schemaID: string) => void;
}

export function DataSourceSchemaList({
  schemas,
  searchQuery,
  onSelectSchema,
  selectedSchema,
  onDeleteSchema,
}: DataSourceSchemaListProps) {
  const [hoveredSchemaId, setHoveredSchemaId] = useState<string | null>(null);

  const filteredSchemas = schemas.filter((schema) =>
    schema.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex flex-col space-y-2 max-w-lg">
      {filteredSchemas.map((schema) => (
        <div
          key={schema.id}
          className="relative"
          onMouseEnter={() => setHoveredSchemaId(schema.id)}
          onMouseLeave={() => setHoveredSchemaId(null)}
        >
          <Button
            onClick={() => onSelectSchema(schema)}
            variant={
              selectedSchema && schema.id == selectedSchema.id
                ? "outline"
                : "default"
            }
            className="justify-start rounded w-full"
          >
            <div className="flex flex-col items-start">
              <span>{schema.name}</span>
              <span className="text-xs text-muted-foreground">
                {schema.type.name}
              </span>
            </div>
          </Button>
          <div
            className={`absolute right-2 top-1/2 transform -translate-y-1/2 transition-opacity duration-300 ${
              hoveredSchemaId === schema.id ? "opacity-100" : "opacity-0"
            }`}
          >
            <Trash2
              className="h-5 w-5 text-red-500 cursor-pointer"
              onClick={() => onDeleteSchema(schema.id)}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
