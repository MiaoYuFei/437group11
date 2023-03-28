<script lang="ts">
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, type INews } from "@/utilities";

export default {
  data() {
    return {
      newsList: [] as INews[],
      newsLoading: true,
      newsNeedMore: true,
      newsPageCurrent: 1,
      newsError: false,
      newsErrorMessage: "",
    };
  },
  methods: {
    onGetLatestNews(callback: Function | undefined = undefined) {
      const apiData = {
        page: this.newsPageCurrent,
      };
      handleApi("post", "/api/news/getnewslatest", apiData).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        this.newsNeedMore = false;
        if (code === 200) {
          this.newsList = this.newsList.concat(data.news_list);
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
    onNewsInfinitScroll(page: number | undefined = undefined) {
      this.newsError = false;
      if (page !== undefined) {
        this.newsPageCurrent = page;
      } else {
        this.newsPageCurrent += 1;
      }
      this.newsLoading = true;
      this.onGetLatestNews(() => {
        this.newsLoading = false;
      });
    },
    onScroll(event: Event) {
      const scrollSoucre = event.target as HTMLElement;
      if (
        scrollSoucre.scrollTop + scrollSoucre.clientHeight >=
        0.9 * scrollSoucre.scrollHeight
      ) {
        if (!this.newsNeedMore) {
          this.newsNeedMore = true;
          this.onNewsInfinitScroll();
        }
      }
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
          this.onNewsInfinitScroll(1);
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
  <div class="overflow-auto" @scroll="onScroll">
    <div class="container my-3">
      <div v-if="newsError" class="card">
        <div class="card-header"><h5>Error</h5></div>
        <div class="card-body">
          <p class="card-text" style="text-align: justify">
            Failed to get news. Please try again later. ({{ newsErrorMessage }})
          </p>
        </div>
      </div>
      <div v-if="!newsError">
        <h4 class="mb-3">Home - Latest News</h4>
      </div>
      <NewsContainer
        :newsData="newsList"
        :newsPageCurrent="newsPageCurrent"
        :newsLoading="newsLoading"
        class="mb-3"
      />
      <div
        class="flex-fill justify-content-center align-items-center h-100"
        :class="{ 'd-flex': newsLoading, 'd-none': !newsLoading }"
      >
        <div
          class="spinner-border text-primary me-2"
          role="status"
          style="width: 3rem; height: 3rem"
        >
          <span class="visually-hidden">Loading...</span>
        </div>
        Loading news...
      </div>
    </div>
  </div>
</template>
