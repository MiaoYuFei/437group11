<script lang="ts">
import { RouterLink } from "vue-router";
export default {
  data() {
    return {
      news_string:
        '[{"id": "0", "article": {"title": "Invest Like Warren Buffett, Not Carl Icahn", "description": "Warren Buffett and Carl Icahn are two of the most successful investors of the past century. But Buffett is a superior model for investors to follow because of his patient style and focus on finding great businesses.", "keywords": ["investing"], "datetime": "2017-04-10T00:24:00Z", "url": "https://www.fool.com/investing/2017/04/09/invest-like-warren-buffett-not-carl-icahn.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/435736/warren-buffett3_tmf.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["BRK.B", "IEP", "BRK.A", "AAPL", "NFLX"]}, \
  {"id": "0", "article": {"title": "Stock Market Power Rankings", "description": "They\'re big, beautiful, and ranked from 1 to 50.", "keywords": ["investing"], "datetime": "2018-11-05T22:50:00Z", "url": "https://www.fool.com/investing/2018/11/05/stock-market-power-rankings.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/500252/bronze-bear-and-bull-figurines-bear-market-bull-market-stock-market.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["BRK.A", "AAPL", "T", "MSFT", "JPM", "PFE", "AMZN", "WMT", "MRK", "MCD", "UNP", "META", "SBUX", "NFLX", "COST", "DIS", "CMCSA", "V", "LLY", "VZ", "EBAY", "BAC", "KO", "BA", "WFC", "INTC", "CVX", "XOM", "BHP", "CSCO", "PEP", "MA", "PG", "CRM", "NVDA", "UNH", "HD", "MDT", "LOW", "ABT", "FOXA", "NKE", "TJX", "ADBE", "NOV", "GOOG", "BABA", "PYPL"]}, \
  {"id": "0", "article": {"title": "Stock Market Power Rankings: Last Call for Facebook", "description": "They\'re big, beautiful, and ranked from 1 to 50.", "keywords": ["investing"], "datetime": "2018-11-12T16:11:00Z", "url": "https://www.fool.com/investing/2018/11/12/stock-market-power-rankings-last-call-for-facebook.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/501475/top50bullbear.jpeg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["AAPL", "WMT", "MSFT", "AMZN", "KO", "DIS", "UNH", "META", "BRK.A", "TGT", "V", "GOOG", "JPM", "MRK", "MCD", "UNP", "NFLX", "COST", "CMCSA", "SBUX", "LLY", "VZ", "T", "BAC", "BA", "WFC", "INTC", "CVX", "XOM", "BHP", "CSCO", "PEP", "MA", "JNJ", "PFE", "PG", "CRM", "NVDA", "ORCL", "HD", "GPS", "MDT", "LOW", "ABT", "AMGN", "FOXA", "NKE", "TJX", "ADBE", "NOV", "BABA", "PYPL"]}]',
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
    parseDatetime(datetimeString: string) {
      return new Date(datetimeString).toLocaleString([], {
        year: "numeric",
        month: "numeric",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
  created() {
    document.title = "My Feeds - " + (this as any).$projectName;
  },
  mounted() {
    this.news_list = JSON.parse(this.news_string);
  },
  components: {
    RouterLink,
  },
};
</script>
<template>
  <div>
    <span class="fw-bold">Selected news for you:</span>
    <div class="container">
      <ul class="list-group">
        <li
          class="list-group-item"
          v-for="(news, index) in news_list"
          :key="index"
        >
          <div class="card d-flex flex-row container p-2 border-0">
            <div class="col-3 d-flex justify-content-center">
              <img
                :src="news.cover_image.url"
                class="w-100"
                style="height: fit-content"
                alt="cover image"
              />
            </div>
            <div class="card-body py-0 col-9">
              <a
                class="text-decoration-none fw-bold"
                :href="news.article.url"
                target="_blank"
              >
                <h5 class="card-title stocknews-article-title">
                  <strong>{{ news.article.title }}</strong>
                </h5>
              </a>
              <p class="card-text stocknews-article-description">
                {{ news.article.description }}
              </p>
              <span
                class="d-flex align-items-center stocknews-article-publisher"
              >
                <div
                  class="d-flex gap-1 align-items-center pe-2"
                  style="border-right: 1px solid rgb(var(--bs-dark-rgb))"
                >
                  <span>From</span>
                  <img :src="news.publisher.logo.url" alt="publisher logo" />
                  <a
                    class="fst-italic"
                    :href="news.publisher.homepage.url"
                    target="_blank"
                  >
                    {{ news.publisher.name }}</a
                  >
                </div>
                <span class="ps-2">{{
                  parseDatetime(news.article.datetime as unknown as string)
                }}</span>
              </span>
              <div>
                <ul class="list-group list-group-horizontal">
                  <li
                    class="list-group-item border-0 p-0 me-2"
                    v-for="(ticker, index) of news.tickers.slice(0, 5)"
                    :key="index"
                  >
                    <RouterLink :to="'/ticker?q=' + ticker" target="_blank">
                      <span
                        class="badge rounded-pill text-bg-secondary stocknews-ticker"
                        >{{ ticker }}</span
                      >
                    </RouterLink>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
<style scoped>
@import url("https://fonts.googleapis.com/css?family=Newsreader");

.stocknews-article-title {
  font-size: 1.4em;
  font-optical-sizing: auto;
  font-family: "Newsreader rev=1";
  font-weight: 500;
  font-style: normal;
  font-stretch: normal;
  line-height: initial;
  font-variation-settings: "opsz" 48;
  text-decoration: none;
  color: rgb(var(--bs-dark-rgb));
}

.stocknews-article-title:hover {
  color: #1e90ff;
}

.stocknews-article-title:active {
  color: #4682b4;
}

.stocknews-article-description {
  font-optical-sizing: auto;
  font-family: "Newsreader rev=1";
  font-weight: 300;
  font-style: normal;
  font-stretch: normal;
  line-height: initial;
  font-variation-settings: "opsz" 48;
  color: rgb(var(--bs-dark-rgb));
}

.stocknews-article-publisher {
  font-size: 0.85em;
  font-optical-sizing: auto;
  font-family: "Newsreader rev=1";
  font-weight: 200;
  font-style: normal;
  font-stretch: normal;
  line-height: initial;
  font-variation-settings: "opsz" 48;
}

.stocknews-article-publisher a {
  text-decoration: none;
  color: rgb(var(--bs-dark-rgb));
}

.stocknews-article-publisher a:hover {
  text-decoration: underline rgb(var(--bs-dark-rgb));
}

.stocknews-article-publisher img {
  height: 1em;
  width: auto;
}

.stocknews-ticker {
  font-size: 0.7em;
  font-weight: 400;
}
</style>
