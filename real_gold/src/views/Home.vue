<template lang="pug">
  .home
    //- v-parallax(height="800" src="@/assets/back.jpg")
    v-container
      v-row
        v-col.z-1
          PayForm.elevation-20
      v-row
        v-col(cols=12 md=4).z-1
          .faq.rounded-xl.pa-5.elevation-20.block
            h2.text-center FAQ
            h3 Delivery
            p Delivery usually takes 5 to 20 minutes :) 
              | When the end of the world in full swing, 
              | the delivery time can be up to 24 hours.
            h3 How to bye?
            p Place and pay for your order. It's all :) Wait your gold in game!
            h3 Contacts
            span Email: 
              a(href="mailto:mail").black--text mail
        v-col.z-1
          .reviews.text-center.rounded-xl.pa-5.elevation-20.block
            h2 REVIEWS
            Thanks
            Reviews
    v-img(src="@/assets/c.png" contain position="right bottom").c.d-none.d-md-block
      
</template>

<script>
import PayForm from "@/components/PayForm.vue"
import Reviews from "@/components/Reviews.vue"
import Thanks from "@/components/Thanks.vue"

export default {
  name: "Home",

  components: {
    PayForm,
    Reviews,
    Thanks,
  },
}
</script>

<style lang="sass" scoped>
.c
  position: fixed
  bottom: 0
  right: 0
  height: 100vh
  max-width: 100vw
  z-index: 0
  opacity: 0.4
.z-1
  z-index: 1
</style>
