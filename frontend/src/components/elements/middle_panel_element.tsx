import { DataSource } from "@/types/data_source.type";
import { PlayIcon, PlusIcon } from "lucide-react";
import { Button } from "../ui/button";
import { useState } from "react";
import { ColumnPanel } from "./column_panel_element";
import TaskList from "./task_list_element";

interface MiddlePanelProps {
  selectedSchema: DataSource;
}

export function MiddlePanel({ selectedSchema }: MiddlePanelProps) {
  // State of the create column form modal (Open/Closed)
  const [openCreateForm, setOpenCreateForm] = useState(false);
  const [showTasks, setShowTasks] = useState(false);

  const closePanel = () => setOpenCreateForm(false);
  const alternatePanel = () => setShowTasks(!showTasks);

  const panel = showTasks ? (
    <TaskList
      dataSourceId={selectedSchema.id}
      isPanelOpen={openCreateForm}
      closePanel={closePanel}
    />
  ) : (
    <ColumnPanel
      onCloseColumnForm={closePanel}
      selectedSchemaID={selectedSchema.id}
      isFormOpen={openCreateForm}
    />
  );

  return (
    <div className="h-full p-4 flex flex-col gap-2">
      <div className="grid grid-cols-8 gap-2">
        <Button
          variant={showTasks ? "ghost" : "default"}
          className="col-start-4 px-8 mr-2  animate-in"
          onClick={alternatePanel}
        >
          Columns
        </Button>
        <Button
          variant={showTasks ? "default" : "ghost"}
          className="col-start-5 ml-5 px-7 animate-in"
          onClick={alternatePanel}
        >
          Tasks
        </Button>

        <Button className="col-start-7" onClick={() => setOpenCreateForm(true)}>
          <PlusIcon />
        </Button>
        <Button variant="outline" className="col-start-8">
          <PlayIcon className="text-green-600" />
        </Button>
      </div>
      <div className="mx-4">{panel}</div>
    </div>
  );
}
