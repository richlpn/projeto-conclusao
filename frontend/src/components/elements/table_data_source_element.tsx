import React from "react";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { useFetchAllData } from "@/hooks/useFetchAllData";
import { dataSourceSchema } from "@/types/data_source.type";
import { endpoints } from "@/utils/endpoints";

const IGNORE_COLUMS = ["columns", "id"];
const COLUMNS = Object.keys(dataSourceSchema.shape)
  .filter((column) => !IGNORE_COLUMS.includes(column.toLowerCase()))
  .map((col) => col[0].toUpperCase() + col.substring(1).toLowerCase());

interface Row {
  [key: string]: any; // index signature
}

export const TableDataSourceElement: React.FC = () => {
  const { data, isLoading, error } = useFetchAllData(
    dataSourceSchema,
    endpoints.data_source.getAll(0, 100)
  );

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="container mx-auto p-4">
      <Table>
        <TableHeader>
          <TableRow>
            {COLUMNS.map((column) => (
              <TableHead key={column}>{column}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data?.map((row, index) => (
            <TableRow key={index}>
              {COLUMNS.map((column) => (
                <TableCell key={column}>
                  {(row as Record<string, any>)[column.toLowerCase()]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};
