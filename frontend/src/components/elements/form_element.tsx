import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, UseFormReturn } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Form, FormField } from "@/components/ui/form";
import {
  FormFieldInterface,
  GenericFormItem,
} from "@/components/elements/generic_form_item_element";

export interface FormSubmitResponse<T> {
  schema: T;
  form: UseFormReturn;
}

interface GenericFormProps<T extends z.ZodType> {
  schema: T;
  onSubmit: (
    submit_form: FormSubmitResponse<z.infer<T>>
  ) => Promise<z.infer<T> | void>;
  fields: FormFieldInterface<z.infer<T>>[];
  isLoading: boolean;
  defaultValues?: Partial<z.infer<T>>;
}

export function GenericForm<T extends z.ZodType>({
  schema,
  onSubmit,
  fields,
  isLoading,
  defaultValues,
}: GenericFormProps<T>) {
  const form = useForm<z.infer<T>>({
    resolver: zodResolver(schema),
    defaultValues: defaultValues
      ? (defaultValues as z.infer<T>)
      : ({} as z.infer<T>),
  });

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit((schema: T) =>
          onSubmit({ schema: schema, form: form })
        )}
        className="space-y-2"
      >
        {fields.map((field) => (
          <FormField
            key={String(field.name)}
            control={form.control}
            name={field.name}
            render={({ field: formField }) => (
              <GenericFormItem field={field} formField={formField} />
            )}
          />
        ))}
        <div className="flex flex-row-reverse">
          <Button type="submit" disabled={isLoading}>
            {isLoading ? "Submitting..." : "Submit"}
          </Button>
        </div>
      </form>
    </Form>
  );
}
