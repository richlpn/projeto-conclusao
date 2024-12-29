import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { DataSourceTypeSchema } from "@/types/data_source_type.type";
import { endpoints } from "@/utils/endpoints";
import {
  dataSourceCreateSchema,
  DataSourceCreate,
} from "@/types/data_source.type";

import { useListSchema } from "@/hooks/useFetchAllData";

import { FormSubmitResponse, GenericForm } from "./form_element";
import dataSourceForm from "../forms/dataSourceForm";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Upload } from "lucide-react";
import { useRef } from "react";

interface CreateSchemaModalProps {
  onClose: () => void;
  isOpen: boolean;
  isLoading: boolean;
  handleSubmit: (
    formResponse: FormSubmitResponse<DataSourceCreate> | null,
    file: FileList | null
  ) => Promise<void>;
}

export function CreateDataSourceModal({
  onClose,
  isLoading,
  handleSubmit,
  isOpen,
}: CreateSchemaModalProps) {
  const { data: typesData, isLoading: isLoadingTypes } = useListSchema(
    endpoints.data_source_type,
    DataSourceTypeSchema,
    {
      limit: 100,
      skip: 0,
    }
  );
  const fileInputRef = useRef<HTMLInputElement>(null);
  const handleFileClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        className="rounded-3xl"
        aria-describedby="form create schema"
      >
        {isLoadingTypes || !typesData ? (
          <div>Loading Types</div>
        ) : (
          <DialogHeader className="flex flex-col gap-5">
            <DialogTitle>Create New Schema</DialogTitle>
            <Input
              type="file"
              ref={fileInputRef}
              className="hidden"
              accept=".txt"
              onChange={(e) => handleSubmit(null, e.target.files)}
            />
            <Button
              onClick={handleFileClick}
              variant="outline"
              className="w-full"
            >
              <Upload className="mr-2 h-4 w-4" />
              From Document
            </Button>
            <GenericForm
              schema={dataSourceCreateSchema}
              fields={dataSourceForm(typesData?.items)}
              onSubmit={(e) => handleSubmit(e, null)}
              isLoading={isLoading}
            />
          </DialogHeader>
        )}
      </DialogContent>
    </Dialog>
  );
}
