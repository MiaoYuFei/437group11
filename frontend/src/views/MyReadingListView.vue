<script lang="ts">
import $ from "jquery";
import NewsContainer from "@/components/NewsContainer.vue";
import { handleApi, parseDatetime } from "@/utilities";

export default {
  data() {
    return {
      news_string:
        '[{"article": {"title": "Invest Like Warren Buffett, Not Carl Icahn", "description": "Warren Buffett and Carl Icahn are two of the most successful investors of the past century. But Buffett is a superior model for investors to follow because of his patient style and focus on finding great businesses.", "keywords": ["investing"], "datetime": "2017-04-10T00:24:00Z", "url": "https://www.fool.com/investing/2017/04/09/invest-like-warren-buffett-not-carl-icahn.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/435736/warren-buffett3_tmf.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["BRK.B", "IEP", "BRK.A", "AAPL", "NFLX"]}, \
        {"article": {"title": "Should Apple Investors Believe Tim Cook\'s Promise of Innovation?", "description": "There are nearly 15 billion reasons to do so.", "keywords": ["investing"], "datetime": "2019-03-05T11:03:00Z", "url": "https://www.fool.com/investing/2019/03/05/should-apple-investors-believe-tim-cooks-promise-o.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/514902/apple-keynote-tim-cook-september-event-09122018.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["AAPL"]}, \
        {"article": {"title": "Apple Is Going to Be Late to 5G -- So What?", "description": "Apple won\'t be the first to adopt this new wireless technology, but that doesn\'t mean the company will be completely helpless.", "keywords": ["investing"], "datetime": "2019-03-03T13:15:00Z", "url": "https://www.fool.com/investing/2019/03/03/apple-is-going-to-be-late-to-5g-so-what.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/514453/apple-customer.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["AAPL"]}]',
      news_list: [
        {
          id: String,
          article: {
            title: String,
            description: String,
            keywords: [String],
            datetime: String,
            url: String,
          },
          cover_image: {
            url: String,
          },
          publisher: {
            name: String,
            homepage: {
              url: String,
            },
            logo: {
              url: String,
            },
          },
          tickers: [String],
        },
      ],
      email: "",
      signedIn: false,
      emailVerified: false,
    };
  },
  methods: {
    parseDatetime,
    onGetUserStatus: function () {
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
    onGetPreferences() {
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
          }
        } else {
          // TODO: Handle error
        }
      });
    },
  },
  created() {
    document.title = "My Feeds - " + (this as any).$projectName;
  },
  mounted() {
    this.onGetUserStatus();
    this.onGetPreferences();
    this.news_list = JSON.parse(this.news_string);
  },
  components: {
    NewsContainer,
  },
};
</script>
<template>
  <div v-if="emailVerified">
    <span class="fw-bold">Selected news for you:</span>
    <div class="container">
      <NewsContainer :newsData="news_list" />
    </div>
  </div>
</template>
