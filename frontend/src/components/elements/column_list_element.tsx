import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { DataSourceColumn } from "@/types/data_source_column.type";
import { Label } from "../ui/label";
import { Button } from "../ui/button";
import { PlusIcon } from "lucide-react";
import useCreateSchema from "@/hooks/useMutateSchema";

interface ColumnListElementProps {
  columns: DataSourceColumn[];
}
export function ColumnListElement({ columns }: ColumnListElementProps) {
  const [selectedColumn, setSelectedColumn] = useState<DataSourceColumn | null>(
    null
  );

  const selected_style = (col: DataSourceColumn) => {
    if (!(selectedColumn && col.id == selectedColumn.id))
      return "hover:bg-slate-300 dark:hover:bg-slate-500";
    return "";
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-row-reverse">
        <Button>{<PlusIcon />}</Button>
      </div>
      {columns.map((col) => (
        <Card
          key={col.id}
          className={`cursor-pointer transition-all duration-300 ${selected_style(
            col
          )}`}
          onClick={() =>
            col.id != selectedColumn?.id
              ? setSelectedColumn(col)
              : setSelectedColumn(null)
          }
        >
          <CardHeader>
            <CardTitle>{col.name}</CardTitle>
            <Label>{col.type}</Label>
          </CardHeader>
          {selectedColumn?.id == col.id ? (
            <CardContent onClick={(e: React.MouseEvent) => e.stopPropagation()}>
              <Textarea defaultValue={col.description} />
            </CardContent>
          ) : null}
        </Card>
      ))}
    </div>
  );
}
