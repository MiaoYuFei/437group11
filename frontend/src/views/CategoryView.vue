<script lang="ts">
import NewsContainer from "@/components/NewsContainer.vue";
import {
  handleApi,
  translate_sic_category_code_to_sic_category_name,
  type INews,
} from "@/utilities";

export default {
  props: {
    userStatus: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      newsList: [] as INews[],
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
    onSwitchNewsPage(page: number) {
      this.newsError = false;
      this.newsPageCurrent = page;
      this.newsLoading = true;
      this.onGetNews(() => {
        this.newsLoading = false;
      });
    },
    onGetNews(callback: Function | undefined = undefined) {
      const apiData = {
        requestType: "category",
        category: this.$route.query.q,
        page: this.newsPageCurrent,
      };
      handleApi("post", "/api/news/getnews", apiData).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code === 200) {
          this.newsList = data.newsList;
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
    translate_sic_category_code_to_sic_category_name,
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
    document.title = "Category - " + (this as any).$projectName;
  },
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
    <div v-show="!newsLoading" class="container my-3">
      <div v-if="newsError" class="card">
        <div class="card-header"><h5>Error</h5></div>
        <div class="card-body">
          <p class="card-text" style="text-align: justify">
            Failed to get news. Please try again later. ({{ newsErrorMessage }})
          </p>
        </div>
      </div>
      <div v-if="!newsError && newsList.length <= 0" class="card">
        <div class="card-header"><h5>Info</h5></div>
        <div class="card-body">
          <p class="card-text" style="text-align: justify">
            No news found for
            <strong>
              {{
                translate_sic_category_code_to_sic_category_name(
                  $route.query.q as string
                )
              }}</strong
            >
            .
          </p>
        </div>
      </div>
      <div v-if="!newsError && newsList.length > 0">
        <h4 class="mb-3">
          News for:
          <strong>
            {{
              translate_sic_category_code_to_sic_category_name(
                $route.query.q as string
              )
            }}</strong
          >
        </h4>
      </div>
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
</template>
