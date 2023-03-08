<script lang="ts">
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { handleApi } from "@/utilities";

export default {
  data() {
    return {
      errorMessage: "unknown errror",
    };
  },
  methods: {},
  created() {
    document.title = "My Account - " + (this as any).$projectName;
  },
  mounted() {},
  components: {
    FontAwesomeIcon,
  },
};
</script>
<template>
  <div>
    <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasExampleLabel">Offcanvas</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div>
          Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists, etc.
        </div>
        <div class="dropdown mt-3">
          <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
            Dropdown button
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Action</a></li>
            <li><a class="dropdown-item" href="#">Another action</a></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div
      class="container d-flex flex-column align-items-center justify-content-center"
      style="min-height: 100%"
    >
      <div
        class="card col-12 col-md-10 col-lg-8 col-xl-6 col-xxl-5"
        style="box-shadow: 0.2rem 0.2rem 0.1rem #eee"
      >
        <div class="card-body p-4">
          <h3 class="card-title mb-4">
            <FontAwesomeIcon icon="fa-user" class="me-3" />My Account
          </h3>
          <div id="myAccountTab">
            <ul class="nav nav-tabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link active"
                  id="profile-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#profile-tab-pane"
                  type="button"
                  role="tab"
                  aria-controls="profile-tab-pane"
                  aria-selected="true"
                >
                  Profile
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link"
                  id="security-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#security-tab-pane"
                  type="button"
                  role="tab"
                  aria-controls="security-tab-pane"
                  aria-selected="false"
                >
                  Security
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link"
                  id="my-readings-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#my-readings-tab-pane"
                  type="button"
                  role="tab"
                  aria-controls="my-readings-tab-pane"
                  aria-selected="false"
                >
                  My Readings
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link"
                  id="preferences-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#preferences-tab-pane"
                  type="button"
                  role="tab"
                  aria-controls="preferences-tab-pane"
                  aria-selected="false"
                >
                  Preferences
                </button>
              </li>
            </ul>
            <div class="tab-content">
              <div
                class="tab-pane fade show active"
                id="profile-tab-pane"
                role="tabpanel"
                aria-labelledby="profile-tab"
                tabindex="0"
              >
                <form>
                  <div class="form-floating mb-3">
                    <input
                      type="email"
                      readonly
                      class="form-control-plaintext"
                      id="profileInputEmail"
                      placeholder="name@example.com"
                      value="name@example.com"
                    />
                    <label for="profileInputEmail">Email</label>
                  </div>
                  <div class="form-floating mb-3">
                    <input
                      type="text"
                      readonly
                      class="form-control-plaintext"
                      id="profileInputName"
                      placeholder="Username"
                      value="Username"
                    />
                    <label for="profileInputName">Name</label>
                  </div>
                  <button class="btn btn-primary">Edit</button>
                </form>
              </div>
              <div
                class="tab-pane fade"
                id="security-tab-pane"
                role="tabpanel"
                aria-labelledby="security-tab"
                tabindex="0"
              >
                <form>
                  <div class="mb-3">
                    <label
                      name="currentPassword"
                      for="securityInputCurrentPassword"
                      class="form-label"
                      >Current password</label
                    >
                    <input
                      type="password"
                      class="form-control"
                      id="securityInputCurrentPassword"
                    />
                  </div>
                  <div class="mb-3">
                    <label
                      name="newPassword"
                      for="securityInputNewPassword"
                      class="form-label"
                      >New password</label
                    >
                    <input
                      type="password"
                      class="form-control"
                      id="securityInputNewPassword"
                    />
                  </div>
                  <div class="mb-3">
                    <label
                      name="newPasswordConfirmation"
                      for="securityInputNewPasswordConfirmation"
                      class="form-label"
                      >Confirm new password</label
                    >
                    <input
                      type="password"
                      class="form-control"
                      id="securityInputNewPasswordConfirmation"
                    />
                  </div>
                  <button type="submit" class="btn btn-primary">Save</button>
                </form>
              </div>
              <div
                class="tab-pane fade"
                id="my-readings-tab-pane"
                role="tabpanel"
                aria-labelledby="my-readings-tab"
                tabindex="0"
              >
                ...
              </div>
              <div
                class="tab-pane fade"
                id="preferences-tab-pane"
                role="tabpanel"
                aria-labelledby="preferences-tab"
                tabindex="0"
              >
                <form>
                  <p>Select the categories you are interested in.</p>
                  <div class="d-flex flex-wrap gap-2">
                    <div
                      v-for="(item, index) in [
                        { key: 'algriculture', value: 'Agriculture' },
                        { key: 'mining', value: 'Mining' },
                        { key: 'construction', value: 'Construction' },
                        { key: 'manufacuring', value: 'Manufacturing' },
                        { key: 'transportation', value: 'Transportation' },
                        { key: 'wholesale', value: 'Wholesale' },
                        { key: 'retail', value: 'Retail' },
                        { key: 'finance', value: 'Finance' },
                        { key: 'services', value: 'Services' },
                        {
                          key: 'public_administration',
                          value: 'Public Administration',
                        },
                      ]"
                      :key="index"
                    >
                      <input
                        type="checkbox"
                        class="btn-check"
                        :name="'inputCheck_' + item.key"
                        :id="'inputCheck_' + item.key"
                        autocomplete="off"
                      />
                      <label
                        class="btn btn-outline-primary"
                        :for="'inputCheck_' + item.key"
                        >{{ item.value }}</label
                      >
                    </div>
                  </div>
                  <hr />
                  <button class="btn btn-primary">Edit</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.form-floating label,
.form-floating input {
  padding-left: 0;
}

#myAccountTab {
  display: flex;
  flex-direction: row;
}

#myAccountTab .nav-tabs {
  display: flex;
  flex-direction: column;
  border: none;
}

#myAccountTab .nav-tabs .nav-link {
  width: 100%;
  border: none;
  border-radius: 0;
  color: rgb(57, 169, 225);
}

#myAccountTab .nav-tabs .nav-link:hover {
  background: rgba(134, 203, 237, 0.6);
}

#myAccountTab .nav-tabs .nav-link:active {
  background: rgba(134, 203, 237, 1);
}

#myAccountTab .nav-tabs .nav-link.active {
  background: rgba(134, 203, 237, 0.8);
  color: #222;
}

#myAccountTab .tab-content .tab-pane {
  margin-left: 1rem;
}
</style>
