<script lang="ts">
import $ from "jquery";
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, type INews } from "@/utilities";

enum NewsSource {
  Recommendations,
  Collections,
}

export default {
  data() {
    return {
      news_list: [] as INews[],
      email: "",
      signedIn: false,
      emailVerified: false,
      newsLoading: true,
      newsPageCurrent: 1,
      newsTotalCount: 0,
      newsError: false,
      newsErrorMessage: "",
      newsSource: NewsSource.Recommendations,
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
    onGetUserStatus: function (callback: Function | undefined = undefined) {
      handleApi("post", "/api/user/status", []).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            this.email = response.data.data.email;
            this.signedIn = true;
            this.emailVerified =
              (response.data.data.emailVerified as string).toLowerCase() ===
              "true"
                ? true
                : false;
            if (!this.emailVerified) {
              this.$router.push("/verifyemail");
            } else {
              if (callback !== undefined) {
                callback();
              }
            }
          } else {
            this.signedIn = false;
            this.emailVerified = false;
            this.$router.push("/signin");
          }
        },
        () => {
          this.signedIn = false;
          this.emailVerified = false;
          this.$router.push("/signin");
        }
      );
    },
    onGetNews(callback: Function | undefined = undefined) {
      const apiData = {
        page: this.newsPageCurrent,
      };
      let apiEndpoint = "";
      if (this.newsSource === NewsSource.Collections) {
        apiEndpoint = "/api/news/getnewscollection";
      } else if (this.newsSource === NewsSource.Recommendations) {
        apiEndpoint = "/api/news/getnewsrecommendation";
      }
      apiEndpoint = "/api/news/getnewslatest"; // TODO: Remove this line after testing
      handleApi("post", apiEndpoint, apiData).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code == 200) {
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
      this.onGetNews(() => {
        this.newsLoading = false;
      });
    },
    onSetNewsSource() {
      const source = $("input[name='btnNewsSource']:checked").val() as string;
      if (source === "recommendations") {
        this.newsSource = NewsSource.Recommendations;
        window.location.hash = "#recommendations";
      } else if (source === "mycollections") {
        this.newsSource = NewsSource.Collections;
        window.location.hash = "#mycollections";
      }
    },
  },
  watch: {
    $route: {
      handler: function (to: any, from: any) {
        this.onGetUserStatus(() => {
          if (
            to.hash !== undefined &&
            (from === undefined ||
              (from !== undefined &&
                from.hash !== undefined &&
                to.hash !== from.hash))
          ) {
            if (to.hash === "#recommendations") {
              this.newsSource = NewsSource.Recommendations;
              this.onNewsSwitchToPage(1);
              $("#btnMyCollections").prop("checked", false);
              $("#btnRecommendations").prop("checked", true);
            } else if (to.hash === "#mycollections") {
              this.newsSource = NewsSource.Collections;
              this.onNewsSwitchToPage(1);
              $("#btnRecommendations").prop("checked", false);
              $("#btnMyCollections").prop("checked", true);
            }
          }
        });
      },
      immediate: true,
    },
  },
  created() {
    document.title = "My Reading List - " + (this as any).$projectName;
  },
  mounted() {
    if (
      window.location.hash === undefined ||
      window.location.hash === null ||
      window.location.hash === ""
    ) {
      window.location.hash = "#recommendations";
    }
  },
  components: {
    NewsContainer,
  },
};
</script>
<template>
  <div style="overflow: auto">
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
          checked
          @click="onSetNewsSource"
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
          @click="onSetNewsSource"
        />
        <label class="btn btn-outline-primary" for="btnMyCollections"
          >My Collections</label
        >
      </div>
      <div v-if="newsError" class="card">
        <div class="card-header"><h5>Error</h5></div>
        <div class="card-body">
          <p class="card-text" style="text-align: justify">
            Failed to get news. Please try again later. ({{ newsErrorMessage }})
          </p>
        </div>
      </div>
      <div v-show="!newsLoading">
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
  </div>
</template>
