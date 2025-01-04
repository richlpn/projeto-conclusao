import {
  CreateDataSourceColumn,
  CreateDataSourceColumnSchema,
} from "@/types/data_source_column.type";
import { Path } from "react-hook-form";
import { FormSubmitResponse, GenericForm } from "../elements/form_element";
import { FormFieldInterface } from "../elements/generic_form_item_element";

export const createColumnFields: FormFieldInterface<CreateDataSourceColumn>[] =
  [
    {
      name: "name" as Path<CreateDataSourceColumn>,
      label: "Column Name",
      placeholder: "Enter column name",
    },
    {
      name: "type" as Path<CreateDataSourceColumn>,
      label: "Column Type",
      placeholder: "Enter column type",
    },
    {
      name: "description" as Path<CreateDataSourceColumn>,
      label: "Description",
      placeholder: "Enter column description",
      type: "textarea",
    },
  ];

export interface ColumnFormProps {
  onSubmit: (
    response: FormSubmitResponse<CreateDataSourceColumn>
  ) => Promise<void>;
  isPending: boolean;
  dataSourceSchemaId: string;
  column?: CreateDataSourceColumn;
}

export const ColumnForm = ({
  onSubmit,
  dataSourceSchemaId,
  column,
  isPending,
}: ColumnFormProps) => {
  const defaultValues: {
    [key: string]: any;
    dataSourceId: string;
  } = { dataSourceId: dataSourceSchemaId };

  if (column) {
    Object.entries(column).forEach(([key, value]) => {
      defaultValues[key] = value;
    });
  }
  return (
    <GenericForm
      schema={CreateDataSourceColumnSchema}
      fields={createColumnFields}
      onSubmit={onSubmit}
      isLoading={isPending}
      defaultValues={defaultValues}
    />
  );
};
