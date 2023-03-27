<script lang="ts">
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, type ITicker, type INews } from "@/utilities";
import * as echarts from "echarts";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

export default {
  data() {
    return {
      tickerInfo: null as ITicker | null,
      news_list: [] as INews[],
      stockPriceResizeObserver: null as null | ResizeObserver,
      pageLoading: true,
      newsLoading: true,
      newsPageCurrent: 1,
      newsTotalCount: 0,
      newsError: false,
    };
  },
  computed: {
    newsTotalPage() {
      return Math.ceil(this.newsTotalCount / 10);
    },
    newsFirstPage() {
      return Math.max(1, this.newsPageCurrent - 2);
    },
    newsLastPage() {
      return Math.min(this.newsTotalPage, this.newsPageCurrent + 2);
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
          this.onNewsSwitchToPage(1);
        }
      },
      immediate: true,
    },
  },
  methods: {
    onGetTickerInfo(callback: Function | undefined = undefined) {
      const apiData = {
        ticker: this.$route.query.q,
      };
      handleApi("post", "/api/stock/gettickerinfo", apiData).then(
        (response) => {
          const code = parseInt(response.data.code);
          const data = response.data.data;
          if (code === 200) {
            this.tickerInfo = data;
            if (callback !== undefined) {
              callback();
            }
          }
        }
      );
    },
    onGetPrice(callback: Function | undefined = undefined) {
      // TODO: change to real trading date.
      // const endDate = new Date();
      // const startDate = new Date(endDate.getTime() - 24 * 60 * 60 * 1000);
      handleApi("post", "/api/stock/getprice", {
        ticker: this.$route.query.q,
        start_date: "2023-03-17",
        end_date: "2023-03-17",
        // start_date: Math.round(startDate.getTime() / 1000),
        // end_date: Math.round(endDate.getTime() / 1000),
      }).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code === 200) {
          this.drawPriceChartAdvanced(data.price);
          if (callback !== undefined) {
            callback();
          }
        }
      });
    },
    onGetTickerNews(callback: Function | undefined = undefined) {
      const apiData = {
        ticker: this.$route.query.q,
        page: this.newsPageCurrent,
      };
      handleApi("post", "/api/news/getnewsbyticker", apiData).then(
        (response) => {
          const code = parseInt(response.data.code);
          const data = response.data.data;
          if (code === 200) {
            this.news_list = data.news_list;
            if (data.total_count !== undefined) {
              this.newsTotalCount = data.total_count;
            }
            if (callback !== undefined) {
              callback();
            }
          } else {
            this.newsError = true;
          }
        }
      );
    },
    onNewsSwitchToPage(page: number) {
      this.newsError = false;
      this.newsPageCurrent = page;
      this.newsLoading = true;
      this.onGetTickerNews(() => {
        this.newsLoading = false;
      });
    },
    drawPriceChartAdvanced(
      data: {
        timestamp: number;
        open: number;
        close: number;
        low: number;
        high: number;
      }[]
    ) {
      const chartObj = echarts.init(
        this.$refs.chart_stockprice_advanced as HTMLDivElement
      );
      this.stockPriceResizeObserver = new ResizeObserver(() =>
        chartObj.resize()
      );
      this.stockPriceResizeObserver.observe(
        this.$refs.chart_stockprice_advanced as Element
      );
      const chartOption: echarts.EChartsOption = {
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
          axisLabel: {
            margin: 20,
          },
          name: this.tickerInfo?.currency_name,
          nameTextStyle: {
            padding: [0, 60, 0, 0],
            align: "center",
          },
        },
        series: {
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
        },
      };
      chartObj.setOption(chartOption);
    },
  },
  created() {
    document.title = "Ticker - " + (this as any).$projectName;
  },
  mounted() {
    this.onGetTickerInfo(() => {
      this.onGetPrice(() => {
        this.pageLoading = false;
      });
    });
  },
  beforeUnmount() {
    this.stockPriceResizeObserver?.unobserve(
      this.$refs.chart_stockprice_advanced as Element
    );
  },
  components: {
    NewsContainer,
    FontAwesomeIcon,
  },
};
</script>
<template>
  <div style="max-height: 100%; overflow: auto">
    <div
      v-if="pageLoading"
      class="w-100 h-100 d-flex justify-content-center align-items-center"
    >
      <div
        role="status"
        class="spinner-border text-primary"
        style="width: 3rem; height: 3rem"
      >
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
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
                    <tr v-if="tickerInfo.total_employees !== undefined">
                      <td>Total Employees</td>
                      <td>{{ tickerInfo.total_employees }}</td>
                    </tr>
                    <tr v-if="tickerInfo.currency_name !== undefined">
                      <td>Currency</td>
                      <td>{{ tickerInfo.currency_name }}</td>
                    </tr>
                    <tr v-if="tickerInfo.list_date !== undefined">
                      <td>List Date</td>
                      <td>{{ tickerInfo.list_date }}</td>
                    </tr>
                    <tr v-if="tickerInfo.market_cap !== undefined">
                      <td>Market Cap</td>
                      <td>{{ tickerInfo.market_cap }}</td>
                    </tr>
                    <tr v-if="tickerInfo.primary_exchange !== undefined">
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
            <div class="card-header"><h5>Price</h5></div>
            <div class="card-body">
              <div class="card-text">
                <div
                  style="width: 100%; min-height: 30rem"
                  ref="chart_stockprice_advanced"
                ></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5>Latest News</h5>
            </div>
            <div class="card-body">
              <div class="card-text">
                <div
                  v-if="newsLoading"
                  class="d-flex align-items-center justify-content-center gap-2 my-2"
                >
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  Loading news...
                </div>
                <div v-show="!newsLoading">
                  <NewsContainer
                    :newsData="news_list"
                    :newsTotalPage="newsTotalPage"
                    :newsTotalCount="newsTotalCount"
                    :newsPageCurrent="newsPageCurrent"
                    :newsFirstPage="newsFirstPage"
                    :newsLastPage="newsLastPage"
                    :newsLoading="newsLoading"
                    :newsError="newsError"
                    @newsSwitchToPage="onNewsSwitchToPage"
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
.card {
  border: none;
  box-shadow: 0 7px 14px 0 rgba(65, 69, 88, 0.1),
    0 3px 6px 0 rgba(0, 0, 0, 0.07);
}

.card .card-header {
  border: none;
  background-color: rgb(249, 250, 253);
}

.card .card-header *,
.card .card-title * {
  margin-bottom: 0;
}

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
