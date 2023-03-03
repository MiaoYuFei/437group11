<script lang="ts">
import { parseDatetime } from "@/utilities";
import $ from "jquery";

let domObj: Element | null = null;

export default {
  props: {
    newsData: Object,
  },
  methods: {
    parseDatetime,
  },
  mounted: function () {
    domObj = this.$refs.root as Element;
    const jqObj = $(domObj);
  },
};
</script>
<template>
  <ul class="list-group">
    <li class="list-group-item" v-for="(news, index) in newsData" :key="index">
      <div class="card container p-2 border-0">
        <div class="row">
          <div class="col-12 col-lg-3">
            <img
              :src="news.cover_image.url"
              class="img-thumbnail border-0"
              style="height: fit-content"
              alt="cover image"
            />
          </div>
          <div class="card-body py-0 col-12 col-lg-9">
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
            <span class="d-flex align-items-center stocknews-article-publisher">
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
              <ul class="list-group list-group-horizontal flex-wrap">
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
      </div>
    </li>
  </ul>
</template>
<style scoped>
@import url("https://fonts.googleapis.com/css?family=Newsreader");

.stocknews-article-title {
  font-size: 1.6em;
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
  font-size: 1.2em;
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
