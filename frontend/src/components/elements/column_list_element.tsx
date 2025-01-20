import { ColumnForm } from "@/components/forms/column_form";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog";
import {
  CreateDataSourceColumn,
  CreateDataSourceColumnSchema,
  DataSourceColumn,
  DataSourceColumnSchema,
} from "@/types/data_source_column.type";
import { Loader2, Trash2 } from "lucide-react";
import React, { useEffect, useState } from "react";
import { Button } from "../ui/button";
import { Description } from "@radix-ui/react-dialog";
import { endpoints } from "@/utils/endpoints";
import { FormSubmitResponse } from "./form_element";
import { useUpdateSchema } from "@/hooks/useUpdateSchema";
import { useToast } from "@/hooks/use-toast";

export interface ColumnListElementProps {
  columns: DataSourceColumn[];
  dataSourceId: string;
  onDeleteColumn: (id: string) => void;
}
export function ColumnListElement({
  columns,
  onDeleteColumn,
  dataSourceId,
}: ColumnListElementProps) {
  // Track the Selected Column for update or expand
  const [selectedColumn, setSelectedColumn] = useState<DataSourceColumn | null>(
    null
  );
  // Used to render an shade/depth on the hoverd column
  const [hoverColumn, setHoverColumn] = useState<
    DataSourceColumn | undefined
  >();
  // Create a mutation to update the selected column schema
  const {
    mutateAsync: updateSchema,
    isPending,
    isSuccess,
  } = useUpdateSchema(
    endpoints.data_source_columns,
    CreateDataSourceColumnSchema,
    DataSourceColumnSchema
  );
  const { toast } = useToast();

  const onDelete = (e: React.MouseEvent, col_id: string) => {
    e.stopPropagation();
    onDeleteColumn(col_id);
  };

  async function onSubmit(
    response: FormSubmitResponse<CreateDataSourceColumn>
  ) {
    const { schema, form } = response;
    if (!selectedColumn) throw Error(`No column selected`);

    await updateSchema({ data: schema, id: selectedColumn.id });
    form.reset();
    // Close the modal and resed the editing/selected state
    setSelectedColumn(null);
  }
  return (
    <div className="space-y-4">
      {columns.map((col) => (
        <Card
          key={col.id}
          className={`cursor-pointer transition-all duration-300 hover:bg-gray-100 `}
          onClick={() =>
            setSelectedColumn(col.id != selectedColumn?.id ? col : null)
          }
          onMouseOver={() => setHoverColumn(col)}
          onMouseOut={() => setHoverColumn(undefined)}
        >
          <CardHeader>
            <CardTitle className="flex items-center justify-between gap-2">
              {col.name} ({col.type})
              <Button
                variant={"outline"}
                onClick={(e: React.MouseEvent) => onDelete(e, col.id)}
                className={hoverColumn?.id == col.id ? "" : "opacity-0"}
              >
                <Trash2 className="text-red-500" />
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription>{col.description}</CardDescription>
          </CardContent>
        </Card>
      ))}
      {selectedColumn ? (
        <Dialog
          open={selectedColumn !== null}
          onOpenChange={() => setSelectedColumn(null)}
        >
          <Description>Edit column</Description>
          <DialogContent className="max-w-4xl">
            <DialogTitle>{selectedColumn?.name}</DialogTitle>
            <ColumnForm
              dataSourceSchemaId={dataSourceId}
              onSubmit={onSubmit}
              isPending={isPending}
              column={{
                dataSourceId: dataSourceId,
                description: selectedColumn.description,
                name: selectedColumn.name,
                type: selectedColumn.type,
              }}
            />
          </DialogContent>
        </Dialog>
      ) : null}
    </div>
  );
}
