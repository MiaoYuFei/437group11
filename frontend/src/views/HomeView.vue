<script lang="ts">
import NewsContainer from "@/components/NewsContainer.vue";
import { parseDatetime } from "@/utilities";

export default {
  data() {
    return {
      news_string:
        '[{"article": {"title": "Invest Like Warren Buffett, Not Carl Icahn", "description": "Warren Buffett and Carl Icahn are two of the most successful investors of the past century. But Buffett is a superior model for investors to follow because of his patient style and focus on finding great businesses.", "keywords": ["investing"], "datetime": "2017-04-10T00:24:00Z", "url": "https://www.fool.com/investing/2017/04/09/invest-like-warren-buffett-not-carl-icahn.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/435736/warren-buffett3_tmf.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["BRK.B", "IEP", "BRK.A", "AAPL", "NFLX"]}, \
        {"article": {"title": "NASDAQ Rebounds While Waiting for Big Tech Reports", "description": "NASDAQ Rebounds While Waiting for Big Tech Reports", "keywords": "", "datetime": "2020-07-31T14:15:00Z", "url": "https://www.zacks.com/registration/ultimatetrader/welcome/eoffer/30c3?adid=ZU_CONTENT_SYND&cid=CS-ZC-FT-zucommentary-26169"}, "cover_image": {"url": "https://staticx-tuner.zacks.com/woas/adv/services/images/charts/zu/ZU-SR-MSFT-gain-chart.png"}, "publisher": {"name": "Zacks Investment Research", "homepage": {"url": "https://www.zacks.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/zacks.png"}}, "tickers": ["JELD", "NXPI", "FB", "CINF", "NKE", "KEY", "ALGT", "TRST", "CME", "FB", "AAPL", "AMZN", "GOOG"]}, \
        {"article": {"title": "July Marks Four Straight Months of Gains", "description": "July Marks Four Straight Months of Gains", "keywords": "", "datetime": "2020-08-03T14:15:00Z", "url": "https://www.zacks.com/registration/ultimatetrader/welcome/eoffer/30c3?adid=ZU_CONTENT_SYND&cid=CS-ZC-FT-zucommentary-26191"}, "cover_image": {"url": "https://staticx-tuner.zacks.com/woas/adv/services/images/charts/zu/ZU-SR-GOOG-gain-chart.png"}, "publisher": {"name": "Zacks Investment Research", "homepage": {"url": "https://www.zacks.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/zacks.png"}}, "tickers": ["INTC", "MDC", "BTG", "PINS", "BNFT", "MXL", "FB", "AMZN", "AAPL", "GOOG", "SLP"]}]',
      news_list: [
        {
          id: String,
          article: {
            title: String,
            description: String,
            keywords: [String],
            datetime: String,
            url: String,
          },
          cover_image: {
            url: String,
          },
          publisher: {
            name: String,
            homepage: {
              url: String,
            },
            logo: {
              url: String,
            },
          },
          tickers: [String],
        },
      ],
    };
  },
  methods: {
    parseDatetime,
  },
  created() {
    document.title = "Home - " + (this as any).$projectName;
  },
  mounted() {
    this.news_list = JSON.parse(this.news_string);
  },
  components: {
    NewsContainer,
  },
};
</script>
<template>
  <div>
    <div class="container">
      <NewsContainer :newsData="news_list" />
    </div>
  </div>
</template>
