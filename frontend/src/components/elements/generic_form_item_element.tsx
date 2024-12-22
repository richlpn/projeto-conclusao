import { FormControl, FormItem, FormLabel, FormMessage } from "../ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Input } from "../ui/input";
import { ControllerRenderProps, Path } from "react-hook-form";

export interface FieldOption {
  value: any;
  label: string;
}

export interface FormFieldInterface<T> {
  name: Path<T>;
  label: string;
  type?: "select" | "input";
  placeholder?: string;
  options?: FieldOption[];
}

interface ItemProps<T> {
  field: FormFieldInterface<T>;
  formField: ControllerRenderProps;
}
export function GenericFormItem<T>({ field, formField }: ItemProps<T>) {
  return (
    <FormItem>
      <FormLabel>{field.label}</FormLabel>

      <FormControl>
        {field.type == "select" && field.options ? (
          <Select
            name={field.name}
            value={formField.value}
            onValueChange={formField.onChange}
            disabled={formField.disabled}
          >
            <SelectTrigger aria-label={field.label}>
              <SelectValue
                placeholder={field.placeholder ?? "Select an option"}
              />
            </SelectTrigger>
            <SelectContent>
              {field.options.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        ) : (
          <Input type={"text"} placeholder={field.placeholder} {...formField} />
        )}
      </FormControl>
      <FormMessage />
    </FormItem>
  );
}
