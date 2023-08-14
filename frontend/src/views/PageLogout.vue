<template>
  <div class="row flex-center min-vh-100 py-6">
    <div class="col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4">
      <div class="d-flex flex-center mb-4"><a class="navbar-brand" href="/home">
          <div class="d-flex align-items-center py-3"><span
              class="font-sans-serif fw-bolder fs-5 d-inline-block text-black">CS3243</span>
          </div>
        </a></div>
      <div class="card">
        <div class="card-body p-4 p-sm-5">
          <div class="text-center"><img class="d-block mx-auto mb-4" src="../assets/img/icons/spot-illustrations/45.png"
              alt="shield" width="100" />
            <h4>See you again!</h4>
            <p>You are successfully signed out.</p><a class="btn btn-primary btn-sm mt-3" href="/login"><span
                class="fas fa-chevron-left me-1" data-fa-transform="shrink-4 down-1"></span>Return to
              Login</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "../vendors/simplebar/simplebar.min.css";
@import "../assets/css/user.min.css";
@import "../assets/css/theme.min.css";
@import "https://fonts.googleapis.com/css?family=Open+Sans:300,400,500,600,700%7cPoppins:300,400,500,600,700,800,900&amp;display=swap";
</style>