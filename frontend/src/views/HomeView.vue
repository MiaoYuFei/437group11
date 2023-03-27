<script lang="ts">
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, type INews } from "@/utilities";

export default {
  data() {
    return {
      news_list: [] as INews[],
      newsLoading: true,
      newsPageCurrent: 1,
      newsTotalCount: 0,
      newsError: false,
      newsErrorMessage: "",
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
  methods: {
    onGetTopNews(callback: Function | undefined = undefined) {
      const apiData = {
        page: this.newsPageCurrent,
      };
      handleApi("post", "/api/news/getnewslatest", apiData).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code === 200) {
          this.news_list = data.news_list;
          if (data.total_count !== undefined) {
            this.newsTotalCount = data.total_count;
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
    onNewsSwitchToPage(page: number) {
      this.newsError = false;
      this.newsPageCurrent = page;
      this.newsLoading = true;
      this.onGetTopNews(() => {
        this.newsLoading = false;
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
          this.onNewsSwitchToPage(1);
        }
      },
      immediate: true,
    },
  },
  created() {
    document.title = "Home - " + (this as any).$projectName;
  },
  mounted() {},
  components: {
    NewsContainer,
  },
};
</script>
<template>
  <div class="overflow-auto">
    <div
      class="flex-fill justify-content-center align-items-center h-100"
      :class="{ 'd-flex': newsLoading, 'd-none': !newsLoading }"
    >
      <div
        class="spinner-border text-primary"
        role="status"
        style="width: 4rem; height: 4rem"
      >
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-if="!newsLoading" class="container my-3">
      <div v-if="newsError" class="card">
        <div class="card-header"><h5>Error</h5></div>
        <div class="card-body">
          <p class="card-text" style="text-align: justify">
            Failed to get news. Please try again later. ({{ newsErrorMessage }})
          </p>
        </div>
      </div>
      <div v-if="!newsError && news_list.length > 0">
        <h4 class="mb-3">Home - Latest News</h4>
      </div>
      <NewsContainer
        :newsData="news_list"
        :newsTotalPage="newsTotalPage"
        :newsTotalCount="newsTotalCount"
        :newsPageCurrent="newsPageCurrent"
        :newsFirstPage="newsFirstPage"
        :newsLastPage="newsLastPage"
        :newsLoading="newsLoading"
        @newsSwitchToPage="onNewsSwitchToPage"
      />
    </div>
  </div>
</template>
