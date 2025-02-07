import { HeaderElement } from "@/components/elements/header_element";
import LeftPanelElement from "@/components/elements/left_panel_element";
import {
  ResizablePanel,
  ResizablePanelGroup,
  ResizableHandle,
} from "./components/ui/resizable";
import { MiddlePanel } from "./components/elements/middle_panel_element";
import { DataSource } from "./types/data_source.type";
import { useState } from "react";
import { RightPanelElement } from "./components/elements/right_panel_element";
import { Toaster } from "./components/ui/toaster";

export function App() {
  const [selectedSchema, setSelectedSchema] = useState<DataSource | null>(null);

  const handleSelectSchema = (schema: DataSource) => {
    schema == selectedSchema
      ? setSelectedSchema(null)
      : setSelectedSchema(schema);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <HeaderElement />
      <ResizablePanelGroup
        direction="horizontal"
        className="min-h-screen max-h-screen"
      >
        <ResizablePanel id="left_bar" defaultSize={25} minSize={10}>
          <LeftPanelElement
            selectedSchema={selectedSchema}
            onSelectSchema={handleSelectSchema}
          />
        </ResizablePanel>
        <ResizableHandle />
        {selectedSchema ? (
          <>
            <ResizablePanel id="middle" defaultSize={35} minSize={20}>
              <MiddlePanel selectedSchema={selectedSchema} />
            </ResizablePanel>
            <ResizableHandle id="handle" />
            <ResizablePanel id="code" defaultSize={40} minSize={30}>
              <RightPanelElement
                schema={selectedSchema}
                setSchema={setSelectedSchema}
              />
            </ResizablePanel>
          </>
        ) : (
          <ResizablePanel
            id="placeholder"
            defaultSize={75}
            minSize={20}
            className="flex justify-center items-center"
          >
            Select a data source
          </ResizablePanel>
        )}
      </ResizablePanelGroup>
      <Toaster />
    </div>
  );
}
