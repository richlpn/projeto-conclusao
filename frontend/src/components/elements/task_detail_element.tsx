import { Button } from "@/components/ui/button";
import { Task } from "@/types/task.type";
import { Label } from "../ui/label";

interface TaskDetailProps {
  task: Task;
}

export default function TaskDetail({ task }: TaskDetailProps) {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">{task.title}</h2>
        <Label>Description</Label>
        <p className="mb-4">{task.description}</p>
        <Label>Function name</Label>
        <p className="mb-2">{task.signatureFunction}</p>

        <div className="flex space-x-2">
          <Button>Start</Button>
          <Button variant="outline">Edit</Button>
          <Button variant="destructive">Delete</Button>
        </div>
      </div>
    </div>
  );
}
