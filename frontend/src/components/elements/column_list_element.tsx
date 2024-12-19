import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { DataSourceColumn } from "@/types/data_source_column.type";
import { Label } from "../ui/label";
import { Button } from "../ui/button";
import { PlusIcon } from "lucide-react";
import { CreateColumnModal } from "./create_data_source_column_modal_element";
import { DataSource } from "@/types/data_source.type";

interface ColumnListElementProps {
  data_source: DataSource;
}
export function ColumnListElement({ data_source }: ColumnListElementProps) {
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
      {data_source.columns.map((col) => (
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
