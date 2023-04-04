<script lang="ts">
import { handleApi, parseDatetime, type INews } from "@/utilities";
import { Modal } from "bootstrap";

export default {
  props: {
    newsData: {
      type: Array as () => INews[],
      required: true,
    },
    userSignedIn: {
      type: Boolean,
      required: true,
    },
    newsTotalPage: {
      type: Number,
      required: false,
    },
    newsPageCurrent: {
      type: Number,
      required: false,
    },
    newsFirstPage: {
      type: Number,
      required: false,
    },
    newsLastPage: {
      type: Number,
      required: false,
    },
  },
  data: () => {
    return {
      liking: false,
      modalLikingObj: {} as Modal,
    };
  },
  methods: {
    parseDatetime,
    onLikeClick(item: any) {
      item.liked = !item.liked;
      const apiData = {
        requestType: "like",
        newsId: item.id,
        liked: item.liked,
      };
      this.liking = true;
      handleApi("post", "/api/news/setnewsuseraction", apiData).then(() => {
        this.liking = false;
      });
    },
    onCollectClick(item: any) {
      item.collected = !item.collected;
      const apiData = {
        requestType: "collect",
        newsId: item.id,
        collected: item.collected,
      };
      handleApi("post", "/api/news/setnewsuseraction", apiData);
    },
    onNewsSwitchPage(page: number) {
      this.$emit("newsSwitchToPage", page);
    },
  },
  mounted() {
    this.modalLikingObj = new Modal(this.$refs.modalLiking as HTMLElement);
  },
  watch: {
    liking: function (newVal) {
      if (newVal) {
        this.modalLikingObj.show();
      } else {
        this.modalLikingObj.hide();
      }
    },
  },
};
</script>
<template>
  <div>
    <ul class="list-group">
      <li
        class="list-group-item"
        v-for="(news, index) in newsData"
        :key="index"
      >
        <div class="card container p-2 border-0 m-0" style="box-shadow: none">
          <div class="row">
            <div class="col-12 col-lg-3">
              <img
                :src="news.cover_image.url"
                class="img-thumbnail border-0"
                style="height: auto; width: 100%"
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
                  parseDatetime(news.article.datetime as string)
                }}</span>
              </span>
              <div class="mb-1">
                <span class="text-muted" style="font-size: 0.9em"
                  >Tickers:</span
                >
                <ul class="list-group list-group-horizontal flex-wrap">
                  <li
                    class="list-group-item border-0 p-0 me-2"
                    v-for="(ticker, index) of news.tickers"
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
              <div class="mb-1">
                <span class="text-muted" style="font-size: 0.9em"
                  >Industries:</span
                >
                <ul class="list-group list-group-horizontal flex-wrap">
                  <li
                    class="list-group-item border-0 p-0 me-2"
                    v-for="(category, index) of news.categories"
                    :key="index"
                  >
                    <RouterLink :to="'/category?q=' + category" target="_blank">
                      <span
                        class="badge rounded-pill text-bg-secondary stocknews-category"
                        >{{ category }}</span
                      >
                    </RouterLink>
                  </li>
                </ul>
              </div>
              <div v-if="userSignedIn">
                <div>
                  <div class="d-inline me-1">
                    <a href="#" @click="onLikeClick(news)">
                      <img
                        v-show="news.liked === true"
                        src="/src/assets/icon/like.png"
                        alt="Unlike"
                        style="height: 2em"
                        title="Unlike"
                      />
                      <img
                        v-show="news.liked !== true"
                        src="/src/assets/icon/no_like.png"
                        alt="Like"
                        style="height: 2em"
                        title="Like"
                      />
                    </a>
                  </div>
                  <div class="d-inline">
                    <a href="#" @click="onCollectClick(news)">
                      <img
                        v-show="news.collected === true"
                        src="/src/assets/icon/collect.png"
                        alt="Uncollect"
                        style="height: 2em"
                        title="Uncollect"
                      />
                      <img
                        v-show="news.collected !== true"
                        src="/src/assets/icon/no_collect.png"
                        alt="Collect"
                        style="height: 2em"
                        title="Collect"
                      />
                    </a>
                  </div>
                </div>
                <div
                  v-if="
                    news.collect_datetime !== undefined &&
                    news.collect_datetime !== null &&
                    news.collect_datetime !== ''
                  "
                  class="mt-1"
                >
                  Collect time:&nbsp;<span>{{
                    parseDatetime(news.collect_datetime as string)
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </li>
    </ul>
    <nav
      v-if="
        newsPageCurrent !== undefined &&
        newsFirstPage !== undefined &&
        newsLastPage !== undefined &&
        newsTotalPage !== undefined &&
        newsTotalPage > 1
      "
      class="user-select-none my-3"
      aria-label="Page navigation"
    >
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: newsPageCurrent === 1 }">
          <a
            class="page-link"
            href="#"
            @click="onNewsSwitchPage(newsPageCurrent! - 1)"
            >Previous</a
          >
        </li>
        <li v-if="newsFirstPage !== 1" class="page-item">
          <a class="page-link" href="#" @click="onNewsSwitchPage(1)">1</a>
        </li>
        <li v-if="newsFirstPage !== 1" class="page-item disabled">
          <a class="page-link">...</a>
        </li>
        <li
          v-for="i in newsLastPage - newsFirstPage + 1"
          :key="i"
          class="page-item"
          :class="{
            active: i + newsFirstPage - 1 === newsPageCurrent,
          }"
        >
          <a
            class="page-link"
            href="#"
            @click="onNewsSwitchPage(i + newsFirstPage! - 1)"
            >{{ i + newsFirstPage - 1 }}</a
          >
        </li>
        <li v-if="newsLastPage !== newsTotalPage" class="page-item disabled">
          <a class="page-link">...</a>
        </li>
        <li v-if="newsLastPage !== newsTotalPage" class="page-item">
          <a
            class="page-link"
            href="#"
            @click="onNewsSwitchPage(newsTotalPage!)"
            >{{ newsTotalPage }}</a
          >
        </li>
        <li
          class="page-item"
          :class="{ disabled: newsPageCurrent === newsTotalPage }"
        >
          <a
            class="page-link"
            href="#"
            @click="onNewsSwitchPage(newsPageCurrent! + 1)"
            >Next</a
          >
        </li>
      </ul>
    </nav>
    <div
      class="modal fade"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
      aria-labelledby="modalLikingLabel"
      aria-hidden="true"
      ref="modalLiking"
    >
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="modalLikingLabel">Info</h1>
          </div>
          <div class="modal-body">
            Liking/Unliking the news, please wait some time...
          </div>
        </div>
      </div>
    </div>
  </div>
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
  text-align: justify;
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

.stocknews-ticker,
.stocknews-category {
  font-size: 0.7em;
  font-weight: 400;
}
</style>
