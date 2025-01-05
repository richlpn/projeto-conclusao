import { TaskCreate, taskCreateSchema } from "@/types/task.type";
import { FormFieldInterface } from "../elements/generic_form_item_element";
import { Path } from "react-hook-form";
import { FormSubmitResponse, GenericForm } from "../elements/form_element";

export const createColumnFields: FormFieldInterface<TaskCreate>[] = [
  {
    name: "title" as Path<TaskCreate>,
    label: "Title",
    placeholder: "Enter task title",
  },
  {
    name: "signatureFunction" as Path<TaskCreate>,
    label: "Function Name",
    placeholder: "Enter the function name",
  },
  {
    name: "description" as Path<TaskCreate>,
    label: "Description",
    placeholder: "Enter column description",
    type: "textarea",
  },
];
export interface TaskFormProps {
  onSubmit: (response: FormSubmitResponse<TaskCreate>) => Promise<void>;
  isPending: boolean;
  dataSourceId: string;
  task?: TaskCreate;
}
export const TaskForm = ({
  onSubmit,
  dataSourceId,
  task,
  isPending,
}: TaskFormProps) => {
  const defaultValues: {
    [key: string]: any;
    dataSourceId: string;
  } = { dataSourceId: dataSourceId };

  if (task) {
    Object.entries(task).forEach(([key, value]) => {
      defaultValues[key] = value;
    });
  }
  return (
    <GenericForm
      schema={taskCreateSchema}
      fields={createColumnFields}
      onSubmit={onSubmit}
      isLoading={isPending}
      defaultValues={defaultValues}
    />
  );
};
