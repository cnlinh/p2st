<template>
  <div class="container-fluid" data-layout="container">
    <!-- side navigation bar -->
    <nav class="navbar navbar-light navbar-vertical navbar-expand-xl">
      <div class="d-flex align-items-center">
        <a class="navbar-brand" href="/home">
          <div class="d-flex align-items-center py-3"><span class="font-sans-serif text-black">P2ST</span>
          </div>
        </a>
      </div>
      <div class="navbar-collapse" id="navbarVerticalCollapse">
        <!-- Navigation -->
        <div class="navbar-vertical-content scrollbar">
          <ul class="navbar-nav flex-column mb-3" id="navbarVerticalNav">
            <div class="nav-link dropdown-indicator">
              <div class="d-flex align-items-center">
                <span class="nav-link-icon"><span class="fas fa-layer-group"></span></span>
                <span class="nav-link-text ps-1">Modules</span>
              </div>
            </div>
            <ul class="nav" id="modules">
              <li class="nav-item" v-for="moduleCode in enrolledModules" :key="moduleCode"
                :class="{ active: moduleCode === selectedModule }" @click="selectModule(moduleCode)">
                <div class="d-flex align-items-center">
                  <span class="nav-link-icon"></span>
                  <span class="nav-link-text ps-1">{{ moduleCode }}</span>
                </div>
              </li>
            </ul>
            <div class="nav-link dropdown-indicator">
              <div class="d-flex align-items-center"><span class="nav-link-icon"><span
                    class="fas fa-book"></span></span><span class="nav-link-text ps-1">Topics</span>
              </div>
            </div>
            <ul class="nav" id="topics">
              <li class="nav-item" v-for="topic in topics" :key="topic?.id" :class="{ active: topic?.id === selectedTopic?.id }"
                @click="selectTopic(topic)">
                <div class="d-flex align-items-center">
                  <span class="nav-link-icon"></span>
                  <span class="nav-link-text ps-1">{{ topic.name }}</span>
                </div>
              </li>
            </ul>
            <li class="nav-item">
              <!-- parent pages--><a class="nav-link" role="button" @click.prevent="handleChangeStudentId">
                <div class="d-flex align-items-center">
                  <span class="nav-link-icon"><span class="fas fa-id-card"></span></span><span
                    class="nav-link-text ps-1">Change Student ID</span>
                </div>
              </a>
            </li>
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
          <div class="d-flex align-items-center"><span class="font-sans-serif text-black">P2ST</span>
          </div>
        </a>
        <ul class="navbar-nav navbar-nav-icons ms-auto flex-row align-items-center">
          <li class="nav-item">
            <!-- email display -->
            <div class="nav-link d-flex align-items-center">
              <div class="email-icon d-flex align-items-center justify-content-center me-1"
                style="background-color: black; width: 35px; height: 35px; border-radius: 5px;">
                <span class="text-white">{{ emailInitial }}</span>
              </div>
              <span>linh.caongoc12@gmail.com</span>
            </div>
          </li>
        </ul>
      </nav>
      <!-- Main content -->
      <div class="main-content">
        <slot name="main-content"></slot>
      </div>

      <ModalChangeStudentId ref="modalStudentId" @confirm="handleUpdateStudentId" />
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import ModalChangeStudentId from '@/components/modals/ModalChangeStudentId.vue';

export default {
  name: "BaseLayout",

  components: {
    ModalChangeStudentId,
  },

  computed: {
    ...mapState('admin', ['topics', 'selectedTopic', 'email', 'enrolledModules', 'selectedModule']),

    emailInitial() {
      return this.email ? this.email.charAt(0).toUpperCase() : '';
    }
  },

  methods: {
    ...mapActions('admin', ['initData', 'fetchTopics', 'fetchModules', 'selectTopic', 'selectModule']),
    ...mapActions('auth', ['logout']),

    handleChangeStudentId() {
      this.$refs.modalStudentId.show();
    },

    handleUpdateStudentId() {

    },

    handleLogout() {
      this.logout().then(() => {
        this.$router.push("/logout");
      });
    },
  },

  async mounted() {
    await this.initData();
  },

  watch: {
    selectedModule(newModule, oldModule) {
      if (newModule !== oldModule) {
        this.fetchTopics(newModule);
      }
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

#modules .nav-item {
  cursor: pointer;
  user-select: none;
}

#topics .nav-item {
  cursor: pointer;
  user-select: none;
}

.email-icon {
  font-size: 15px;
}

.email-icon>span {
  display: block;
  width: 100%;
  text-align: center;
}
</style>
