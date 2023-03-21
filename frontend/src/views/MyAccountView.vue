<script lang="ts">
import $ from "jquery";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { getFormData, handleApi } from "@/utilities";
import { VueRecaptcha } from "vue-recaptcha";

export default {
  name: "UserSettings",
  data() {
    return {
      userid: "",
      username: "",
      useremail: "",
      updatedUsername: "",
      formProfileInEdit: false,
      formProfileGetLoading: false,
      formProfileSetLoading: false,
      formSecuritySetLoading: false,
      formPreferencesGetLoading: true,
      formPreferencesSetLoading: false,
      formProfileAlertMessage: "unknown errror",
      formSecurityAlertMessage: "unknown errror",
      formPreferencesAlertMessage: "unknown errror",
      formSecurityPasswordMatch: true,
      formSecurityPasswordWeak: false,
      formSecurityRecaptchaResponse: "",
      formSecurityRecaptchaChecked: true,
    };
  },
  watch: {
    formSecuritySetLoading(newValue) {
      const formAlert = $(this.$refs.formSecurityAlert as Element);
      if (newValue) {
        formAlert.fadeOut();
        $(this.$refs.formSecurityRecaptchaContainer as Element).hide();
      } else {
        formAlert.css("display", "flex").hide().fadeIn();
        $(this.$refs.formSecurityRecaptchaContainer as Element).show();
        (this.$refs.formSecurityRecaptcha as VueRecaptcha).reset();
      }
    },
    formPreferencesSetLoading(newValue) {
      const formAlert = $(this.$refs.formPreferencesAlert as Element);
      if (newValue) {
        formAlert.fadeOut();
      } else {
        formAlert.css("display", "flex").hide().fadeIn();
      }
    },
  },
  methods: {
    submitProfileChanges() {
      if (this.updatedUsername) {
        this.username = this.updatedUsername;
      }
      this.formProfileInEdit = false;
    },
    onUpdateProfile() {
      // Pass the user's inputted username to the backend
      // Use 'this.updatedUsername' to access the updated username
      // Implement the backend call here

      // Reset the formProfileInEdit variable to false after successful update
      this.formProfileInEdit = false;
    },
    onGetStatus() {
      this.formProfileGetLoading = true;
      handleApi("post", "/api/user/status", []).then((response) => {
        const code = parseInt(response.data.code);
        const data = response.data.data;
        if (code == 200) {
          this.formProfileGetLoading = false;
          this.userid = data.id;
          this.username = data.name;
          this.useremail = data.email;
        } else {
          this.formProfileAlertMessage = data.reason;
        }
      });
    },
    onSetSecurity() {
      if (!this.formSecurityPasswordMatch) {
        return false;
      }
      if (
        (
          $(this.$refs.formSecurity as Element)
            .find("input[name='newPassword']")
            .val() as any
        ).length < 6
      ) {
        this.formSecurityPasswordWeak = true;
        return false;
      }
      if (this.formSecurityRecaptchaResponse == "") {
        this.formSecurityRecaptchaChecked = false;
        return false;
      }
      const formSecurityLastRecaptchaResponse =
        this.formSecurityRecaptchaResponse;
      this.formSecurityRecaptchaChecked = true;
      this.formSecurityRecaptchaResponse = "";
      this.formSecuritySetLoading = true;
      const apiData = getFormData(this.$refs.formSecurity, [
        "currentPassword",
        "newPassword",
      ]);
      apiData["recaptcha_response"] = formSecurityLastRecaptchaResponse;
      handleApi("post", "/api/user/updatepassword", apiData).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            (this.$refs.formSecurity as any).reset();
            this.formSecurityAlertMessage = "Password updated successfully.";
            this.formSecuritySetLoading = false;
          } else {
            this.formSecurityAlertMessage = response.data.data.reason;
            this.formSecuritySetLoading = false;
          }
        },
        (error) => {
          this.formSecurityAlertMessage = error.message;
          this.formSecuritySetLoading = false;
        }
      );
    },
    onSetPreferences() {
      this.formPreferencesSetLoading = true;
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
            this.formPreferencesAlertMessage =
              "Preferences updated successfully.";
          } else {
            this.formPreferencesAlertMessage = data.reason;
          }
          this.formPreferencesSetLoading = false;
          const queries: any = {};
          for (const key in this.$route.query) {
            if (key !== "showSetPreferences") {
              queries[key] = this.$route.query[key];
            }
          }
          this.$router.replace({ query: queries, hash: this.$route.hash });
        }
      );
    },
    onGetPreferences() {
      if (this.$route.query.showSetPreferences === "true") {
        this.formPreferencesAlertMessage = "Please select your preferences.";
        this.formPreferencesGetLoading = false;
        $(this.$refs.formPreferencesAlert as Element)
          .css("display", "flex")
          .hide()
          .fadeIn();
      } else {
        this.formPreferencesGetLoading = true;
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
            this.formPreferencesAlertMessage = data.reason;
            this.formPreferencesGetLoading = false;
          }
          this.formPreferencesGetLoading = false;
        });
      }
    },
    onFormPreferencesAlertClose() {
      $(this.$refs.formPreferencesAlert as Element).fadeOut();
    },
    onFormSecurityAlertClose() {
      $(this.$refs.formSecurityAlert as Element).fadeOut();
    },
    onFormSecurityChange() {
      const form = $(this.$refs.formSecurity as Element);
      this.formSecurityPasswordMatch =
        form.find("input[name='newPassword']").val() ===
          form.find("input[name='newPasswordConfirmation']").val() ||
        form.find("input[name='newPasswordConfirmation']").val() === "";
      this.formSecurityPasswordWeak =
        (form.find("input[name='newPassword']").val() as any).length < 6 &&
        (form.find("input[name='newPasswordConfirmation']").val() as any)
          .length != 0;
    },
    onRecaptchaExpired() {
      this.formSecurityRecaptchaResponse = "";
      this.formSecurityRecaptchaChecked = false;
    },
    onRecaptchaChecked(response: string) {
      this.formSecurityRecaptchaResponse = response;
      this.formSecurityRecaptchaChecked = true;
    },
  },
  created() {
    document.title = "My Account - " + (this as any).$projectName;
  },
  mounted() {
    $(this.$refs.formSecurityAlert as Element).fadeOut();
    if (
      this.$route.query.showSetPreferences?.toString().toLowerCase() !== "true"
    ) {
      $(this.$refs.formPreferencesAlert as Element).fadeOut();
    }
    (this.$refs.formSecurity as any).reset();
    $(this.$refs.formSecurity as Element)
      .find("input")
      .on("change keydown keyup keypress paste", this.onFormSecurityChange);
    $(".nav-tabs button[data-bs-toggle]").each(function () {
      const jqObj = $(this);
      const target = jqObj.attr("data-bs-target");
      if (
        target != undefined &&
        "#" + target.substring(target.indexOf("_") + 1).toLowerCase() ==
          window.location.hash.toLowerCase()
      ) {
        jqObj.trigger("click");
      }
    });
    $(".nav-tabs button[data-bs-toggle='tab']").on("click", function (e) {
      let target = $(e.target).attr("data-bs-target");
      target = target?.substring(target.indexOf("_") + 1);
      if (target != undefined) {
        window.location.hash = target;
      }
    });
    this.onGetStatus();
    this.onGetPreferences();
  },
  components: {
    FontAwesomeIcon,
    VueRecaptcha,
  },
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
            <form ref="formProfile" @submit.prevent="submitProfileChanges">
              <div class="mb-3">
                <label class="d-block user-select-none">Id</label>
                <label class="d-block text-muted placeholder-glow"
                  ><span
                    class="placeholder col-8"
                    v-if="formProfileGetLoading"
                  ></span
                  >{{ userid }}</label
                >
              </div>
              <div class="mb-3">
                <label class="d-block user-select-none">Name</label>
                <label
                  class="d-block text-muted placeholder-glow"
                  v-show="!formProfileInEdit"
                >
                  <span
                    class="placeholder col-6"
                    v-if="formProfileGetLoading"
                  ></span
                  >{{ username }}</label
                >
                <input
                  type="text"
                  v-show="formProfileInEdit"
                  v-model="updatedUsername"
                />
              </div>
              <div class="mb-3">
                <label class="d-block user-select-none">Email</label>
                <label class="d-block text-muted placeholder-glow"
                  ><span
                    class="placeholder col-6"
                    v-if="formProfileGetLoading"
                  ></span
                  >{{ useremail }}</label
                >
              </div>
              <hr />
              <button
                class="btn btn-primary"
                type="button"
                v-show="!formProfileInEdit"
                @click="formProfileInEdit = true"
              >
                Edit
              </button>
              <div class="mb-3">
                <button
                  class="btn btn-primary"
                  type="submit"
                  v-show="formProfileInEdit"
                >
                  Save
                </button>
                <button
                  class="btn btn-secondary"
                  type="button"
                  v-show="formProfileInEdit"
                  style="margin-left:20px;"
                  @click="formProfileInEdit = false"
                >
                  Cancel
                </button>
              </div>
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
            <form @submit.prevent="onSetSecurity" ref="formSecurity">
              <div class="mb-3">
                <label for="securityInputCurrentPassword" class="form-label"
                  >Current password</label
                >
                <input
                  type="password"
                  name="currentPassword"
                  class="form-control"
                  id="securityInputCurrentPassword"
                />
              </div>
              <div class="mb-3">
                <label for="securityInputNewPassword" class="form-label"
                  >New password</label
                >
                <input
                  type="password"
                  name="newPassword"
                  class="form-control"
                  id="securityInputNewPassword"
                />
                <span
                  v-if="formSecurityPasswordWeak"
                  class="text-danger d-block"
                  >Password minimum length is 6.</span
                >
              </div>
              <div class="mb-3">
                <label
                  for="securityInputNewPasswordConfirmation"
                  class="form-label"
                  >Confirm new password</label
                >
                <input
                  type="password"
                  name="newPasswordConfirmation"
                  class="form-control"
                  id="securityInputNewPasswordConfirmation"
                />

                <span
                  v-if="!formSecurityPasswordMatch"
                  class="text-danger d-block"
                  >Password and confirmation don&apos;t match.</span
                >
              </div>
              <div class="mb-3" ref="formSecurityRecaptchaContainer">
                <VueRecaptcha
                  sitekey="6LeQ5LQkAAAAAJ4QjiBn6F9P9lyX76eVMSFGX72X"
                  @verify="onRecaptchaChecked"
                  @expired="onRecaptchaExpired"
                  ref="formSecurityRecaptcha"
                >
                </VueRecaptcha>
                <span v-if="!formSecurityRecaptchaChecked" class="text-danger"
                  >Please complete the reCAPTCHA verification.</span
                >
              </div>
              <hr />
              <div class="mb-3">
                <button type="submit" class="btn btn-primary">Save</button>
              </div>
              <div>
                <div
                  class="alert alert-warning align-items-center mb-0"
                  role="alert"
                  aria-hidden="true"
                  ref="formSecurityAlert"
                >
                  <FontAwesomeIcon icon="fa-circle-exclamation" />
                  <span class="mx-2">
                    {{ formSecurityAlertMessage }}
                  </span>
                  <button
                    type="button"
                    class="btn-close ms-auto"
                    aria-label="Close"
                    @click="onFormSecurityAlertClose"
                  ></button>
                </div>
              </div>
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
            <form @submit.prevent="onSetPreferences" ref="formPreferences">
              <p>Select the categories you are interested in.</p>
              <div class="placeholder-glow" style="min-width: 18rem">
                <span
                  class="placeholder col-12"
                  v-if="formPreferencesGetLoading"
                ></span>
                <span
                  class="placeholder col-12"
                  v-if="formPreferencesGetLoading"
                ></span>
              </div>
              <div
                class="flex-wrap gap-2"
                :class="{
                  'd-none': formPreferencesGetLoading,
                  'd-flex': !formPreferencesGetLoading,
                }"
              >
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
              <div class="mb-3">
                <button type="submit" class="btn btn-primary">
                  <span v-if="!formPreferencesSetLoading">Save</span>
                  <div
                    v-if="formPreferencesSetLoading"
                    class="spinner-border"
                    role="status"
                  >
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </button>
                <RouterLink to="/myreadinglist" class="btn btn-secondary ms-2"
                  >Go to my reading list</RouterLink
                >
              </div>
              <div>
                <div
                  class="alert alert-warning align-items-center mb-0"
                  role="alert"
                  aria-hidden="true"
                  ref="formPreferencesAlert"
                >
                  <FontAwesomeIcon icon="fa-circle-exclamation" />
                  <span class="mx-2">
                    {{ formPreferencesAlertMessage }}
                  </span>
                  <button
                    type="button"
                    class="btn-close ms-auto"
                    aria-label="Close"
                    @click="onFormPreferencesAlertClose"
                  ></button>
                </div>
              </div>
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

form {
  min-width: 20rem;
}
</style>
