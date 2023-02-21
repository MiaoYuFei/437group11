<script setup lang="ts">
import $ from "jquery";
</script>
<script lang="ts">
export default {
    created: function () {

    },
    data: () => {
        return {
            searchText: "",
        };
    },
    methods: {
        search_click: function () {
            if (this.searchText === "") {
                return false;
            }
            window.open("/search?q=" + encodeURIComponent(this.searchText), "_blank");
        },
    },
};
</script>
<template>
    <nav class="navbar navbar-expand-lg bg-light" aria-label="Navigation">
        <div class="container-fluid">
            <a class="navbar-brand d-flex align-items-center gap-1" href="#">
                <img src="/src/assets/vue.svg" alt="Logo" width="30" height="24" class="d-inline-block align-text-top">
                Stock News
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Link</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            Dropdown
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">Action</a></li>
                            <li><a class="dropdown-item" href="#">Another action</a></li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li><a class="dropdown-item" href="#">Something else here</a></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link disabled">Disabled</a>
                    </li>
                </ul>
                <form class="d-flex" role="search" @submit.prevent="search_click">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" required
                        v-model="searchText">
                    <button class="btn btn-outline-success" type="submit"><font-awesome-icon icon="fa-magnifying-glass"
                            class="fs-5" /></button>
                </form>
            </div>
        </div>
    </nav>
</template>
<style scoped></style>
