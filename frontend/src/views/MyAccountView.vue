<script lang="ts">
import $ from "jquery";
import { handleApi } from "@/utilities";

export default {
  data() {
    return {
      userid: "",
      username: "",
      useremail: "",
      profileLoading: true,
      errorMessage: "unknown errror",
    };
  },
  methods: {
    onUpdateStatus() {
      this.profileLoading = true;
      handleApi("post", "/api/user/status", []).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code == 200) {
          this.profileLoading = false;
          this.userid = data.id;
          this.username = data.name;
          this.useremail = data.email;
        } else {
          this.errorMessage = data.reason;
        }
      });
    },
    onSubmitPreferences() {
      const apiData: { [key: string]: boolean } = {};
      $(this.$refs.formPreferences as Element)
        .find("input")
        .each(function () {
          const jqObj = $(this);
          const name: string = jqObj.attr("name") as string;
          apiData[name] = jqObj.is(":checked");
        });
      handleApi("post", "/api/user/updatepreferences", apiData).then(
        (response) => {
          const code = parseInt(response.data.code);
          const data = response.data.data;
          if (code == 200) {
            this.errorMessage = "Preferences updated successfully.";
          } else {
            this.errorMessage = data.reason;
          }
        }
      );
    },
    onUpdatePreferences() {
      handleApi("post", "/api/user/getpreferences", []).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;

        if (code == 200) {
          for (const key in data.preferences) {
            const value =
              data.preferences[key].toString().toLowerCase() === "true";
            $(this.$refs.formPreferences as Element)
              .find(`input[name="${key}"]`)
              .prop("checked", value);
          }
        } else {
          this.errorMessage = data.reason;
        }
      });
    },
  },
  created() {
    document.title = "My Account - " + (this as any).$projectName;
  },
  mounted() {
    this.onUpdateStatus();
    this.onUpdatePreferences();
  },
  components: {},
};
</script>
<template>
  <div class="d-flex">
    <div
      class="offcanvas-lg offcanvas-start text-bg-dark"
      tabindex="-1"
      id="offcanvas"
      aria-labelledby="offcanvasLabel"
    >
      <div class="offcanvas-header d-lg-none">
        <h5 class="offcanvas-title" id="offcanvasLabel">Navigation</h5>
        <button
          type="button"
          class="btn-close btn-close-white"
          data-bs-dismiss="offcanvas"
          data-bs-target="#offcanvas"
          aria-label="Close"
        ></button>
      </div>
      <div class="offcanvas-body">
        <div>
          <ul class="nav nav-tabs w-100" role="tablist">
            <li
              class="nav-item"
              role="presentation"
              v-for="(item, index) in [
                { key: 'profile', value: 'Profile' },
                { key: 'security', value: 'Security' },
                { key: 'preferences', value: 'Preferences' },
              ]"
              :key="index"
            >
              <button
                :class="'nav-link' + (index === 0 ? ' active' : '')"
                :id="'tab_' + item.key"
                data-bs-toggle="tab"
                :data-bs-target="'#tabPane_' + item.key"
                type="button"
                role="tab"
                :aria-controls="'tabPane_' + item.key"
                :aria-selected="index === 0 ? 'true' : 'false'"
              >
                {{ item.value }}
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div>
      <div class="p-4">
        <div class="tab-content">
          <div
            class="tab-pane fade show active"
            id="tabPane_profile"
            role="tabpanel"
            aria-labelledby="tab_profile"
            tabindex="0"
          >
            <h5 class="user-select-none">Profile</h5>
            <form style="min-width: 18rem">
              <div class="mb-3">
                <label class="d-block user-select-none">Id</label>
                <label class="d-block text-muted placeholder-glow"
                  ><span class="placeholder col-8" v-if="profileLoading"></span
                  >{{ userid }}</label
                >
              </div>
              <div class="mb-3">
                <label class="d-block user-select-none">Name</label>
                <label class="d-block text-muted placeholder-glow"
                  ><span class="placeholder col-6" v-if="profileLoading"></span
                  >{{ username }}</label
                >
              </div>
              <div class="mb-3">
                <label class="d-block user-select-none">Email</label>
                <label class="d-block text-muted placeholder-glow"
                  ><span class="placeholder col-6" v-if="profileLoading"></span
                  >{{ useremail }}</label
                >
              </div>
              <hr />
              <button class="btn btn-primary">Edit</button>
            </form>
          </div>
          <div
            class="tab-pane fade"
            id="tabPane_security"
            role="tabpanel"
            aria-labelledby="tab_security"
            tabindex="0"
          >
            <h5 class="user-select-none">Security</h5>
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
              <hr />
              <button type="submit" class="btn btn-primary">Save</button>
            </form>
          </div>
          <div
            class="tab-pane fade"
            id="tabPane_preferences"
            role="tabpanel"
            aria-labelledby="tab_preferences"
            tabindex="0"
          >
            <h5 class="user-select-none">Preferences</h5>
            <form @submit.prevent="onSubmitPreferences" ref="formPreferences">
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
                    :name="item.key"
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
              <button class="btn btn-primary">Save</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
@import url("@/assets/common.css");

.form-floating label,
.form-floating input {
  padding-left: 0;
}

.offcanvas-body > * {
  display: flex;
  flex-direction: row;
}

.offcanvas-body .nav-tabs {
  display: flex;
  flex-direction: column;
  border: none;
}

.offcanvas-body .nav-tabs .nav-link {
  width: 100%;
  padding: 1rem;
  margin: 0.1rem;
  border: none;
  border-radius: 0.25rem;
  color: #eee;
}

.offcanvas-body .nav-tabs .nav-link:hover {
  background: rgb(255 255 255 / 10%);
}

.offcanvas-body .nav-tabs .nav-link:active {
  background: rgb(255 255 255 / 30%);
}

.offcanvas-body .nav-tabs .nav-link.active {
  background: rgb(255 255 255 / 20%);
}

.tab-content {
  width: 100%;
}

.offcanvas-lg + .container {
  min-height: 100%;
  overflow: auto;
}
</style>
