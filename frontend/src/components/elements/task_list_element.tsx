import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Task, taskSchema } from "@/types/task.type";
import { TaskDetailModal } from "@/components/elements/task_detail_modal_element";
import { useListSchemaFromFields } from "@/hooks/useListSchemaFromField";
import { endpoints } from "@/utils/endpoints";
import { Button } from "../ui/button";
import { Trash2 } from "lucide-react";
import { useDeleteSchema } from "@/hooks/useDeleteSchema";
interface TaskListProps {
  dataSourceId: string;
  isPanelOpen: boolean;
  closePanel: () => void;
}

export default function TaskList({
  isPanelOpen,
  dataSourceId,
  closePanel,
}: TaskListProps) {
  const [selectedTask, setSelectedTask] = useState<Task | undefined>();
  const [hoverTask, setHoverTask] = useState<Task | undefined>();

  const { data: tasks, isFetching } = useListSchemaFromFields(
    endpoints.tasks,
    "data-source",
    {
      id: dataSourceId,
    },
    taskSchema
  );
  const { mutateAsync: deleteTask } = useDeleteSchema(endpoints.tasks);

  const onCloseModal = () => {
    closePanel();
    setSelectedTask(undefined);
  };
  const onDelete = (e: React.MouseEvent, task: Task) => {
    e.stopPropagation();
    deleteTask(task.id);
  };
  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <ScrollArea className="h-[600px] pr-4">
        {tasks?.slice(0, 10).map((task) => (
          <Card
            key={task.id}
            className="mb-4 cursor-pointer"
            onClick={() => setSelectedTask(task)}
            onMouseEnter={() => setHoverTask(task)}
            onMouseLeave={() => setHoverTask(undefined)}
          >
            <CardHeader>
              <CardTitle className="flex items-center justify-between gap-2">
                {task.title}

                <div
                  className={`flex flex-row-reverse ${
                    hoverTask?.id == task.id ? "" : "opacity-0"
                  }`}
                >
                  <Button
                    className=" text-red-500"
                    variant="outline"
                    onClick={(e) => onDelete(e, task)}
                  >
                    <Trash2 />
                  </Button>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent className="flex flex-row justify-between items-center">
              <p className="text-sm text-gray-500">
                Function: {task.signatureFunction}
              </p>
            </CardContent>
          </Card>
        ))}
      </ScrollArea>
      {(selectedTask || isPanelOpen) && (
        <TaskDetailModal
          task={isPanelOpen ? undefined : selectedTask}
          onModalClose={onCloseModal}
          dataSoureId={dataSourceId}
          isCreate={isPanelOpen}
        />
      )}
    </div>
  );
}
