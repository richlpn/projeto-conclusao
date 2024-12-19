import { zodResolver } from "@hookform/resolvers/zod";
import { Path, useForm, UseFormReturn } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

export interface FormField<T> {
  name: Path<T>;
  label: string;
  type?: string;
  placeholder?: string;
}

export interface FormSubmitResponse<T> {
  schema: T;
  form: UseFormReturn;
}

interface GenericFormProps<T extends z.ZodType> {
  schema: T;
  onSubmit: (
    submit_form: FormSubmitResponse<z.infer<T>>
  ) => Promise<z.infer<T> | void>;
  fields: FormField<z.infer<T>>[];
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
    defaultValues: defaultValues as z.infer<T>,
  });

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit((schema: T) =>
          onSubmit({ schema: schema, form: form })
        )}
        className="space-y-8"
      >
        {fields.map((field) => (
          <FormField
            key={String(field.name)}
            control={form.control}
            name={field.name}
            render={({ field: formField }) => (
              <FormItem>
                <FormLabel>{field.label}</FormLabel>
                <FormControl>
                  <Input
                    type={field.type || "text"}
                    placeholder={field.placeholder}
                    {...formField}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        ))}
        <Button type="submit" disabled={isLoading}>
          {isLoading ? "Submitting..." : "Submit"}
        </Button>
      </form>
    </Form>
  );
}
