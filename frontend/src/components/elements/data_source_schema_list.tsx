import { Button } from "@/components/ui/button";
import { DataSourceSchema } from "@/types/data_source.type";

interface DataSourceSchemaListProps {
  schemas: DataSourceSchema[];
  searchQuery: string;
  onSelectSchema: (schema: DataSourceSchema) => void;
  selectedSchema: DataSourceSchema | null;
}

export function DataSourceSchemaList({
  schemas,
  searchQuery,
  onSelectSchema,
  selectedSchema,
}: DataSourceSchemaListProps) {
  const filteredSchemas = schemas.filter((schema) =>
    schema.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex flex-col space-y-2 max-w-lg">
      {filteredSchemas.map((schema) => (
        <Button
          key={schema.id}
          onClick={() => onSelectSchema(schema)}
          variant={
            selectedSchema && schema.id == selectedSchema.id
              ? "outline"
              : "default"
          }
          className="justify-start rounded"
        >
          <div className="flex flex-col items-start">
            <span>{schema.name}</span>
            <span className="text-xs text-muted-foreground">
              {schema.type.name}
            </span>
          </div>
        </Button>
      ))}
    </div>
  );
}
