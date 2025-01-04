import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { ColumnForm, ColumnFormProps } from "../forms/column_form";

interface ColumnPanelProps {
  isColumnFormOpen: boolean;
  onCloseColumnForm: () => void;
  formProps: ColumnFormProps;
}
export const CreateColumnModal = ({
  isColumnFormOpen,
  onCloseColumnForm,
  formProps,
}: ColumnPanelProps) => {
  // Takes the fields of the form as an schema and request the creation of a new schema
  return (
    <Dialog open={isColumnFormOpen} onOpenChange={onCloseColumnForm}>
      <DialogTrigger asChild></DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Column</DialogTitle>
          <DialogDescription>Describe the new column</DialogDescription>
        </DialogHeader>
        <ColumnForm {...formProps} />
      </DialogContent>
    </Dialog>
  );
};
