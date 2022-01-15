import {
  Button,
  FormFieldSideways,
  Input,
  FormLabel,
  FlexWrap,
} from "../../../ui-library";

import React from "react";
import { useForm } from "react-hook-form";

export type NewUrlForm = {
  name: string;
  url: string;
};

type Props = {
  onSubmit: (data: NewUrlForm) => void;
};

export const AddUrlForm: React.FC<Props> = ({ onSubmit }) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { isValid },
  } = useForm<NewUrlForm>({
    mode: "onChange",
  });

  const submit = (data: NewUrlForm) => {
    reset();
    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit(submit)}>
      <FormFieldSideways>
        <FormLabel>Name</FormLabel>
        <Input
          id="name"
          {...register("name", {
            required: true,
          })}
        />
      </FormFieldSideways>
      <FormFieldSideways>
        <FormLabel>Url</FormLabel>
        <Input
          id="url"
          {...register("url", {
            required: true,
          })}
        />
      </FormFieldSideways>
      <FlexWrap justifyContent="left">
        <Button
          type="submit"
          variant="outlined"
          disabled={!isValid}
          sx={{ textAlign: "left" }}
        >
          Add Url
        </Button>
      </FlexWrap>
    </form>
  );
};
