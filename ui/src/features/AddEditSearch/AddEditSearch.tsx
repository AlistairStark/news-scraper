import {
  Button,
  FormError,
  FormField,
  FormLabel,
  Input,
  StandardDialog,
  TextArea,
  MediumHeader,
} from "../../ui-library";

import React, { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { axios } from "../../services";
import { AddOrEdit, ApiRoutes, Search } from "../../types";
import { Checkbox, Tooltip } from "@mui/material";

type AddEditForm = {
  name: string;
  description?: string;
  id?: number;
  is_rss?: boolean;
};

type Props = {
  type: AddOrEdit;
  open: boolean;
  selected?: Search;
  onSuccess: () => void;
  onClose: () => void;
};

export const AddEditSearch: React.FC<Props> = ({
  type,
  open,
  selected,
  onSuccess,
  onClose,
}) => {
  const {
    register,
    control,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<AddEditForm>({
    mode: "onChange",
    defaultValues:
      type === AddOrEdit.Edit
        ? {
            id: selected?.id,
            name: selected?.name,
            description: selected?.description,
            is_rss: selected?.is_rss,
          }
        : {
            is_rss: false,
          },
  });
  const [serverError, setServerError] = useState("");

  const onSubmit = async (data: AddEditForm) => {
    const isEdit = AddOrEdit.Edit === type;
    setServerError("");
    const apiMethod = isEdit ? axios.put : axios.post;
    try {
      await apiMethod(ApiRoutes.Search, data);
      onSuccess();
    } catch (err) {
      setServerError("Something went wrong!");
    }
  };

  return (
    <StandardDialog open={open} onClose={onClose}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <MediumHeader>{type} Search</MediumHeader>
        <FormField>
          <FormLabel htmlFor="name">Name</FormLabel> <br />
          <Input
            id="name"
            {...register("name", {
              required: "name is required",
            })}
          />
          <FormError>{errors.name?.message}</FormError>
        </FormField>
        <FormField>
          <FormLabel htmlFor="description">Description</FormLabel> <br />
          <TextArea id="description" rows={5} {...register("description")} />
        </FormField>
        <Tooltip title="Will set search to scrape an RSS feed. Search terms will be ignored.">
          <FormField>
            <FormLabel htmlFor="description">RSS Feed</FormLabel> <br />
            <Controller
              name="is_rss"
              control={control}
              render={({ field }) => (
                <Checkbox
                  checked={!!field.value}
                  onChange={(e) => field.onChange(e.target.checked)}
                />
              )}
            />
          </FormField>
        </Tooltip>
        <Button type="submit" variant="outlined" disabled={!isValid}>
          {type}
        </Button>
        <FormError>{serverError}</FormError>
      </form>
    </StandardDialog>
  );
};
