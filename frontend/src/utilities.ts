import $ from "jquery";
import qs from "qs";
import axios, { type AxiosResponse } from "axios";

function getFormData(form: any, fields: string[]): { [key: string]: string } {
  const data: { [key: string]: string } = {};
  const jqObj = $(form as Element);
  for (const field of fields) {
    data[field] = (
      jqObj.find("input[name=" + field + "]").val() as string
    ).trim();
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

function parseDatetime(datetimeString: string) {
  return new Date(datetimeString).toLocaleString([], {
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function translate_sic_category_code_to_sic_category_name(
  sic_category_code: string
): string {
  switch (sic_category_code) {
    case "agriculture":
      return "Agriculture, Forestry and Fishing";
    case "mining":
      return "Mining, Quarrying, and Oil and Gas Extraction";
    case "construction":
      return "Construction";
    case "manufacturing":
      return "Manufacturing";
    case "transportation":
      return "Transportation and Warehousing";
    case "wholesale":
      return "Wholesale Trade";
    case "retail":
      return "Retail Trade";
    case "finance":
      return "Finance and Insurance";
    case "services":
      return "Services";
    case "public_administration":
      return "Public Administration";
    default:
      return "N/A";
  }
}

export interface ITicker {
  active: boolean;
  address: {
    address1: string;
    city: string;
    postal_code: string;
    state: string;
  };
  branding: {
    icon_url: string;
    logo_url: string;
  };
  cik: string;
  composite_figi: string;
  currency_name: string;
  description: string;
  homepage_url: string;
  list_date: string;
  locale: string;
  market: string;
  market_cap: number;
  name: string;
  phone_number: string;
  primary_exchange: string;
  round_lot: number;
  share_class_figi: string;
  share_class_shares_outstanding: number;
  sic_code: string;
  sic_description: string;
  ticker: string;
  ticker_root: string;
  total_employees: number;
  type: string;
  weighted_shares_outstanding: number;
  category: string;
}

export interface INews {
  id: string;
  article: {
    title: string;
    description: string;
    datetime: string;
    url: string;
  };
  cover_image: {
    url: string;
  };
  publisher: {
    name: string;
    homepage: {
      url: string;
    };
    logo: {
      url: string;
    };
  };
  tickers: string[];
  categories: string[];
}

export {
  getFormData,
  handleApi,
  enableForm,
  disableForm,
  focusForm,
  parseDatetime,
  translate_sic_category_code_to_sic_category_name,
};
