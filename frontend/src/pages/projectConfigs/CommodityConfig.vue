<template>
  <Card>
    <template #title>Commodities</template>
    <template #content>
      My commodities
      <div class="mt-3 flex justify-end">
        <Button
          @click="
            router.push({
              name: 'ProjectProcess',
              params: {
                proj: route.params.proj,
              },
            })
          "
        >
          Processes >>
        </Button>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
</script>

<style scoped></style>
