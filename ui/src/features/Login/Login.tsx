import {
  FormError,
  FormField,
  FormLabel,
  Input,
  LoginWrap,
} from "../../ui-library";
import React, { useState } from "react";

import { Button } from "@mui/material";
import { login } from "../../services";
import { useForm } from "react-hook-form";

type LoginForm = {
  email: string;
  password: string;
};

type Props = {
  isAuthenticated: boolean;
};

export const Login: React.FC<Props> = ({ isAuthenticated }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>();
  const [serverError, setServerError] = useState<string>();

  const onSubmit = async (data: LoginForm) => {
    setServerError("");
    const error = await login(data.email, data.password);
    if (error) {
      setServerError(error.message);
    } else {
      window.location.href = window.location.origin;
    }
  };

  if (isAuthenticated) {
    window.location.href = window.location.origin;
  }

  return (
    <LoginWrap>
      <form onSubmit={handleSubmit(onSubmit)}>
        <h1>Reporter Login</h1>
        <FormField>
          <FormLabel htmlFor="email">Username</FormLabel> <br />
          <Input
            id="email"
            {...register("email", {
              required: "username is required",
            })}
          />
          <FormError>{errors.email?.message}</FormError>
        </FormField>
        <FormField>
          <FormLabel htmlFor="password">Password</FormLabel> <br />
          <Input
            id="password"
            type="password"
            {...register("password", { required: "password is required" })}
          />
          <FormError>{errors.password?.message}</FormError>
        </FormField>
        <Button type="submit">Login</Button>
        <FormError>{serverError}</FormError>
      </form>
    </LoginWrap>
  );
};
