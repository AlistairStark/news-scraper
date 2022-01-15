import styled from "styled-components";

export const Input = styled.input`
  padding: 10px;
`;

export const TextArea = styled.textarea`
  padding: 10px;
`;

export const FormField = styled.div`
  padding: 5px 0;
`;

export const FormFieldSideways = styled.div`
  display: flex;
  justify-content: left;
  align-items: center;
  margin-bottom: 10px;
  label {
    min-width: 50px;
  }
`;

export const FormError = styled.p`
  color: red;
  font-size: 12px;
`;

export const FormLabel = styled.label`
  padding-right: 10px;
  font-size: 12px;
`;
