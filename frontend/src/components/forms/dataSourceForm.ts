import { DataSourceCreate } from "@/types/data_source.type";
import { FormFieldInterface } from "../elements/generic_form_item_element";
import { DataSourceType } from "@/types/data_source_type.type";

export default (
  data: DataSourceType[]
): FormFieldInterface<DataSourceCreate>[] => {
  return [
    {
      name: "name",
      label: "Name",
      type: "input",
      placeholder: "Enter schema name",
    },
    {
      name: "type",
      label: "Type",
      type: "select",
      options: data.map((item) => ({
        value: item.id,
        label: item.name,
      })),
    },
  ];
};
