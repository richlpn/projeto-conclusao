import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

interface Task {
  id: string;
  name: string;
  description: string;
}

export function TaskList() {
  const [selectedTask, setSelectedTask] = useState<string | null>(null);
  const tasks: Task[] = [
    { id: "1", name: "Task 1", description: "Description for Task 1" },
    { id: "2", name: "Task 2", description: "Description for Task 2" },
    // Add more mock data as needed
  ];

  const [taskDescriptions, setTaskDescriptions] = useState<{
    [key: string]: string;
  }>(Object.fromEntries(tasks.map((task) => [task.id, task.description])));

  const handleDescriptionChange = (taskId: string, newDescription: string) => {
    setTaskDescriptions((prev) => ({ ...prev, [taskId]: newDescription }));
    // Here you would typically update the backend
  };

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <Card
          key={task.id}
          className="cursor-pointer"
          onClick={() => setSelectedTask(task.id)}
        >
          <CardHeader>
            <CardTitle>{task.name}</CardTitle>
          </CardHeader>
          {selectedTask === task.id && (
            <CardContent>
              <Textarea
                value={taskDescriptions[task.id]}
                onChange={(e) =>
                  handleDescriptionChange(task.id, e.target.value)
                }
                className="mt-2"
              />
            </CardContent>
          )}
        </Card>
      ))}
    </div>
  );
}
