import React, { useState } from "react";
import {
  Card,
  CardHeader,
  CardContent,
  CardDescription,
} from "@/components/ui/card";
import {
  CreateDataSourceColumn,
  CreateDataSourceColumnSchema,
  DataSourceColumn,
} from "@/types/data_source_column.type";
import { Button } from "../ui/button";
import { Trash2 } from "lucide-react";
import { FormSubmitResponse, GenericForm } from "./form_element";
import { FormFieldInterface } from "./generic_form_item_element";

interface ColumnListElementProps {
  columns: DataSourceColumn[];
  isColumnCreationPending: boolean;
  data_source_id: string;
  createColumnFields: FormFieldInterface<CreateDataSourceColumn>[];
  onCreateColumn: (
    submit_form: FormSubmitResponse<CreateDataSourceColumn>
  ) => Promise<void>;
  onDeleteColumn: (id: string) => void;
}
export function ColumnListElement({
  columns,
  onCreateColumn,
  data_source_id,
  isColumnCreationPending,
  createColumnFields,
  onDeleteColumn,
}: ColumnListElementProps) {
  // Track the Selected Column for update or expand
  const [selectedColumn, setSelectedColumn] = useState<DataSourceColumn | null>(
    null
  );

  // Used to change the style of the hover effect and background color of the selected column
  const selected_style = (col: DataSourceColumn) => {
    if (!(selectedColumn && col.id == selectedColumn.id))
      return "hover:bg-slate-700 dark:hover:bg-slate-500";
    return "bg-slate-700 ";
  };

  //
  const onDelete = (e: React.MouseEvent, col_id: string) => {
    e.stopPropagation();
    onDeleteColumn(col_id);
  };

  return (
    <div className="space-y-4">
      {columns.map((col) => (
        <Card
          key={col.id}
          className={`text-white cursor-pointer transition-all duration-300 bg-gray-600 ${selected_style(
            col
          )}`}
          onClick={() =>
            col.id != selectedColumn?.id
              ? setSelectedColumn(col)
              : setSelectedColumn(null)
          }
        >
          {selectedColumn?.id != col.id ? (
            <>
              <CardHeader>
                <div className="flex items-center justify-between gap-2">
                  {col.name} ({col.type})
                  <Button
                    onClick={(e: React.MouseEvent) => onDelete(e, col.id)}
                  >
                    <Trash2 className="text-red-500" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-white">
                  {col.description}
                </CardDescription>
              </CardContent>
            </>
          ) : (
            <div className="mx-10 my-5">
              <CardContent
                onClick={(e: React.MouseEvent) => e.stopPropagation()}
              >
                <GenericForm
                  schema={CreateDataSourceColumnSchema}
                  fields={createColumnFields}
                  onSubmit={onCreateColumn}
                  isLoading={isColumnCreationPending}
                  defaultValues={{
                    dataSourceId: data_source_id,
                    description: col.description,
                    name: col.name,
                    type: col.type,
                  }}
                />
              </CardContent>
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}
