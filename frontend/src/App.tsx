import { HeaderElement } from "@/components/elements/header_element";
import LeftPanelElement from "@/components/elements/left_panel_element";
import {
  ResizablePanel,
  ResizablePanelGroup,
  ResizableHandle,
} from "./components/ui/resizable";
import { MiddlePanel } from "./components/elements/middle_panel_element";
import { DataSourceSchema } from "./types/data_source.type";
import { useState } from "react";
import { RightPanelElement } from "./components/elements/right_panel_element";

export function App() {
  const [selectedSchema, setSelectedSchema] = useState<DataSourceSchema | null>(
    null
  );

  const handleSelectSchema = (schema: DataSourceSchema) => {
    selectedSchema != null && schema == selectedSchema
      ? setSelectedSchema(null)
      : setSelectedSchema(schema);
  };

  return (
    <div className="bg-slate-400 min-h-screen">
      <HeaderElement />
      <ResizablePanelGroup direction="horizontal" className="min-h-screen">
        <ResizablePanel defaultSize={20} minSize={10}>
          <LeftPanelElement
            selectedSchema={selectedSchema}
            onSelectSchema={handleSelectSchema}
          />
        </ResizablePanel>
        <ResizableHandle />
        {selectedSchema ? (
          <>
            <ResizablePanel defaultSize={25} minSize={20}>
              <MiddlePanel selectedSchema={selectedSchema} />
            </ResizablePanel>
            <ResizableHandle />
            <ResizablePanel defaultSize={50} minSize={30}>
              <RightPanelElement schema={selectedSchema} />
            </ResizablePanel>
          </>
        ) : (
          <ResizablePanel
            defaultSize={75}
            minSize={20}
            className="flex justify-center items-center"
          >
            Select a data source
          </ResizablePanel>
        )}
      </ResizablePanelGroup>
    </div>
  );
}
