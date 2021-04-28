<template lang="pug">
  .pa-12
    v-container
      v-row
        v-col
          .elevation-20.rounded-xl.pa-6.text-center.mx-auto.secondary
            h1 Payment canceled. 
            v-btn(@click='$router.push("/")' color='accent').pa-6.ma-4 OK

</template>