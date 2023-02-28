 <script lang="ts">
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import BsAlert from "@/components/BsAlert.vue";
import BsButton from "@/components/BsButton.vue";
import { disableForm, enableForm, focusForm, handleApi } from "@/utilities";

export default {
  data() {
    return{
      userid:"",
      username:"",
      email:"",
      emailVerified:"",
    }
  },
  watch: {
    loading(newValue) {
      const formAlert = this.$refs.formAlert as typeof BsAlert;
      if (newValue) {
        formAlert.hide();
        disableForm(this.$refs.form);
      } else {
        formAlert.show();
        enableForm(this.$refs.form);
      }
    },
  },
 methods:{
            update(){
                  handleApi(this.$refs.form, []).then(doc => {
                          var code = doc.data.code;
                          var data = doc.data.data;
                      if (parseInt(code) == 200){
                        this.userid = data.id;
                        this.username = data.username;
                        this.email = data.email;
                        this.emailVerified = data.emailVerified;
                      }   
                  })
            },
        },
  mounted() {
    this.update()
  },
  components: {
    FontAwesomeIcon,
    BsAlert,
    BsButton,
  },
};
</script>
<template>
<div class="page-content page-container" id="page-content">
  <link href="/Users/xuruowen/Documents/437group11-main/frontend/stocknews/src/views/trt.css" rel="stylesheet" type="text/css"/>
    <div class="padding">
        <div class="row container d-flex justify-content-center">
            <div class="col-xl-6 col-md-12">
                      <div class="card user-card-full">
                          <div class="row m-l-0 m-r-0">
                              <div class="col-sm-4 bg-c-lite-green user-profile">
                                  <div class="card-block text-center text-white">
                                      <div class="m-b-25">
                                        <h2><FontAwesomeIcon icon="fa-user" class="me-2" /></h2>
                                      </div>
                                      <h3 class="f-w-600">{{username}}</h3>                                 
                                       </div>
                              </div>
                              <div class="col-sm-8">
                                  <div class="card-block">
                                      <h3 class="m-b-20 p-b-5 b-b-default f-w-600">User Information</h3>
                                      <div class="row">
                                          <div class="col-sm-6">
                                              <p class="m-b-10 f-w-600">Email</p>
                                              <h6 class="text-muted f-w-400">{{email}}</h6>
                                          </div>
                                      </div>
                                     <h5 class="m-b-20 m-t-40 p-b-5 b-b-default f-w-600"> </h5>
                                      <div class="row">
                                          <div class="col-sm-6">
                                              <p class="m-b-10 f-w-600"> </p>
                                              <h6 class="text-muted f-w-400"></h6>
                                          </div>
                                      </div>
                                      <ul class="social-link list-unstyled m-t-40 m-b-10">
                                          <li><a href="#!" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="facebook" data-abc="true"><i class="mdi mdi-facebook feather icon-facebook facebook" aria-hidden="true"></i></a></li>
                                          <li><a href="#!" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="twitter" data-abc="true"><i class="mdi mdi-twitter feather icon-twitter twitter" aria-hidden="true"></i></a></li>
                                          <li><a href="#!" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="instagram" data-abc="true"><i class="mdi mdi-instagram feather icon-instagram instagram" aria-hidden="true"></i></a></li>
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