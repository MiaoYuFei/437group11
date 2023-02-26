import $ from "jquery";
import axios, { type AxiosResponse } from "axios";

function handleApi(
  form: any,
  fields: string[],
  data: any | undefined = undefined
): Promise<AxiosResponse<any, any>> {
  const jqObj = $(form as Element);
  const method = jqObj.attr("method")?.toLowerCase() || "get";
  const action = jqObj.attr("action") as string;
  const apiDdata: { [key: string]: string } = data != undefined ? data : {};
  for (const field of fields) {
    apiDdata[field] = jqObj.find("input[name=" + field + "]").val() as string;
  }
  let api: Promise<AxiosResponse<any, any>>;
  if (method === "get") {
    const search =
      (action.substring(action.indexOf("/")).indexOf("?") < 0 ? "?" : "&") +
      $.param(apiDdata);
    api = axios.get(action + search);
  } else if (method === "post") {
    api = axios.post(action, apiDdata);
  } else {
    throw new Error("api method not supported: " + method);
  }
  return api;
}

function enableForm(form: any) {
  $(form as Element)
    .find("input, button")
    .removeClass("disabled")
    .removeAttr("disabled");
}

function disableForm(form: any) {
  $(form as Element)
    .find("input, button")
    .addClass("disabled")
    .attr("disabled", "disabled");
}

function focusForm(form: any) {
  $(form as Element)
    .find("input:first")
    .trigger("focus");
}

export { handleApi, enableForm, disableForm, focusForm };
