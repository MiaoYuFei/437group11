<script lang="ts">
import LoadingIndicator from "@/components/LoadingIndicator.vue";
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, type INews } from "@/utilities";

enum NewsSource {
  Recommendation,
  Collection,
}

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
      newsSource: NewsSource.Recommendation,
    };
  },
  computed: {
    NewsSource() {
      return NewsSource;
    },
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
        requestType:
          this.newsSource === NewsSource.Collection
            ? "collection"
            : "recommendation",
        page: this.newsPageCurrent,
      };
      handleApi("post", "/api/news/getnews", apiData).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code == 200) {
          this.newsList = data.newsList;
          if (data.totalCount !== undefined) {
            this.newsTotalCount = data.totalCount;
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
    onCheckPreferencesSet(callback: Function | undefined = undefined) {
      handleApi("post", "/api/user/checkpreferencesset", {}).then(
        (response) => {
          const code = parseInt(response.data.code);
          if (code == 200) {
            if (callback !== undefined) {
              callback(true);
            }
          } else {
            if (callback !== undefined) {
              callback(false);
            }
          }
        }
      );
    },
    onSwitchNewsPage(page: number) {
      this.newsError = false;
      this.newsPageCurrent = page;
      this.newsLoading = true;
      this.onGetNews(() => {
        this.newsLoading = false;
      });
    },
    onSwitchNewsSource(newsSource: NewsSource) {
      this.newsSource = newsSource;
      if (newsSource === NewsSource.Recommendation) {
        this.$router.push({ query: { source: "recommendations" } });
      } else if (newsSource === NewsSource.Collection) {
        this.$router.push({ query: { source: "mycollections" } });
      }
    },
  },
  watch: {
    $route: {
      handler: function (to: any, from: any) {
        if (
          to.query.source === undefined ||
          to.query.source === null ||
          to.query.source === ""
        ) {
          this.$router.replace({ query: { source: "recommendations" } });
          return;
        }
        if (from !== undefined && to.query.source === from.query.source) {
          return;
        }
        this.onCheckPreferencesSet((result: boolean) => {
          if (!result) {
            this.$router.push("/myaccount?showSetPreferences=true#preferences");
            return;
          } else {
            if (to.query.source === "recommendations") {
              this.newsSource = NewsSource.Recommendation;
            } else if (to.query.source === "mycollections") {
              this.newsSource = NewsSource.Collection;
            }
          }
        });
      },
      immediate: true,
    },
    newsSource: {
      handler: function (to: NewsSource, from: NewsSource) {
        if (to === from) {
          return;
        }
        this.onSwitchNewsPage(1);
      },
      immediate: true,
    },
  },
  created() {
    document.title = "My Reading List - " + (this as any).$projectName;
  },
  components: {
    LoadingIndicator,
    NewsContainer,
  },
};
</script>
<template>
  <div style="overflow: auto">
    <LoadingIndicator :loading="newsLoading" message="Loading news..." />
    <div v-show="!newsLoading" class="container my-3">
      <div
        class="d-block btn-group mb-3"
        role="group"
        aria-label="Toggle news source between recommendations and my collections"
      >
        <input
          type="radio"
          class="btn-check"
          name="btnNewsSource"
          id="btnRecommendations"
          value="recommendations"
          autocomplete="off"
          :checked="newsSource === NewsSource.Recommendation"
          @click="onSwitchNewsSource(NewsSource.Recommendation)"
        />
        <label class="btn btn-outline-primary" for="btnRecommendations"
          >Recommendations</label
        >
        <input
          type="radio"
          class="btn-check"
          name="btnNewsSource"
          id="btnMyCollections"
          value="mycollections"
          autocomplete="off"
          :checked="newsSource === NewsSource.Collection"
          @click="onSwitchNewsSource(NewsSource.Collection)"
        />
        <label class="btn btn-outline-primary" for="btnMyCollections"
          >My Collections</label
        >
      </div>
      <div v-if="newsError" class="card">
        <div class="card-header"><h5>Error</h5></div>
        <div class="card-body">
          <p class="card-text" style="text-align: justify">
            {{ newsErrorMessage }}
          </p>
        </div>
      </div>
      <div v-show="!newsLoading">
        <NewsContainer
          :newsData="newsList"
          :newsTotalPage="newsTotalPage"
          :newsPageCurrent="newsPageCurrent"
          :newsFirstPage="newsFirstPage"
          :newsLastPage="newsLastPage"
          :userSignedIn="userStatus.signedIn"
          @newsSwitchToPage="onSwitchNewsPage"
        />
        <div
          v-if="newsList.length === 0 && newsSource === NewsSource.Collection"
          class="card"
        >
          <div class="card-header"><h5>Error</h5></div>
          <div class="card-body">
            <p class="card-text" style="text-align: justify">
              You don&apos;t have any collections.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
