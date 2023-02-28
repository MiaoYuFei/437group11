import $ from "jquery";
import qs from "qs";
import axios, { type AxiosResponse } from "axios";

function getFormData(form: any, fields: string[]): { [key: string]: string } {
  const data: { [key: string]: string } = {};
  const jqObj = $(form as Element);
  for (const field of fields) {
    data[field] = jqObj.find("input[name=" + field + "]").val() as string;
  }
  return data;
}

function handleApi(
  method: string,
  action: string,
  data: any | undefined = undefined
): Promise<AxiosResponse<any, any>> {
  if (method === "get") {
    const search =
      (action.substring(action.indexOf("/")).indexOf("?") < 0 ? "?" : "&") +
      $.param(data);
    return axios({
      method: "get",
      url: action + search,
    });
  } else if (method === "post") {
    return axios({
      method: "post",
      url: action,
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      data: qs.stringify(data),
    });
  } else {
    throw new Error("api method not supported: " + method);
  }
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

export { getFormData, handleApi, enableForm, disableForm, focusForm };
