<script lang="ts">
import * as echarts from "echarts";
import { handleApi } from "@/utilities";

export default {
  data() {
    return {};
  },
  methods: {
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
        grid: {
          left: "10%",
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
};
</script>
<template>
  <div>
    <div class="container">
      Ticker information for {{ $route.query.q }}:
      <div style="width: 40rem; height: 30rem" ref="chart_stockprice"></div>
    </div>
  </div>
</template>
<style scoped></style>
