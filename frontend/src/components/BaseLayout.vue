<template>
  <div class="container-fluid" data-layout="container">
    <!-- side navigation bar -->
    <nav class="navbar navbar-light navbar-vertical navbar-expand-xl">
      <div class="d-flex align-items-center">
        <a class="navbar-brand" href="/home">
          <div class="d-flex align-items-center py-3"><span class="font-sans-serif text-black">CS3243</span>
          </div>
        </a>
      </div>
      <div class="navbar-collapse" id="navbarVerticalCollapse">
        <!-- Navigation -->
        <div class="navbar-vertical-content scrollbar">
          <ul class="navbar-nav flex-column mb-3" id="navbarVerticalNav">
            <li class="nav-item">
              <router-link to="/home" class="nav-link">
                <div class="d-flex align-items-center">
                  <span class="nav-link-icon"><span class="fas fa-home"></span></span><span
                    class="nav-link-text ps-1">Home</span>
                </div>
              </router-link>
            </li>
            <div class="nav-link dropdown-indicator">
              <div class="d-flex align-items-center"><span class="nav-link-icon"><span
                    class="fas fa-book"></span></span><span class="nav-link-text ps-1">Topics</span>
              </div>
            </div>
            <ul class="nav" id="topics">
              <li class="nav-item" v-for="topic in topics" :key="topic.id" :class="{ active: topic.id === selectedTopic }"
                @click="selectTopicHandler(topic.id)">
                <div class="d-flex align-items-center">
                  <span class="nav-link-icon"></span>
                  <span class="nav-link-text ps-1">{{ topic.name }}</span>
                </div>
              </li>
            </ul>
            <li class="nav-item">
              <!-- parent pages--><a class="nav-link" role="button" @click.prevent="handleLogout">
                <div class="d-flex align-items-center">
                  <span class="nav-link-icon"><span class="fas fa-door-open"></span></span><span
                    class="nav-link-text ps-1">Logout</span>
                </div>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="content">
      <!-- top nav bar -->
      <nav class="navbar navbar-light navbar-glass navbar-top navbar-expand">
        <a class="navbar-brand me-1 me-sm-3" href="/home">
          <div class="d-flex align-items-center"><span class="font-sans-serif text-black">CS3243</span>
          </div>
        </a>
        <ul class="navbar-nav align-items-center d-none d-lg-block">
          <li class="nav-item">
            <div class="search-box" data-list='{"valueNames":["title"]}'>
              <form class="position-relative" data-bs-toggle="search" data-bs-display="static">
                <input class="form-control search-input fuzzy-search" type="search" placeholder="Search..."
                  aria-label="Search" />
                <span class="fas fa-search search-box-icon"></span>
              </form>
            </div>
          </li>
        </ul>
        <ul class="navbar-nav navbar-nav-icons ms-auto flex-row align-items-center">
          <li class="nav-item dropdown">
            <!-- notification -->
            <a class="nav-link notification-indicator notification-indicator-primary px-0 fa-icon-wait"
              id="navbarDropdownNotification" role="button" data-bs-toggle="dropdown" aria-haspopup="true"
              aria-expanded="false" data-hide-on-body-scroll="data-hide-on-body-scroll"><span class="fas fa-bell"
                data-fa-transform="shrink-6" style="font-size: 33px"></span></a>
          </li>
        </ul>
      </nav>
      <!-- Main content -->
      <div class="main-content">
        <slot name="main-content"></slot>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: "BaseLayout",

  computed: {
    ...mapState('admin', ['topics', 'selectedTopic'])
  },

  mounted() {
    this.$store.dispatch('admin/initData');
  },

  methods: {
    handleLogout() {
      this.$store.dispatch("auth/logout").then(() => {
        this.$router.push("/logout");
      });
    },

    selectTopicHandler(topicId) {
      this.$store.dispatch('admin/selectTopic', topicId);
    }
  },
};
</script>

<style scoped>
.username {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.active {
  background-color: #767676;
}

.active,
.active * {
  color: #fff !important;
}

#topics .nav-item {
  cursor: pointer;
  user-select: none;
}
</style>
