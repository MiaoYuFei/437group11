<script lang="ts">
import LoadingIndicator from "@/components/LoadingIndicator.vue";
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, type ITicker, type INews } from "@/utilities";
import $ from "jquery";
import * as echarts from "echarts";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { shallowRef } from "vue";

enum ChartType {
  Basic,
  Advanced,
}

enum ChartTimeSpan {
  OneDay,
  OneMonth,
  ThreeMonths,
  OneYear,
}

export default {
  props: {
    userStatus: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      tickerInfo: null as ITicker | null,
      newsList: [] as INews[],
      pageLoading: true,
      newsLoading: true,
      newsPageCurrent: 1,
      newsTotalCount: 0,
      newsError: false,
      newsErrorMessage: "",
      priceData: [] as {
        timestamp: number;
        open: number;
        close: number;
        low: number;
        high: number;
      }[],
      priceChartObj: shallowRef<echarts.ECharts | null>(null),
      priceChartType: ChartType.Basic,
      priceChartTimeSpan: ChartTimeSpan.OneDay,
      priceEndDate: new Date().toISOString().split("T")[0],
      priceChartLoading: true,
    };
  },
  computed: {
    $() {
      return $;
    },
    ChartType() {
      return ChartType;
    },
    ChartTimeSpan() {
      return ChartTimeSpan;
    },
    ticker() {
      return this.$route.query.q;
    },
    newsTotalPage() {
      return Math.ceil(this.newsTotalCount / 10);
    },
    newsFirstPage() {
      return Math.max(1, this.newsPageCurrent - 2);
    },
    newsLastPage() {
      return Math.min(this.newsTotalPage, this.newsPageCurrent + 2);
    },
    priceStartDate() {
      const priceEndDateObj = new Date(this.priceEndDate + "T00:00:00Z");
      if (this.priceChartTimeSpan === ChartTimeSpan.OneDay) {
        return this.priceEndDate;
      } else if (this.priceChartTimeSpan === ChartTimeSpan.OneMonth) {
        priceEndDateObj.setUTCMonth(priceEndDateObj.getUTCMonth() - 1);
        return priceEndDateObj.toISOString().slice(0, 10);
      } else if (this.priceChartTimeSpan === ChartTimeSpan.ThreeMonths) {
        priceEndDateObj.setUTCMonth(priceEndDateObj.getUTCMonth() - 3);
        return priceEndDateObj.toISOString().slice(0, 10);
      } else if (this.priceChartTimeSpan === ChartTimeSpan.OneYear) {
        priceEndDateObj.setUTCFullYear(priceEndDateObj.getUTCFullYear() - 1);
        return priceEndDateObj.toISOString().slice(0, 10);
      } else {
        return new Date().toISOString().split("T")[0];
      }
    },
  },
  methods: {
    getPriceChartTimeSpanText(timeSpan: ChartTimeSpan) {
      if (timeSpan === ChartTimeSpan.OneDay) {
        return "Day View";
      } else if (timeSpan === ChartTimeSpan.OneMonth) {
        return "Month View";
      } else if (timeSpan === ChartTimeSpan.ThreeMonths) {
        return "3 Months View";
      } else if (timeSpan === ChartTimeSpan.OneYear) {
        return "1 Year View";
      } else {
        return "N/A";
      }
    },
    onGetTickerInfo(callback: Function | undefined = undefined) {
      const apiData = {
        ticker: this.ticker,
      };
      handleApi("post", "/api/stock/gettickerinfo", apiData).then(
        (response) => {
          const code = parseInt(response.data.code);
          const data = response.data.data;
          if (code === 200) {
            this.tickerInfo = data;
            this.priceEndDate = data.last_trading_date;
            if (callback !== undefined) {
              callback();
            }
          }
        }
      );
    },
    onGetPrice(callback: Function | undefined = undefined) {
      handleApi("post", "/api/stock/getprice", {
        ticker: this.ticker,
        start_date: this.priceStartDate,
        end_date: this.priceEndDate,
        mode: this.priceStartDate === this.priceEndDate ? "hour" : "day",
      }).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code === 200) {
          this.priceData = data.price;
          if (callback !== undefined) {
            callback();
          }
        }
      });
    },
    onGetNews(callback: Function | undefined = undefined) {
      const apiData = {
        requestType: "ticker",
        ticker: this.ticker,
        page: this.newsPageCurrent,
      };
      handleApi("post", "/api/news/getnews", apiData).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code === 200) {
          this.newsList = data.newsList;
          if (data.totalCount !== undefined) {
            this.newsTotalCount = data.totalCount;
          }
          if (callback !== undefined) {
            callback(true);
          }
        } else {
          this.newsError = true;
          this.newsErrorMessage = data.reason;
          if (callback !== undefined) {
            callback(false);
          }
        }
      });
    },
    onSwitchNewsPage(page: number) {
      this.newsError = false;
      this.newsPageCurrent = page;
      this.newsLoading = true;
      this.onGetNews(() => {
        this.newsLoading = false;
      });
    },
    onSwitchPriceChartType(chartType: ChartType) {
      this.priceChartType = chartType;
      if (chartType === ChartType.Basic) {
        this.drawPriceChart(ChartType.Basic, this.priceData);
      } else {
        this.drawPriceChart(ChartType.Advanced, this.priceData);
      }
    },
    onSwitchPriceChartTimeSpan(chartTimeSpan: ChartTimeSpan) {
      this.priceChartTimeSpan = chartTimeSpan;
      this.onGetPrice(() => {
        if (this.priceChartType === ChartType.Basic) {
          this.drawPriceChart(ChartType.Basic, this.priceData);
        } else {
          this.drawPriceChart(ChartType.Advanced, this.priceData);
        }
      });
    },
    drawPriceChart(
      chartType: ChartType,
      data: {
        timestamp: number;
        open: number;
        close: number;
        low: number;
        high: number;
      }[]
    ) {
      if (this.priceChartObj !== null) {
        this.priceChartObj.dispose();
      }
      this.priceChartObj = echarts.init(
        this.$refs.chart_stockprice as HTMLDivElement
      );
      const chartOption: echarts.EChartsOption = {
        title: {
          text:
            this.priceStartDate === this.priceEndDate
              ? `${this.tickerInfo?.ticker} Price Chart (${this.priceStartDate})`
              : `${this.tickerInfo?.ticker} Price Chart (${this.priceStartDate} - ${this.priceEndDate})`,
          textStyle: {
            fontWeight: "bold",
          },
          left: "center",
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
          },
        },
        xAxis: {
          type: "time",
          scale: true,
        },
        yAxis: {
          type: "value",
          scale: true,
          name: this.tickerInfo?.currency_name,
          nameTextStyle: {
            align: "center",
          },
        },
      };
      if (chartType === ChartType.Basic) {
        chartOption.series = {
          type: "line",
          data: data.map((item) => [item.timestamp, item.close]),
        };
      } else if (chartType === ChartType.Advanced) {
        chartOption.series = {
          type: "candlestick",
          data: data.map((item) => [
            item.timestamp,
            item.open,
            item.close,
            item.low,
            item.high,
          ]),
          itemStyle: {
            color: "green",
            color0: "red",
            borderColor: "green",
            borderColor0: "red",
          },
        };
      }
      this.priceChartObj.setOption(chartOption);
      $(window)
        .off("resize.echarts")
        .on("resize.echarts", () => {
          this.priceChartObj?.resize();
        });
    },
  },
  watch: {
    $route: {
      handler: function (to: any, from: any) {
        if (
          to.query !== undefined &&
          (from === undefined ||
            (from !== undefined &&
              from.query !== undefined &&
              to.query.q !== from.query.q))
        ) {
          this.onSwitchNewsPage(1);
        }
      },
      immediate: true,
    },
  },
  created() {
    document.title = "Ticker - " + (this as any).$projectName;
  },
  mounted() {
    this.onGetTickerInfo(() => {
      this.onGetPrice(() => {
        $(() => {
          this.drawPriceChart(ChartType.Basic, this.priceData);
        });
        this.priceChartLoading = false;
      });
      this.pageLoading = false;
    });
  },
  components: {
    LoadingIndicator,
    NewsContainer,
    FontAwesomeIcon,
  },
};
</script>
<template>
  <div style="max-height: 100%; overflow: auto">
    <LoadingIndicator
      :loading="pageLoading"
      message="Loading ticker details..."
    />
    <div v-show="!pageLoading" class="container">
      <div v-if="tickerInfo" class="my-3 row gap-3">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="card-title mb-3">
                <div class="d-flex align-items-center gap-2">
                  <img
                    v-if="
                      tickerInfo.branding.logo_url !== undefined &&
                      tickerInfo.branding.logo_url !== null
                    "
                    :src="tickerInfo.branding.logo_url"
                    alt="brand logo"
                    style="max-height: 3em; width: auto"
                  />
                  <h4>{{ tickerInfo.name }}</h4>
                </div>
              </div>
              <div class="card-text">
                <h6 class="text-muted">
                  {{
                    tickerInfo.ticker +
                    (tickerInfo.sic_description !== undefined &&
                    tickerInfo.sic_description !== null
                      ? ", " + tickerInfo.sic_description
                      : "")
                  }}
                </h6>
                <div>
                  <span
                    v-if="
                      tickerInfo.address.city !== undefined &&
                      tickerInfo.address.state !== undefined &&
                      tickerInfo.address.city !== null &&
                      tickerInfo.address.state !== null
                    "
                    class="text-muted"
                    >{{
                      tickerInfo.address.city + ", " + tickerInfo.address.state
                    }}</span
                  >
                </div>
                <div
                  v-if="
                    tickerInfo.homepage_url !== undefined &&
                    tickerInfo.homepage_url !== null
                  "
                >
                  <a
                    :href="tickerInfo.homepage_url"
                    target="_blank"
                    class="stocknews-link"
                    ><FontAwesomeIcon
                      icon="fa-link"
                      class="me-1"
                    ></FontAwesomeIcon
                    >Home Page</a
                  >
                </div>
                <div
                  v-if="
                    tickerInfo.phone_number !== undefined &&
                    tickerInfo.phone_number !== null
                  "
                >
                  <a
                    :href="
                      'tel:' + tickerInfo.phone_number.replace(/[^0-9]/g, '')
                    "
                    class="stocknews-link"
                  >
                    <FontAwesomeIcon
                      icon="fa-phone"
                      class="me-1"
                    ></FontAwesomeIcon>
                    {{ tickerInfo.phone_number }}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-12">
          <div class="card">
            <div class="card-header"><h5>Intro</h5></div>
            <div class="card-body">
              <p class="card-text" style="text-align: justify">
                {{ tickerInfo.description }}
              </p>
            </div>
          </div>
        </div>
        <div class="col-12">
          <div class="card">
            <div class="card-header"><h5>Info</h5></div>
            <div class="card-body">
              <div class="card-text">
                <table class="table table-striped">
                  <tbody>
                    <tr>
                      <td>Category</td>
                      <td>{{ tickerInfo.category }}</td>
                    </tr>
                    <tr
                      v-if="
                        tickerInfo.sic_code !== undefined &&
                        tickerInfo.sic_code !== null
                      "
                    >
                      <td>SIC Code</td>
                      <td>{{ tickerInfo.sic_code }}</td>
                    </tr>
                    <tr
                      v-if="
                        tickerInfo.total_employees !== undefined &&
                        tickerInfo.total_employees !== null
                      "
                    >
                      <td>Total Employees</td>
                      <td>{{ tickerInfo.total_employees }}</td>
                    </tr>
                    <tr v-if="tickerInfo.currency_name !== undefined">
                      <td>Currency</td>
                      <td>{{ tickerInfo.currency_name }}</td>
                    </tr>
                    <tr
                      v-if="
                        tickerInfo.list_date !== undefined &&
                        tickerInfo.list_date !== null
                      "
                    >
                      <td>List Date</td>
                      <td>{{ tickerInfo.list_date }}</td>
                    </tr>
                    <tr
                      v-if="
                        tickerInfo.market_cap !== undefined &&
                        tickerInfo.market_cap !== null
                      "
                    >
                      <td>Market Cap</td>
                      <td>
                        {{
                          (tickerInfo.currency_name !== undefined &&
                          tickerInfo.currency_name !== null
                            ? tickerInfo.currency_name + " "
                            : "") + tickerInfo.market_cap.toLocaleString()
                        }}
                      </td>
                    </tr>
                    <tr
                      v-if="
                        tickerInfo.primary_exchange !== undefined &&
                        tickerInfo.primary_exchange !== null
                      "
                    >
                      <td>Primary Exchange</td>
                      <td>{{ tickerInfo.primary_exchange }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        <div class="col-12">
          <div class="card">
            <div class="card-header"><h5>Price Chart</h5></div>
            <div class="card-body">
              <div v-if="priceChartLoading" class="card-text">
                <LoadingIndicator
                  :loading="true"
                  message="Loading ticker price..."
                />
              </div>
              <div v-if="!priceChartLoading" class="card-text">
                <div
                  class="btn-group me-2"
                  role="group"
                  aria-label="Basic radio toggle button group"
                >
                  <input
                    type="radio"
                    class="btn-check"
                    name="btnPriceChartType"
                    id="btnPriceChartBasic"
                    value="pricechartbasic"
                    autocomplete="off"
                    checked
                    @click="onSwitchPriceChartType(ChartType.Basic)"
                  />
                  <label
                    class="btn btn-outline-primary"
                    for="btnPriceChartBasic"
                    >Basic</label
                  >
                  <input
                    type="radio"
                    class="btn-check"
                    name="btnPriceChartType"
                    id="btnPriceChartAdvanced"
                    value="pricechartadvanced"
                    autocomplete="off"
                    @click="onSwitchPriceChartType(ChartType.Advanced)"
                  />
                  <label
                    class="btn btn-outline-primary"
                    for="btnPriceChartAdvanced"
                    >Advanced</label
                  >
                </div>
                <div class="btn-group" role="group">
                  <button
                    class="btn btn-primary dropdown-toggle"
                    type="button"
                    name="btnPriceChartTimeSpan"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    {{ getPriceChartTimeSpanText(priceChartTimeSpan) }}
                  </button>
                  <ul class="dropdown-menu">
                    <li>
                      <a
                        class="dropdown-item"
                        :class="{
                          active: priceChartTimeSpan === ChartTimeSpan.OneDay,
                        }"
                        @click="
                          onSwitchPriceChartTimeSpan(ChartTimeSpan.OneDay)
                        "
                        href="#"
                      >
                        {{ getPriceChartTimeSpanText(ChartTimeSpan.OneDay) }}</a
                      >
                    </li>
                    <li>
                      <a
                        class="dropdown-item"
                        :class="{
                          active: priceChartTimeSpan === ChartTimeSpan.OneMonth,
                        }"
                        @click="
                          onSwitchPriceChartTimeSpan(ChartTimeSpan.OneMonth)
                        "
                        href="#"
                        >{{
                          getPriceChartTimeSpanText(ChartTimeSpan.OneMonth)
                        }}</a
                      >
                    </li>
                    <li>
                      <a
                        class="dropdown-item"
                        :class="{
                          active:
                            priceChartTimeSpan === ChartTimeSpan.ThreeMonths,
                        }"
                        @click="
                          onSwitchPriceChartTimeSpan(ChartTimeSpan.ThreeMonths)
                        "
                        href="#"
                        >{{
                          getPriceChartTimeSpanText(ChartTimeSpan.ThreeMonths)
                        }}</a
                      >
                    </li>
                    <li>
                      <a
                        class="dropdown-item"
                        :class="{
                          active: priceChartTimeSpan === ChartTimeSpan.OneYear,
                        }"
                        @click="
                          onSwitchPriceChartTimeSpan(ChartTimeSpan.OneYear)
                        "
                        href="#"
                        >{{
                          getPriceChartTimeSpanText(ChartTimeSpan.OneYear)
                        }}</a
                      >
                    </li>
                  </ul>
                </div>
                <div
                  style="width: 100%; height: 30rem"
                  ref="chart_stockprice"
                ></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5>Related News</h5>
            </div>
            <div class="card-body">
              <div class="card-text">
                <LoadingIndicator
                  :loading="newsLoading"
                  message="Loading news..."
                />
                <div v-if="newsError" class="card">
                  <div class="card-header"><h5>Error</h5></div>
                  <div class="card-body">
                    <p class="card-text" style="text-align: justify">
                      Failed to get news. Please try again later. ({{
                        newsErrorMessage
                      }})
                    </p>
                  </div>
                </div>
                <div v-show="!newsLoading">
                  <NewsContainer
                    :newsData="newsList"
                    :newsTotalPage="newsTotalPage"
                    :newsTotalCount="newsTotalCount"
                    :newsPageCurrent="newsPageCurrent"
                    :newsFirstPage="newsFirstPage"
                    :newsLastPage="newsLastPage"
                    :userSignedIn="userStatus.signedIn"
                    @newsSwitchToPage="onSwitchNewsPage"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.stocknews-link {
  color: #0d0d0d;
  text-decoration: none;
  background-color: transparent;
}

.stocknews-link:hover {
  color: #0088c7;
  text-decoration: underline;
}

.stocknews-link:active {
  color: #0077b2;
  text-decoration: underline;
}
</style>
