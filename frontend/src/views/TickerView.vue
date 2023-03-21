<script lang="ts">
import * as echarts from "echarts";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { handleApi } from "@/utilities";

export default {
  data() {
    return {
      tickerInfo: {
        active: false,
        address: {
          address1: "",
          city: "",
          postal_code: "",
          state: "",
        },
        branding: {
          icon_url: "",
          logo_url: "",
        },
        cik: "",
        composite_figi: "",
        currency_name: "",
        description: "",
        homepage_url: "",
        list_date: "",
        locale: "",
        market: "",
        market_cap: 0,
        name: "",
        phone_number: "",
        primary_exchange: "",
        round_lot: 0,
        share_class_figi: "",
        share_class_shares_outstanding: 0,
        sic_code: "",
        sic_description: "",
        ticker: "",
        ticker_root: "",
        total_employees: 0,
        type: "",
        weighted_shares_outstanding: 0,
      },
    };
  },
  methods: {
    onGetTickerInfo() {
      const apiData = {
        ticker: this.$route.query.q,
      };
      handleApi("post", "/api/stock/gettickerinfo", apiData).then(
        (response) => {
          const code = parseInt(response.data.code);
          const data = response.data.data;
          if (code === 200) {
            this.tickerInfo = data;
          }
        }
      );
    },
    drawPriceChart(
      data: {
        timestamp: number;
        open: number;
        close: number;
        low: number;
        high: number;
      }[]
    ) {
      const chartObj = echarts.init(
        this.$refs.chart_stockprice as HTMLDivElement
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
    this.onGetTickerInfo();
    const endDate = new Date();
    const startDate = new Date(endDate.getTime() - 24 * 60 * 60 * 1000);
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
        this.drawPriceChart(data.price);
      }
    });
  },
  components: {
    FontAwesomeIcon,
  },
};
</script>
<template>
  <div style="max-height: 100%; overflow: auto">
    <div class="container">
      <div class="my-3 row gap-3">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="card-title mb-3">
                <div class="d-flex align-items-center gap-2">
                  <img
                    v-if="tickerInfo.branding.logo_url !== undefined"
                    :src="tickerInfo.branding.logo_url"
                    alt="brand logo"
                    style="height: 3em; width: auto"
                  />
                  <h4>{{ tickerInfo.name }}</h4>
                </div>
              </div>
              <div class="card-text">
                <h6 class="text-muted">
                  {{ $route.query.q + ", " + tickerInfo.sic_description }}
                </h6>
                <div>
                  <span
                    v-if="
                      tickerInfo.address.city !== undefined &&
                      tickerInfo.address.state !== undefined
                    "
                    class="text-muted"
                    >{{
                      tickerInfo.address.city + ", " + tickerInfo.address.state
                    }}</span
                  >
                </div>
                <div v-if="tickerInfo.homepage_url !== undefined">
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
                <div v-if="tickerInfo.phone_number !== undefined">
                  <FontAwesomeIcon
                    icon="fa-phone"
                    class="me-1"
                  ></FontAwesomeIcon>
                  {{ tickerInfo.phone_number }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-12">
          <div class="card">
            <div class="card-header"><h5>Intro</h5></div>
            <div class="card-body">
              <p class="card-text">{{ tickerInfo.description }}</p>
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
                    <tr v-if="tickerInfo.sic_code !== undefined">
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
                  style="width: 40rem; height: 30rem"
                  ref="chart_stockprice"
                ></div>
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
