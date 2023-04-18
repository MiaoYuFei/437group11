<script lang="ts">
import LoadingIndicator from "@/components/LoadingIndicator.vue";
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, type IPublisher, type INews } from "@/utilities";
import $ from "jquery";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

export default {
  props: {
    userStatus: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      publisherInfo: null as IPublisher | null,
      newsList: [] as INews[],
      pageLoading: true,
      newsLoading: true,
      newsPageCurrent: 1,
      newsTotalCount: 0,
      publisherError: false,
      publisherErrorMessage: "",
      newsError: false,
      newsErrorMessage: "",
    };
  },
  computed: {
    $() {
      return $;
    },
    publisher() {
      return this.$route.query.q;
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
    onGetPublisherInfo(callback: Function | undefined = undefined) {
      const apiData = {
        publisher: this.publisher,
      };
      handleApi("post", "/api/news/getpublisherinfo", apiData).then(
        (response) => {
          const code = parseInt(response.data.code);
          const data = response.data.data;
          if (code === 200) {
            this.publisherInfo = data;
            if (callback !== undefined) {
              callback(true);
            }
          } else {
            this.publisherError = true;
            this.publisherErrorMessage = data.reason;
            if (callback !== undefined) {
              callback(false);
            }
          }
        }
      );
    },
    onGetNews(callback: Function | undefined = undefined) {
      const apiData = {
        requestType: "publisher",
        publisher: this.publisher,
        page: this.newsPageCurrent,
      };
      handleApi("post", "/api/news/getnews", apiData).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code === 200) {
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
    onSwitchNewsPage(page: number) {
      this.newsError = false;
      this.newsPageCurrent = page;
      this.newsLoading = true;
      this.onGetNews(() => {
        this.newsLoading = false;
      });
    },
  },
  created() {
    document.title = "Publisher - " + (this as any).$projectName;
  },
  mounted() {
    this.onGetPublisherInfo((result: boolean) => {
      this.pageLoading = false;
      if (result) {
        this.onSwitchNewsPage(1);
      }
    });
  },
  components: {
    LoadingIndicator,
    NewsContainer,
    FontAwesomeIcon,
  },
};
</script>
<template>
  <div style="max-height: 100%; overflow: auto">
    <LoadingIndicator
      :loading="pageLoading"
      message="Loading publisher details..."
    />
    <div v-show="!pageLoading" class="container">
      <div v-if="publisherError" class="card my-3">
        <div class="card-header"><h5>Error</h5></div>
        <div class="card-body">
          <p class="card-text" style="text-align: justify">
            {{ publisherErrorMessage }}
          </p>
        </div>
      </div>
      <div v-if="publisherInfo" class="my-3 row gap-3">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <div class="my-2">
                <img
                  v-if="
                    publisherInfo.logo_url !== undefined &&
                    publisherInfo.logo_url !== null
                  "
                  :src="publisherInfo.logo_url"
                  alt="brand logo"
                  style="
                    max-height: 3em;
                    width: auto;
                    filter: drop-shadow(0.1em 0.1em 0.2em rgba(0, 0, 0, 0.4));
                  "
                />
              </div>
            </div>
            <div class="card-body">
              <div class="card-title">
                <h5>{{ publisherInfo.name }}</h5>
              </div>
              <div class="card-text">
                <div
                  v-if="
                    publisherInfo.homepage_url !== undefined &&
                    publisherInfo.homepage_url !== null
                  "
                >
                  <a
                    :href="publisherInfo.homepage_url"
                    target="_blank"
                    class="stocknews-link"
                    ><FontAwesomeIcon
                      icon="fa-link"
                      class="me-1"
                    ></FontAwesomeIcon
                    >Home Page</a
                  >
                </div>
                <div v-if="newsTotalCount > 0">
                  Total News: {{ newsTotalCount }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5>Published News</h5>
            </div>
            <div class="card-body">
              <div class="card-text">
                <LoadingIndicator
                  :loading="newsLoading"
                  message="Loading news..."
                />
                <div v-if="newsError" class="card">
                  <div class="card-header"><h5>Error</h5></div>
                  <div class="card-body">
                    <p class="card-text" style="text-align: justify">
                      Failed to get news. Please try again later. ({{
                        newsErrorMessage
                      }})
                    </p>
                  </div>
                </div>
                <div v-show="!newsLoading">
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
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.stocknews-link {
  color: #0d0d0d;
  text-decoration: none;
  background-color: transparent;
}

.stocknews-link:hover {
  color: #0088c7;
  text-decoration: underline;
}

.stocknews-link:active {
  color: #0077b2;
  text-decoration: underline;
}
</style>
