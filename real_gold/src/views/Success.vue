<template lang="pug">
  .pa-12
    v-container
      v-row
        v-col
          .elevation-20.rounded-xl.pa-6.text-center.mx-auto.secondary
              h1 Thanks
              .faq.rounded-xl.pa-5.elevation-1.block.text-left
                h3 Delivery
                p Delivery usually takes 5 to 20 minutes :) 
                  | When the end of the world in full swing, 
                  | the delivery time can be up to 24 hours.
                h3 Contacts
                a(href="").black--text Email
              v-btn(@click='$router.push("/")' color='accent').pa-6.ma-4 Go back
          .text-center.rounded-xl.pa-6.ma-8.mx-auto.elevation-20.block
            h2 REVIEWS
            Thanks
            Reviews

</template>

<script>
import Reviews from '@/components/Reviews.vue'
import Thanks from '@/components/Thanks.vue'

export default {
  components: {
    Reviews,
    Thanks,
  },
}
</script>
