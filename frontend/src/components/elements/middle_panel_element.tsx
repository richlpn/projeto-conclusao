import { ScrollArea } from "@/components/ui/scroll-area";
import { DataSourceSchema } from "@/types/data_source.type";
import { ColumnListElement } from "./column_list_element";

interface MiddlePanelProps {
  selectedSchema: DataSourceSchema | null;
}

export function MiddlePanel({ selectedSchema }: MiddlePanelProps) {
  return (
    <div className="h-full p-4">
      {selectedSchema ? (
        <ScrollArea className="h-full">
          <ColumnListElement columns={selectedSchema.columns} />
        </ScrollArea>
      ) : (
        <h1 className="h-full flex items-center justify-center text-muted-foreground">
          Select a schema to view tasks
        </h1>
      )}
    </div>
  );
}
