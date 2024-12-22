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

interface CreateSchemaModalProps {
  onClose: () => void;
  isOpen: boolean;
  isLoading: boolean;
  handleSubmit: (
    formResponse: FormSubmitResponse<DataSourceCreate>
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

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        className="rounded-3xl"
        aria-describedby="form create schema"
      >
        {isLoadingTypes || !typesData ? (
          <div>Loading Types</div>
        ) : (
          <DialogHeader>
            <DialogTitle>Create New Schema</DialogTitle>
            <GenericForm
              schema={dataSourceCreateSchema}
              fields={dataSourceForm(typesData?.items)}
              onSubmit={handleSubmit}
              isLoading={isLoading}
            />
          </DialogHeader>
        )}
      </DialogContent>
    </Dialog>
  );
}
