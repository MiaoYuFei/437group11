<script lang="ts">
import LoadingIndicator from "@/components/LoadingIndicator.vue";
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, type INews } from "@/utilities";

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
    onGetNews(callback: Function | undefined = undefined) {
      const apiData = {
        requestType: "search",
        q: this.$route.query.q,
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
            callback();
          }
        } else {
          this.newsError = true;
        }
      });
    },
    onSwitchNewsPage(page: number) {
      this.newsError = false;
      this.newsPageCurrent = page;
      this.newsLoading = true;
      this.onGetNews(() => {
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
          this.onSwitchNewsPage(1);
        }
      },
      immediate: true,
    },
  },
  created() {
    document.title = "Search - " + (this as any).$projectName;
  },
  components: {
    LoadingIndicator,
    NewsContainer,
  },
};
</script>
<template>
  <div class="overflow-auto">
    <LoadingIndicator :loading="newsLoading" message="Searching news..." />
    <div v-if="!newsLoading" class="container my-3">
      <div v-if="!newsError && newsList.length > 0">
        <h4 class="mb-3">
          Search results for <strong>{{ $route.query.q }}</strong
          >:
        </h4>
      </div>
      <span v-if="newsList.length <= 0">
        No news found for <strong>{{ $route.query.q }}</strong
        >.
      </span>
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
