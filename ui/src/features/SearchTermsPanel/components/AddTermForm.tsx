import { Button, FormField, Input } from "../../../ui-library";

import React from "react";
import { useForm } from "react-hook-form";

export type NewTermForm = {
  term: string;
};

type Props = {
  onSubmit: (data: NewTermForm) => void;
};

export const AddTermForm: React.FC<Props> = ({ onSubmit }) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { isValid },
  } = useForm<NewTermForm>({
    mode: "onChange",
  });

  const submit = (data: NewTermForm) => {
    reset();
    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit(submit)}>
      <FormField>
        <Input
          id="term"
          {...register("term", {
            required: true,
          })}
        />
      </FormField>
      <Button type="submit" variant="outlined" disabled={!isValid}>
        Add Term
      </Button>
    </form>
  );
};
