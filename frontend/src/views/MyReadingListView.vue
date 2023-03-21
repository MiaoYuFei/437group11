<script lang="ts">
import $ from "jquery";
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, parseDatetime } from "@/utilities";

export default {
  data() {
    return {
      news_list: [],
      email: "",
      signedIn: false,
      emailVerified: false,
      loading: true,
      firstPage: 1,
      lastPage: 3,
      currentPage: 1,
    };
  },
  watch: {
    loading: function (newValue: boolean) {
      if (newValue) {
        $(this.$refs.newsContainer as Element).fadeOut();
      } else {
        $(this.$refs.newsContainer as Element).fadeIn();
      }
    },
  },
  methods: {
    parseDatetime,
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
    onGetPreferences(callback: Function | undefined = undefined) {
      handleApi("post", "/api/user/getpreferences", []).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code == 200) {
          let preferencesAllFalse = true;
          for (const key in data.preferences) {
            const value =
              data.preferences[key].toString().toLowerCase() === "true";
            if (value) {
              preferencesAllFalse = false;
              break;
            }
          }
          if (preferencesAllFalse) {
            this.$router.push("/myaccount?showSetPreferences=true#preferences");
          } else {
            if (callback !== undefined) {
              callback();
            }
          }
        } else {
          // TODO: Handle error
        }
      });
    },
    onGetRecommendationNews() {
      this.loading = true;
      const apiData = {
        requestType: "recommendations",
      };
      handleApi("post", "/api/news/getnews", apiData).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code == 200) {
          this.news_list = data.news;
          this.loading = false;
        } else {
          // TODO: Handle error
        }
      });
    },
    onGetMyFavoriteNews() {
      this.loading = true;
      const apiData = {
        requestType: "myfavorites",
      };
      handleApi("post", "/api/news/getnews", apiData).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code == 200) {
          this.news_list = data.news;
          this.loading = false;
        } else {
          // TODO: Handle error
        }
      });
    },
    onSetNewsSource() {
      const source = $("input[name='btnNewsSource']:checked").val() as string;
      if (source === "recommendations") {
        this.onGetRecommendationNews();
      } else if (source === "myfavorites") {
        this.onGetMyFavoriteNews();
      }
    },
  },
  created() {
    document.title = "My Reading List - " + (this as any).$projectName;
  },
  mounted() {
    this.loading = true;
    this.onGetUserStatus(() => {
      this.onGetPreferences(() => {
        this.onGetRecommendationNews();
      });
    });
  },
  components: {
    NewsContainer,
  },
};
</script>
<template>
  <div style="overflow: auto">
    <div class="container d-flex flex-column h-100 my-3">
      <div
        class="d-block btn-group mb-3"
        role="group"
        aria-label="Basic radio toggle button group"
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
          id="btnMyFavorites"
          value="myfavorites"
          autocomplete="off"
          @click="onSetNewsSource"
        />
        <label class="btn btn-outline-primary" for="btnMyFavorites"
          >My favorites</label
        >
      </div>
      <div
        class="flex-fill justify-content-center align-items-center mb-3"
        :class="{ 'd-flex': loading, 'd-none': !loading }"
      >
        <div
          class="spinner-border text-primary"
          role="status"
          style="width: 4rem; height: 4rem"
        >
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <NewsContainer
        :newsData="news_list"
        class="mb-3"
        :class="{ 'd-block': !loading, 'd-none': loading }"
        ref="newsContainer"
      />
      <nav
        class="mb-3"
        :class="{ 'd-none': loading, 'd-block': !loading }"
        aria-label="Page navigation"
      >
        <ul class="pagination justify-content-center">
          <li class="page-item" href="#" :class="{ disabled: firstPage === 2 }">
            <a class="page-link">Previous</a>
          </li>
          <li v-for="i in lastPage - firstPage + 1" :key="i" class="page-item">
            <a class="page-link" href="#">{{ i + firstPage - 1 }}</a>
          </li>
          <li class="page-item">
            <a class="page-link" href="#">Next</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>
