import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Copy, Check } from "lucide-react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useCopyToClipboard } from "@/hooks/useCopyToClipboard";
import { DataSource } from "@/types/data_source.type";

interface RightPanelProps {
  schema: DataSource;
  setSchema: (schema: DataSource) => void;
}
export function RightPanelElement({ schema, setSchema }: RightPanelProps) {
  const { isCopied, copyToClipboard } = useCopyToClipboard();
  return (
    <div className="h-full flex flex-col bg-black">
      <div className="flex justify-end ">
        <Button
          variant="outline"
          size="sm"
          onClick={() => copyToClipboard(schema.script || "")}
          className="text-xs"
        >
          {isCopied ? (
            <Check className="mr-2 h-4 w-4" />
          ) : (
            <Copy className="mr-2 h-4 w-4" />
          )}
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
