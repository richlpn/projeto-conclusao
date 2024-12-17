import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Copy, Check } from "lucide-react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useCopyToClipboard } from "@/hooks/useCopyToClipboard";
import { DataSourceSchema } from "@/types/data_source.type";

const pythonScript = `
def example_function():
    print("This is a long Python script")
    for i in range(10):
        print(f"Line {i + 1}")
    
    # Add more Python code here
    def nested_function():
        return "Hello from nested function"
    
    result = nested_function()
    print(result)

if __name__ == "__main__":
    example_function()
  `;

interface RightPanelProps {
  schema: DataSourceSchema;
}
export function RightPanelElement({ schema }: RightPanelProps) {
  const { isCopied, copyToClipboard } = useCopyToClipboard();
  return (
    <div className="h-full flex flex-col bg-black">
      <div className="flex justify-end ">
        <Button
          variant="outline"
          size="sm"
          onClick={() => copyToClipboard(pythonScript)}
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
        >
          {pythonScript}
        </SyntaxHighlighter>
      </ScrollArea>
    </div>
  );
}
