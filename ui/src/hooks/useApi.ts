import { useState } from "react";
import { axios } from "../services";
import { ApiRoutes } from "../types";
import { isEqual } from "lodash";

type Options = {
  params?: { [key: string]: any };
  body?: any;
  method?: "post" | "get" | "patch" | "delete" | "put";
};

export function useApi<Type>(
  url: ApiRoutes,
  options: Options = {
    method: "get",
  }
): {
  data: Type | undefined;
  error: string;
  loading: boolean;
  refetch: () => void;
} {
  const [data, setData] = useState<Type | undefined>(undefined);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [curOptions, setCurOptions] = useState<Options>({});
  const [curUrl, setCurUrl] = useState<ApiRoutes>(url);

  const fetch = (fetchUrl: ApiRoutes, opts: Options) => {
    setLoading(true);
    const method = opts.method ? opts.method : "get";
    axios[method](fetchUrl, {
      data: opts.body,
      params: opts.params,
    })
      .then((res) => {
        setData(res.data);
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  if (url !== curUrl || !isEqual(options, curOptions)) {
    setCurUrl(url);
    setCurOptions(options);
    fetch(url, options);
  }

  const refetch = () => fetch(curUrl, curOptions);

  return { data, error, loading, refetch };
}
