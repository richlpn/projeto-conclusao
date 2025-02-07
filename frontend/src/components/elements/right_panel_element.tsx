import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Copy, Check } from "lucide-react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useCopyToClipboard } from "@/hooks/useCopyToClipboard";
import { DataSource } from "@/types/data_source.type";
import { useCreatePipeline } from "@/hooks/useCreatePipeline";
import { endpoints } from "@/utils/endpoints";
import { PlayIcon } from "lucide-react";

interface RightPanelProps {
  schema: DataSource;
  setSchema: (schema: DataSource) => void;
}

export function RightPanelElement({ schema, setSchema }: RightPanelProps) {
  const { isCopied, copyToClipboard } = useCopyToClipboard();
  const { mutateAsync: generatePipeline } = useCreatePipeline({
    endpoint: endpoints.script,
  });

  const handleGenerateScript = async () => {
    generatePipeline(schema.id)
      .then((res) => {
        console.log("Script generated", res);
        setSchema({
          ...schema,
          script: res,
        });
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return (
    <div className="h-full flex flex-col bg-black">
      <div className="flex gap-5 mx-3 mt-4">
        <Button
          variant="outline"
          className="col-start-8"
          size="sm"
          onClick={handleGenerateScript}
        >
          <PlayIcon className="text-green-600" />
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => copyToClipboard(schema.script || "")}
          className="text-xs"
        >
          {isCopied ? <Check /> : <Copy />}
        </Button>
      </div>
      <ScrollArea className="flex-grow">
        <SyntaxHighlighter
          language="python"
          style={vscDarkPlus}
          showLineNumbers={true}
          wrapLines={true}
          customStyle={{
            margin: 0,
            padding: "1rem",
            fontSize: "0.875rem",
            backgroundColor: "transparent",
          }}
          editable={true}
        >
          {schema.script || ""}
        </SyntaxHighlighter>
        <ScrollBar orientation="vertical" />
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </div>
  );
}
