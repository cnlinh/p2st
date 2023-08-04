<template>
  <div class="container-fluid">
    <div class="row min-vh-100 bg-100">
      <div class="col-6 d-none d-lg-block" style="--falcon-gutter-x: 0">
        <div class="card mb-3 h-100 d-flex justify-content-center bg-primary">
          <div class="tab-content">
            <div class="tab-pane preview-tab-pane active" role="tabpanel"
              aria-labelledby="tab-dom-60d68d55-fe26-474c-98d8-62d1587bc3f8"
              id="dom-60d68d55-fe26-474c-98d8-62d1587bc3f8">
              <div class="carousel slide overflow-clip" id="carouselExampleCaptions" data-ride="carousel">
                <div class="carousel-indicators">
                  <button class="active" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0"
                    aria-current="true" aria-label="Slide 1"></button>
                  <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1"
                    aria-label="Slide 2"></button>
                  <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2"
                    aria-label="Slide 3"></button>
                </div>
                <div class="carousel-inner light">
                  <div class="carousel-item active">
                    <img class="d-block w-100" src="../assets/img/generic/8.jpg" alt="First slide" />
                    <div class="carousel-caption d-none d-md-block">
                      <h5 class="text-white">First Slide Heading</h5>
                      <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      </p>
                    </div>
                  </div>
                  <div class="carousel-item h-100">
                    <img class="d-block w-100" src="../assets/img/generic/8.jpg" alt="Second slide" />
                    <div class="carousel-caption d-none d-md-block">
                      <h5 class="text-white">Second Slide Heading</h5>
                      <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      </p>
                    </div>
                  </div>
                  <div class="carousel-item h-100">
                    <img class="d-block w-100" src="../assets/img/generic/8.jpg" alt="Third slide" />
                    <div class="carousel-caption d-none d-md-block">
                      <h5 class="text-white">Third Slide Heading</h5>
                      <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit
                      </p>
                    </div>
                  </div>
                </div>

                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions"
                  data-bs-slide="prev">
                  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                  <span class="sr-only">Previous</span>
                </button>

                <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions"
                  data-bs-slide="next">
                  <span class="carousel-control-next-icon" aria-hidden="true"></span>
                  <span class="sr-only">Next</span>
                </button>
              </div>
            </div>
          </div>
        </div>
        <!--/.bg-holder-->
      </div>
      <div class="col-sm-10 col-md-6 px-sm-0 align-self-center mx-auto py-5">
        <div class="row justify-content-center g-0">
          <div class="col-lg-9 col-xl-8 col-xxl-6">
            <div class="card">
              <div class="card-body p-4">
                <div class="text-center">
                  <img class="d-block mx-auto mb-4" src="../assets/img/icons/spot-illustrations/45.png" alt="shield"
                    width="100" />
                  <h3>See you again!</h3>
                  <p>
                    You are successfully signed out.
                  </p>
                  <a class="btn btn-primary btn-sm mt-3" href="/login"><span class="fas fa-chevron-left me-1"
                      data-fa-transform="shrink-4 down-1"></span>Return to Login</a>
                </div>
              </div>
            </div>
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