import { Dialog, DialogContent, DialogHeader } from "@/components/ui/dialog";
import { Description, DialogTitle } from "@radix-ui/react-dialog";
import { Button } from "../ui/button";
import {
  Task,
  TaskCreate,
  taskCreateSchema,
  taskSchema,
} from "@/types/task.type";
import { TaskForm } from "../forms/task_form";
import { useUpdateSchema } from "@/hooks/useUpdateSchema";
import { endpoints } from "@/utils/endpoints";
import { FormSubmitResponse } from "./form_element";
import { useToast } from "@/hooks/use-toast";
import { useCreateSchema } from "@/hooks/useCreateSchema";
import { useMutateGenerateTasks } from "@/hooks/useMutateTaskFromDataSource";

interface TaskDetailProps {
  dataSoureId: string;
  task?: Task;
  onModalClose: () => void;
  isCreate: boolean;
}
export const TaskDetailModal = ({
  task,
  onModalClose,
  dataSoureId,
  isCreate,
}: TaskDetailProps) => {
  const { toast } = useToast();

  const { mutateAsync: createTask } = useCreateSchema(
    endpoints.tasks,
    taskCreateSchema,
    taskSchema
  );

  const { mutateAsync: mutateGenTasks, isPending: isGeneratingTasks } =
    useMutateGenerateTasks(endpoints.tasks);

  const { mutateAsync: updateTask, isPending } = useUpdateSchema(
    endpoints.tasks,
    taskCreateSchema,
    taskSchema
  );
  const onSubmit = async (response: FormSubmitResponse<TaskCreate>) => {
    const { schema, form } = response;
    // An existing task was provided and it will be updated
    // Other wise a new will be created, either from the user input or automatically Generated
    if (task) {
      updateTask({ data: schema, id: task.id }).then(() =>
        toast({
          description: `${schema.title} was updated!`,
          title: "Task update",
          duration: 3000,
        })
      );
    } else {
      createTask(schema);
    }

    onModalClose();
    form.reset();
  };

  const onGenerate = async () => {
    await mutateGenTasks(dataSoureId);
  };
  return (
    <Dialog open={!!task || isCreate} onOpenChange={onModalClose}>
      <DialogContent className="flex flex-col gap-6 max-w-xl">
        <DialogHeader className="text-2xl ">
          <DialogTitle>{task ? task.title : "New Task"}</DialogTitle>
        </DialogHeader>
        {isCreate && (
          <Button className="w-full" onClick={onGenerate}>
            Generate
          </Button>
        )}
        <div>
          <TaskForm
            task={task}
            isPending={isPending}
            onSubmit={onSubmit}
            dataSourceId={dataSoureId}
          />
        </div>
      </DialogContent>
    </Dialog>
  );
};
