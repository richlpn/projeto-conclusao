import { ScrollArea } from "@/components/ui/scroll-area";
import { DataSource } from "@/types/data_source.type";
import { ColumnListElement } from "./column_list_element";
import { useState } from "react";
import { Button } from "../ui/button";
import { PlusIcon } from "lucide-react";
import { CreateColumnModal } from "./create_data_source_column_modal_element";

interface MiddlePanelProps {
  selectedSchema: DataSource | null;
}

export function MiddlePanel({ selectedSchema }: MiddlePanelProps) {
  const [openColumnForm, setOpenColumnForm] = useState(false);

  return (
    <div className="h-full p-4">
      <div className="flex flex-row-reverse">
        <Button onClick={() => setOpenColumnForm(true)}>{<PlusIcon />}</Button>
      </div>
      {selectedSchema ? (
        <ScrollArea className="h-full">
          <ColumnListElement data_source={selectedSchema} />
          <CreateColumnModal
            dataSourceId={selectedSchema.id}
            isOpen={openColumnForm}
            onClose={() => setOpenColumnForm(false)}
          />
        </ScrollArea>
      ) : (
        <h1 className="h-full flex items-center justify-center text-muted-foreground">
          Select a schema to view tasks
        </h1>
      )}
    </div>
  );
}
