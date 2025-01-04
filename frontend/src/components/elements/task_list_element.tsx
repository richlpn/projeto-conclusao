import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Dialog, DialogContent, DialogHeader } from "@/components/ui/dialog";
import { Requirement } from "@/types/requirement.type";
import { Task, taskCreateSchema, taskSchema } from "@/types/task.type";
import { Description, DialogTitle } from "@radix-ui/react-dialog";
import { Label } from "@radix-ui/react-label";
import { Button } from "../ui/button";
import { useCreateSchema } from "@/hooks/useMutateSchema";
import { endpoints } from "@/utils/endpoints";

interface TaskListProps {
  dataSourceId: string;
  requirement: Requirement | null;
  isPanelOpen: boolean;
  closePanel: () => void;
}

export default function TaskList({ requirement }: TaskListProps) {
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  const { mutateAsync: createColumn } = useCreateSchema(
    endpoints.tasks,
    taskCreateSchema,
    taskSchema
  );

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <ScrollArea className="h-[600px] pr-4">
        {requirement?.tasks.slice(0, 10).map((task) => (
          <Card
            key={task.id}
            className="mb-4 cursor-pointer hover:bg-gray-100 transition-colors"
            onClick={() => setSelectedTask(task)}
          >
            <CardHeader>
              <CardTitle>{task.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">
                Function: {task.signatureFunction}
              </p>
            </CardContent>
          </Card>
        ))}
      </ScrollArea>
      {selectedTask ? (
        <Dialog
          open={selectedTask !== null}
          onOpenChange={() => setSelectedTask(null)}
        >
          <DialogContent className="flex flex-col gap-6 max-w-xl">
            <DialogHeader className="text-2xl ">
              <DialogTitle>{selectedTask.title}</DialogTitle>
            </DialogHeader>
            <div>
              <Label className="font-bold ">Description</Label>
              <p className="mb-4">{selectedTask.description}</p>
              <Label className="font-bold ">Function name</Label>
              <p className="mb-2">{selectedTask.signatureFunction}</p>
            </div>
            <div className="flex space-x-2">
              <Button variant="outline">Edit</Button>
              <Button variant="destructive">Delete</Button>
            </div>
          </DialogContent>
          <Description>Edit task</Description>
        </Dialog>
      ) : null}
    </div>
  );
}
