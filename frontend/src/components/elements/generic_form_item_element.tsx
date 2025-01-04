import { ControllerRenderProps, Path } from "react-hook-form";
import { FormControl, FormItem, FormLabel, FormMessage } from "../ui/form";
import { Input } from "../ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Textarea } from "../ui/textarea";

export interface FieldOption {
  value: any;
  label: string;
}

export interface FormFieldInterface<T> {
  name: Path<T>;
  label: string;
  type?: "select" | "input" | "textarea";
  placeholder?: string;
  options?: FieldOption[];
}

interface ItemProps<T> {
  field: FormFieldInterface<T>;
  formField: ControllerRenderProps;
}
export function GenericFormItem<T>({ field, formField }: ItemProps<T>) {
  let item;
  if (field.type == "select" && field.options) {
    const options = field.options.map((option) => (
      <SelectItem key={option.value} value={option.value}>
        {option.label}
      </SelectItem>
    ));
    item = (
      <Select
        name={field.name}
        value={formField.value}
        onValueChange={formField.onChange}
        disabled={formField.disabled}
      >
        <SelectTrigger aria-label={field.label}>
          <SelectValue placeholder={field.placeholder ?? "Select an option"} />
        </SelectTrigger>
        <SelectContent>{options}</SelectContent>
      </Select>
    );
  } else if (field.type == "textarea") {
    item = (
      <Textarea
        placeholder={field.placeholder}
        className="w-full"
        defaultValue={formField.value}
        name={formField.name}
        onChange={formField.onChange}
      />
    );
  } else {
    item = (
      <Input type={"text"} placeholder={field.placeholder} {...formField} />
    );
  }
  return (
    <FormItem>
      <FormLabel>{field.label}</FormLabel>
      <FormControl>{item}</FormControl>
      <FormMessage />
    </FormItem>
  );
}
