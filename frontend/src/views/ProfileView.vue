<script lang="ts">
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { handleApi } from "@/utilities";

export default {
  data() {
    return {
      userid: "",
      username: "",
      email: "",
    };
  },
  methods: {
    update() {
      handleApi("post", "/api/user/status", []).then((doc) => {
        var code = doc.data.code;
        var data = doc.data.data;
        console.log(data);
        if (parseInt(code) == 200) {
          this.userid = data.id;
          this.username = data.username;
          this.email = data.email;
        }
      });
    },
  },
  mounted() {
    this.update();
  },
  components: {
    FontAwesomeIcon,
  },
};
</script>
<template>
  <div class="page-content page-container" id="page-content">
    <div class="padding">
      <div class="row container d-flex justify-content-center">
        <div class="col-xl-6 col-md-12">
          <div class="card user-card-full">
            <div class="row m-l-0 m-r-0">
              <div class="col-sm-4 bg-c-lite-green user-profile">
                <div class="card-block text-center text-white">
                  <div class="m-b-25">
                    <h1><FontAwesomeIcon icon="fa-user" class="me-2" /></h1>
                  </div>
                  <h3 class="f-w-600">{{ username }}</h3>
                </div>
              </div>
              <div class="col-sm-8">
                <div class="card-block">
                  <h3 class="m-b-20 p-b-5 b-b-default f-w-600">
                    User Information
                  </h3>
                  <div class="row">
                    <div class="col-sm-6">
                      <p class="m-b-10 f-w-600">Email</p>
                      <h6 class="text-muted f-w-400">{{ email }}</h6>
                    </div>
                    <div class="col-sm-6">
                      <p class="m-b-10 f-w-600">Verified</p>
                      <h6 class="text-muted f-w-400">True</h6>
                    </div>
                  </div>
                  <h5 class="m-b-20 m-t-40 p-b-5 b-b-default f-w-600">
                    Preference
                  </h5>
                  <div class="row">
                    <div class="col-sm-6">
                      <p class="m-b-10 f-w-600">Recent</p>
                      <h6 class="text-muted f-w-400">Economy</h6>
                    </div>
                  </div>
                  <ul class="social-link list-unstyled m-t-40 m-b-10">
                    <li>
                      <a
                        href="#!"
                        data-toggle="tooltip"
                        data-placement="bottom"
                        title=""
                        data-original-title="facebook"
                        data-abc="true"
                        ><i
                          class="mdi mdi-facebook feather icon-facebook facebook"
                          aria-hidden="true"
                        ></i
                      ></a>
                    </li>
                    <li>
                      <a
                        href="#!"
                        data-toggle="tooltip"
                        data-placement="bottom"
                        title=""
                        data-original-title="twitter"
                        data-abc="true"
                        ><i
                          class="mdi mdi-twitter feather icon-twitter twitter"
                          aria-hidden="true"
                        ></i
                      ></a>
                    </li>
                    <li>
                      <a
                        href="#!"
                        data-toggle="tooltip"
                        data-placement="bottom"
                        title=""
                        data-original-title="instagram"
                        data-abc="true"
                        ><i
                          class="mdi mdi-instagram feather icon-instagram instagram"
                          aria-hidden="true"
                        ></i
                      ></a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
body {
  background-color: #f9f9fa;
}

.padding {
  padding: 3rem !important;
}

.user-card-full {
  overflow: hidden;
}

.card {
  border-radius: 6px;
  -webkit-box-shadow: 0 1px 20px 0 rgba(69, 90, 100, 0.08);
  box-shadow: 0 1px 20px 0 rgba(69, 90, 100, 0.08);
  border: none;
  margin-bottom: 30px;
}

.m-r-0 {
  margin-right: 0px;
}

.m-l-0 {
  margin-left: 0px;
}

.user-card-full .user-profile {
  border-radius: 5px 0 0 5px;
}

.bg-c-lite-green {
  background: -webkit-gradient(
    linear,
    left top,
    right top,
    from(#5d4a8b),
    to(#5aee66)
  );
  background: linear-gradient(to right, #a3bded, #6991c7);
}

.user-profile {
  padding: 40px 0;
}

.card-block {
  padding: 1.25rem;
}

.m-b-25 {
  margin-bottom: 25px;
}

.img-radius {
  border-radius: 5px;
}

h6 {
  font-size: 14px;
}

.card .card-block p {
  line-height: 25px;
}

@media only screen and (min-width: 1400px) {
  p {
    font-size: 14px;
  }
}

.card-block {
  padding: 1.25rem;
}

.b-b-default {
  border-bottom: 1px solid #e0e0e0;
}

.m-b-20 {
  margin-bottom: 20px;
}

.p-b-5 {
  padding-bottom: 5px !important;
}

.card .card-block p {
  line-height: 25px;
}

.m-b-10 {
  margin-bottom: 10px;
}

.text-muted {
  color: #919aa3 !important;
}

.b-b-default {
  border-bottom: 1px solid #e0e0e0;
}

.f-w-600 {
  font-weight: 600;
}

.m-b-20 {
  margin-bottom: 20px;
}

.m-t-40 {
  margin-top: 20px;
}

.p-b-5 {
  padding-bottom: 5px !important;
}

.m-b-10 {
  margin-bottom: 10px;
}

.m-t-40 {
  margin-top: 20px;
}

.user-card-full .social-link li {
  display: inline-block;
}

.user-card-full .social-link li a {
  font-size: 20px;
  margin: 0 10px 0 0;
  -webkit-transition: all 0.3s ease-in-out;
  transition: all 0.3s ease-in-out;
}
</style>
